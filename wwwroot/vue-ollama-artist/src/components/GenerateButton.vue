<script setup>
import {ref} from 'vue'

const response = ref('')
const image_name = ref('')
const image_details = ref('')
const image_http = ref('')

const image_order = ref('')


const serverIp = "192.168.4.27:8000"; // backend machine IP and port


async function generateFull() {
  try {
    response.value = 'Generating...'
    const res = await fetch(`http://${serverIp}/api/generate`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: ""// adjust as needed
    })
    if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`)
    const data = await res.json()
    response.value = data.message
    image_name.value = data.image
  } catch (err) {
    response.value = `Error: ${err.message}`
  }

  if (image_name.value) {
    image_http.value = `http://${serverIp}/api/image/${image_name.value}`

  }
}

async function generateOrder() {
  try {
    response.value = 'Generating...'
    const res = await fetch(`http://${serverIp}/api/generate/order`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: ""// adjust as needed
    })
    if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`)
    const data = await res.json()
    response.value = data.image_prompt
    image_order.value = data.image_order
  } catch (err) {
    response.value = `Error: ${err.message}`
  }
}

async function generateFromOrder() {
  try {
    response.value = 'Generating...'
    const res = await fetch(`http://${serverIp}/api/generate/`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ order: image_order.value })
    })
    if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`)
    const data = await res.json()
    image_name.value = data.image

  } catch (err) {
    response.value = `Error: ${err.message}`
  }

  if (image_name.value) {
    image_http.value = `http://${serverIp}/api/image/${image_name.value}`

  }
}
</script>

<template>
  <div>Generate Buttons
    <div>
      <button @click="generateFull">Generate</button>

      <button @click="generateOrder">Generate Order</button>
    </div>

    <!--    <button @click="pingApiSystem">Ping Systems</button>-->
    <div>

      <button v-if="image_order" @click="generateFromOrder">Generate From Order</button>
    </div>
    <!--    <button @click="pingApiSystem">Ping Systems</button>-->
    <p v-if="response">{{ response }}</p>
    <p v-if="image_details">{{ image_details }}</p>
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