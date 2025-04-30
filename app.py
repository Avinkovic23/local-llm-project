from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from langdetect import detect
import os
import shutil

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


@app.post("/ask")
async def ask_question(payload: QuestionRequest):
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
async def upload_pdf(file: UploadFile = File(...)):
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