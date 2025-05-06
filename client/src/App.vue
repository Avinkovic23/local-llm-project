<template>
  <AppHeader />
  <router-view />
</template>

<script>
import AppHeader from './components/AppHeader.vue'

export default {
  name: 'App',
  components: {
    AppHeader
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
