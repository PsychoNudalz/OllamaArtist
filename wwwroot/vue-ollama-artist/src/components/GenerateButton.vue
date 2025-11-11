<script setup>
import {ref} from 'vue'
import ImageOrder from "@/components/ImageOrder"

// Generating a new image
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
// Taking user input
const prompt_idea = ref('')
const prompt_style = ref('')
const prompt_age = ref(0)

function saveData() {
  console.log({
    prompt_idea: prompt_idea.value,
    prompt_style: prompt_style.value,
    prompt_age: prompt_age.value


  })

  const image_order_object = new ImageOrder({prompt_idea: prompt_idea.value, prompt_style: prompt_style.value, prompt_age: prompt_age.value})
  image_order.value = image_order_object.toJSON()

}
</script>

<template>
  <div class="p-4 max-w-md mx-auto"> Input zone
    <form @submit.prevent="saveData" class="space-y-4">
      <div>
        <label class="block text-sm font-medium">Idea</label>
        <input v-model="prompt_idea" type="text" class="border p-2 w-full rounded" />
      </div>

      <div>
        <label class="block text-sm font-medium">Style</label>
        <input v-model="prompt_style" type="text" class="border p-2 w-full rounded" />
      </div>

      <div>
        <label class="block text-sm font-medium">Age</label>
        <input v-model.number="prompt_age" type="number" class="border p-2 w-full rounded" />
      </div>

      <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded">Save</button>
    </form>
  </div>

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