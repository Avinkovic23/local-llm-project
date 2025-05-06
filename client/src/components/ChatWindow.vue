<template>
  <div class="chat-window">
    <div class="messages-container" v-if="messages.length">
      <div v-for="(msg, index) in messages" :key="index" :class="['message', msg.sender === 'user' ? 'user-message' : '']">
        {{ msg.text }}
      </div>
      <div ref="scrollTarget"></div>
    </div>
    <div class="input-container" :style="{ bottom: showTitle ? '200px' : '0px' }">
      <h1 v-if="showTitle" class="gradient-text">Kako Vam mogu pomoći?</h1>
      <input type="file" ref="fileInput" @change="handleFileChange" style="display: none" accept="application/pdf" />
      <button @click="triggerFileInput" style="border: none; background: none;" v-if="isAdmin">
        <img title="Prenesite dokument" src="https://getdrawings.com/free-icon/upload-icon-png-74.png" alt="Prijenos dokumenata" style="width: 40px; height: 40px;" />
      </button>      
    <textarea v-model="input" placeholder="Postavite pitanje..." class="input-field" rows="4"></textarea>
    <button @click="handleSubmit" :disabled="loading">
      {{ loading ? 'U tijeku...' : 'Pretraži' }}
    </button>
    <div v-if="loading" class="spinner"></div>
    </div>
  </div>
</template>

<script>
import { jwtDecode } from 'jwt-decode';

export default {
  name: 'ChatWindow',
  data() {
    return {
      input: '',
      loading: false,
      messages: [],
      showTitle: true
    };
  },
  computed: {
    isAdmin() {
      const token = localStorage.getItem('access_token');
      const decoded_token = jwtDecode(token);
      return decoded_token && decoded_token.role === 'admin';
    }
  },
  methods: {
    scrollToBottom() {
      this.$nextTick(() => {
        const el = this.$refs.scrollTarget;
        if(el) {
          el.scrollIntoView({ behavior: 'smooth' });
        }
      });
    },

    async handleSubmit() {
      if(!this.input.trim()) {
        alert('Unesite pitanje.');
        return;
      }

      this.loading = true;
      this.showTitle = false;

      const message = this.input.trim();
      this.messages.push({ sender: 'user', text: message });
      this.scrollToBottom();

      try {
        this.input = '';
        const response = await this.fetchAnswer(message);
        this.messages.push({ sender: 'llm', text: response });
      } catch (err) {
        alert(err.message);
      } finally {
        this.loading = false;
      }
    },

    async fetchAnswer(question) {
      try {
        const response = await fetch(process.env.VUE_APP_API_BASE_URL + "ask", {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('access_token')
          },
          body: JSON.stringify({ question })
        });

        if(!response.ok) {
          throw new Error('Problem s konekcijom.');
        }

        const data = await response.json();
        return data.response;
      } 
      catch (error) {
        console.error('Greska kod poziva odgovora:', error);
        throw error;
      }
    },

    triggerFileInput() {
      this.$refs.fileInput.click();
    },

    async handleFileChange(event) {
      const file = event.target.files[0];
      if(file) {
        const message = await this.uploadPdf(file);
        alert(message);
      }
    },

    async uploadPdf(file) {
      try {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch('http://127.0.0.1:8000/upload-pdf', {
          method: 'POST',
          headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('access_token')
          },
          body: formData
        });

        if(!response.ok) {
          alert('Greška prilikom učitavanja PDF-a.');
        }

        const data = await response.json();
        return data.message;
      } 
      catch (error) {
        console.error('Greška kod slanja PDF-a:', error);
        throw error;
      }
    },
  }
};
</script>

<style scoped>
.chat-window {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  width: 100%;
  padding: 50px 20px;
}

.gradient-text {
  background: linear-gradient(180deg, rgba(222, 149, 53, 1) 0%, rgba(224, 191, 83, 1) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-size: 50px;
  margin-bottom: 30px;
  text-align: center;
}

.messages-container {
  width: 60%;
  margin-bottom: 30px;
  padding: 10px;
  background: #2b2b2b;
  border-radius: 10px;
  border: 1px solid #de9535;
  color: white;
  font-size: 16px;
  margin-bottom: 250px;
}

.message {
  margin-bottom: 10px;
  white-space: pre-wrap;
}

.user-message {
  align-self: flex-end;
  max-width: 40%;
  width: fit-content;
  background-color: rgb(64, 62, 62);
  color: white;
  text-align: left;
  border-radius: 20px;
  padding: 15px;
  margin-bottom: 40px;
  margin-top: 40px;
}

.input-container {
  background-color: #2c2a2a;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  position: fixed;
  z-index: 1000;
  bottom: 100px;
  padding-bottom: 50px;
  padding-top: 20px;
}

.input-field {
  width: 50%;
  min-height: 80px;
  padding: 15px;
  border-radius: 10px;
  border: 1px solid #de9535;
  font-size: 16px;
  margin-bottom: 20px;
  background: #3b3b3b;
  color: white;
  outline: none;
  resize: vertical;
}

.input-field::placeholder {
  color: #a0a0a0;
  font-size: 16px;
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
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.spinner {
  margin-top: 20px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #de9535;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

</style>
