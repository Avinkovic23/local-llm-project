from datetime import datetime, timedelta, timezone
import sqlite3
from dotenv import load_dotenv
from passlib.hash import bcrypt
from fastapi import Depends, FastAPI, Request, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import jwt
from pydantic import BaseModel
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from langdetect import detect
import os
import shutil

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
HASH_ALGORITHM = os.getenv("HASH_ALGORITHM")
TOKEN_EXPIRATION = int(os.getenv("TOKEN_EXPIRATION_MINUTES")) 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

embed_model = OllamaEmbedding(model_name="nomic-embed-text")
llm = Ollama(model="mistral", request_timeout=500)

if os.listdir("docs"):
    documents = SimpleDirectoryReader("docs").load_data()
    index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)
    query_engine = index.as_query_engine(llm=llm)
else:
    index = None
    query_engine = None

class QuestionRequest(BaseModel):
    question: str

class LoginRequest(BaseModel):
    username: str
    password: str

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=TOKEN_EXPIRATION)):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=HASH_ALGORITHM)

def verify_token(request: Request):
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header missing.")
    
    token = auth_header.split("Bearer ")[1]

    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[HASH_ALGORITHM])

        if datetime.fromtimestamp(decoded_token["exp"], tz=timezone.utc) < datetime.now(timezone.utc):
            raise HTTPException(status_code=401, detail="Token has expired.")
        
        return decoded_token
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token.")
    
def verify_admin_role(request: Request):
    decoded_token = verify_token(request)
    if decoded_token["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin role required.")

@app.post("/login")
async def login(request: LoginRequest):
    conn = sqlite3.connect("local-llm.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=?", (request.username,))
    user = cursor.fetchone()

    if user is None:
        conn.close()
        raise HTTPException(status_code=401, detail="Invalid credentials.")
    
    stored_password = user[2] 
    if not bcrypt.verify(request.password, stored_password):
        conn.close()
        raise HTTPException(status_code=401, detail="Invalid credentials.")
    
    access_token = create_access_token(data={"sub": user[1], "role": user[3]})

    conn.close()
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/ask")
async def ask_question(payload: QuestionRequest, user: dict = Depends(verify_token)):
    if not query_engine:
        raise HTTPException(status_code=400, detail="Nema dokumenta za pretraživanje. Molimo učitajte PDF datoteku.")
    
    query = payload.question
    lang = detect(query)

    if lang == "en":
        enforced_query = f"Answer in English language ONLY. Question: {query}"
    else:
        enforced_query = f"Answer in Croatian language ONLY. Question: {query}"

    response = query_engine.query(enforced_query)
    return {"response": str(response)}

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...), admin: dict = Depends(verify_admin_role)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    
    file_path = os.path.join("./docs", file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    global query_engine
    documents = SimpleDirectoryReader("docs").load_data()
    index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)
    query_engine = index.as_query_engine(llm=llm)

    return {"message": f"'{file.filename}' uploaded successfully."}