<template>
  <img alt="Vue logo" src="./assets/logo.png">
  <PingButton/>
  <GenerateButton/>
<!--  <HelloWorld msg="Welcome to Your Vue.js App"/>-->
</template>

<script>
// import HelloWorld from './components/HelloWorld.vue'
// import PingButton from './components/PingButton.vue'

import PingButton from './components/PingButton.vue'
import GenerateButton from './components/GenerateButton.vue'

export default {
  name: 'App',
  components: {
    PingButton,
    GenerateButton
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
