<template>
  <div>
    <h2>Transaction Summary</h2>
    <p>{{ summary }}</p>
  </div>
</template>

<script>
import axios from '@/axios'

export default {
  data() {
    return {
      summary: ''
    }
  },
  async created() {
    try {
      const response = await axios.get('/reports/summary')
      this.summary = response.data
    } catch (error) {
      console.error(error)
    }
  }
}
</script>
