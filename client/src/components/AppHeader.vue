<template>
    <header class="header">
        <a href="/">
            <img src="https://images.seeklogo.com/logo-png/59/1/ollama-logo-png_seeklogo-593420.png" alt="ollama-logo">
            <h1 class="header-title">Lokalni LLM</h1>
        </a>
        <a href="" v-if="isLoggedIn">
            <button class="logout-button" @click="logOut">Odjava</button>
        </a>
    </header>
    <div class="header-div"></div>
</template>

<script>
export default {
  name: 'AppHeader',
  computed: {
    isLoggedIn() {
      return localStorage.getItem('access_token') !== null;
    }
  },
  methods: {
    logOut() {
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
  }
}
</script>

<style>
.header-div {
    height: 10vh;
}
.header {
    position: fixed;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-left: 40px;
    padding-right: 40px;
    width: 100%;
    height: 10vh;
    background: #de9535;
    background: linear-gradient(180deg,rgba(222, 149, 53, 1) 0%, rgba(224, 191, 83, 1) 100%);
}
a {
    display: flex;
    align-items: center;
    gap: 20px;
    text-decoration: none;
    color: #282626;
}
h1 {
    font-size: 25px;
}
img {
    height: 40px;
    width: 40px;
    border-radius: 100%;
}

.logout-button {
    background: #282626;
    color: #de9535;
    padding: 10px;
    width: 100px;
}

@media (max-width: 450px) {
  .header-title {
    visibility: hidden  ;
  }
}
</style>