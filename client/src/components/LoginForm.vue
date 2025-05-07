<template>
    <div class="login-form-container">
        <div class="form">
            <h1 class="form-title">Prijava</h1>
            <div class="login-input-container">
                <span>Korisničko ime</span>
                <input type="text" placeholder="Korisničko ime" v-model="username" />
            </div>
            <div class="login-input-container">
                <span>Lozinka</span>
                <input type="password" placeholder="Lozinka" v-model="password" />
            </div>
            <button @click="handleLogin">Prijava</button>
        </div>
    </div>
</template>

<script>
export default {
    name: 'LoginForm',
    data() {
        return {
            username: '',
            password: ''
        };
    },
    methods: {
        async handleLogin() {
            if(this.username && this.password) {
                try {
                    const response = await fetch(process.env.VUE_APP_API_BASE_URL + "login", {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ username: this.username, password: this.password })
                    });

                    if(!response.ok) {
                        throw new Error('Neispravni podaci za prijavu.');
                    }

                    const data = await response.json();
                    localStorage.setItem('access_token', data.access_token); 
                    window.location.href = '/';
                } 
                catch (error) {
                    alert(error.message);
                }
            } else {
                alert('Molimo unesite korisničko ime i lozinku.');
            }
        }
    }
}
</script>

<style>
.login-form-container {
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}

.form {
    display: flex;
    flex-direction: column;
    margin-top: 100px;
    gap: 20px;
}

.form-title {
    font-size: 40px;
    background: linear-gradient(180deg, rgba(222, 149, 53, 1) 0%, rgba(224, 191, 83, 1) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 50px;
}

.login-input-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
    font-size: 20px;
}

button {
  width: 30%;
  height: 50px;
  border-radius: 10px;
  border: none;
  background: linear-gradient(180deg, rgba(222, 149, 53, 1) 0%, rgba(224, 191, 83, 1) 100%);
  color: #282626;
  font-size: 20px;
  font-weight: bold;
  cursor: pointer;
  transition: opacity 0.3s ease;
  margin-left: auto;
  margin-right: auto;
}

input {
    width: 500px;
    height: 50px;
    padding: 10px;
    border-radius: 10px;
    border: 1px solid #de9535;
    font-size: 16px;
    margin-bottom: 20px;
    background: #3b3b3b;
    color: white;
}

@media (max-width: 750px) {
    input {
        max-width: 400px;
    }

    button {
        width: 50%;
    }
}

@media (max-width: 450px) {
    input {
        max-width: 300px;
    }

    button {
        width: 100%;
    }
}
</style>