<script setup>
import { ref } from 'vue'
// import {default} from "@/components/HostGetter";

const response = ref('');
//TODO: make the IP dynamic
const serverIp = "192.168.4.27:8000"; // backend machine IP and port



async function pingApi() {
  try {
    // now call the actual API
    const res = await fetch(`http://${serverIp}/api/ping`);
    if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
    const data = await res.json();
    response.value = data.message;
  } catch (err) {
    response.value = `Error: ${err.message}`;
  }
}


async function pingApiSystem() {
  try {
    const host = window.location.hostname; // gets current host IP or domain
    const res = await fetch(`http://${host}:8000/api/ping/systems`);
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