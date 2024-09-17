<template>
  <div>
    <h2>Budgets</h2>
    <button @click="addBudget">Add Budget</button>
    <ul>
      <li v-for="budget in budgets" :key="budget.id">
        {{ budget.description }} - {{ budget.limit_amount }} - {{ budget.start_date }} -
        {{ budget.end_date }}
        <button @click="deleteBudget(budget.id)">Delete</button>
        <button @click="editBudget(budget.id)">Edit</button>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from '@/axios'

export default {
  data() {
    return {
      budgets: []
    }
  },
  async created() {
    this.fetchBudgets()
  },
  methods: {
    async fetchBudgets() {
      try {
        const response = await axios.get('/budgets/')
        this.budgets = response.data
      } catch (error) {
        console.error(error)
        this.$router.push('/auth')
      }
    },
    async addBudget() {
      // Logic to add a budget
    },

    async deleteBudget(id) {
      try {
        await axios.delete(`/budgets/${id}`)
        this.fetchBudgets()
      } catch (error) {
        console.error(error)
      }
    },
    editBudget(id) {
      // Logic to edit a budget
    }
  }
}
</script>
