<template>
    <header class="header">
        <a href="/">
            <img src="https://images.seeklogo.com/logo-png/59/1/ollama-logo-png_seeklogo-593420.png" alt="ollama-logo">
            <h1>Lokalni LLM</h1>
        </a>
    </header>
    <div class="header-div"></div>
</template>

<script>
export default {
  name: 'AppHeader',
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
    justify-content: flex-start;
    padding-left: 50px;
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
</style>