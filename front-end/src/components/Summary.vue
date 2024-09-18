<template>
  <div>
    <h2>Transaction Summary</h2>
    <div v-if="summaryFetched" class="summary">
      <div class="detail">
        <p>Total income</p>
        <p>${{ summary.total_income.toFixed(2) }}</p>
      </div>
      <div class="detail">
        <p>Total expenses</p>
        <p>${{ summary.total_expenses.toFixed(2) }}</p>
      </div>
      <div class="detail">
        <p>Net savings</p>
        <p>${{ summary.net_savings.toFixed(2) }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from '@/axios'

export default {
  data() {
    return {
      summary: {},
      summaryFetched: false
    }
  },
  async created() {
    try {
      const response = await axios.get('/reports/summary')
      this.summary = response.data
      this.summaryFetched = true
    } catch (error) {
      console.error(error)
    }
  }
}
</script>

<style scoped>
h2 {
  text-align: center;
  margin: 20px;
  max-width: 500px;
}

.summary {
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 40px;
}

.detail {
  display: flex;
  justify-content: space-between;
  max-width: 500px;
}
</style>
