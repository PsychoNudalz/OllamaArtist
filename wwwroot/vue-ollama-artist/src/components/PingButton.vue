<script setup>
import { ref } from 'vue'

const response = ref('')

async function pingApi() {
  try {
    const res = await fetch('http://127.0.0.1:8000/api/ping')
    if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`)
    const data = await res.json()
    response.value = data.message
  } catch (err) {
    response.value = `Error: ${err.message}`
  }
}
async function pingApiSystem() {
  try {
    const res = await fetch('http://127.0.0.1:8000/api/ping/systems')
    if (!res.ok) throw new Error(`HTTP error! status: ${res.status}, ${res.statusText}`)
    const data = await res.json()
    response.value = data.message
  } catch (err) {
    response.value = `Error: ${err.message}`
  }
}

</script>

<template>
  <div>Ping Button
    <button @click="pingApi">Ping API</button>
    <button @click="pingApiSystem">Ping Systems</button>
    <p v-if="response">{{ response }}</p>

  </div>
</template>

<style scoped>

</style>