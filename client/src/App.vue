<template>
  <AppHeader />
  <ChatWindow />
</template>

<script>
import AppHeader from './components/AppHeader.vue'
import ChatWindow from './components/ChatWindow.vue'

export default {
  name: 'App',
  components: {
    AppHeader,
    ChatWindow
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  height: 100%;
}

body {
  font-family: 'Arial', sans-serif;
  color: white;
  min-height: 100vh;
  background-color: #2c2a2a;  
  overflow-y: auto;
}
</style>
