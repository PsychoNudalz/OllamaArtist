<script setup>
import { ref } from 'vue'

const response = ref('')
const image_name = ref('')
const image_http = ref('')




async function generate() {
  try {
    response.value = 'Generating...'
    const res = await fetch('http://127.0.0.1:8000/api/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: ""// adjust as needed
    })
    if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`)
    const data = await res.json()
    response.value = data.message
    image_name.value = data.image
  } catch (err) {
    response.value = `Error: ${err.message}`
  }

  if(image_name.value){
    image_http.value = `http://127.0.0.1:8000/api/image/${image_name.value}`

  }
}
</script>

<template>
  <div>Generate Buttons
    <button @click="generate">Generate</button>
<!--    <button @click="pingApiSystem">Ping Systems</button>-->
    <p v-if="response">{{ response }}</p>
    <p v-if="image_name">{{ image_name }}</p>
    <div>
      <img
          v-if="image_http"
          :src="image_http"
          alt="Generated Image"
          style="max-width: 400px; border-radius: 8px;"
      />
      <p v-else>No image generated yet.</p>
    </div>



  </div>
</template>

<style scoped>

</style>