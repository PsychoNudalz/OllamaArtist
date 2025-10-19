<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  /** Text to show on the button (used if the default slot is empty). */
  label: {
    type: String,
    default: '',
  },
  /** Optional CSS class to change the button’s appearance. */
  variant: {
    type: String,
    default: '',
  },
})

// Emit the normal click event so parent components can still listen
const emit = defineEmits(['click'])

// New function that calls the backend ping endpoint
async function handleClick(event) {
  try {
    const res = await fetch('/api/ping', { method: 'POST' })
    if (!res.ok) {
      const err = await res.json()
      console.error('Ping failed:', err)
      alert(`Ping error: ${err.detail}`)
    } else {
      const data = await res.json()
      console.log('Ping success:', data.message)
      // Optionally notify the user
      alert(data.message)
    }
  } catch (e) {
    console.error('Network error while pinging:', e)
    alert('Network error while pinging')
  }
  // Re‑emit the original click event for parent handlers
  emit('click', event)
}
</script>

<template>
  <button
      type="button"
      :class="['my-button', variant]"
      @click="handleClick"
  >
    <slot>{{ label }}</slot>
  </button>
</template>

<style scoped>
/* You can add styles for .my-button here if needed */
</style>