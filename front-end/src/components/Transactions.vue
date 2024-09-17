<template>
  <div>
    <h2>Transactions</h2>
    <button @click="addTransaction">Add Transaction</button>
    <table>
      <thead>
        <tr>
          <th>Category</th>
          <th>Description</th>
          <th>Amount</th>
          <th>Date</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(transaction, index) in transactions" :key="index">
          <td>{{ transaction.category }}</td>
          <td>{{ transaction.description }}</td>
          <td>{{ transaction.amount }}</td>
          <td>{{ transaction.date }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from '@/axios'

export default {
  data() {
    return {
      transactions: []
    }
  },
  async created() {
    this.fetchTransactions()
  },
  methods: {
    async fetchTransactions() {
      try {
        const response = await axios.get('/transactions/')
        this.transactions = response.data
      } catch (error) {
        console.error(error)
      }
    },
    async addTransaction() {
      // Logic to add a transaction
    },
    async deleteTransaction(id) {
      try {
        await axios.delete(`/transactions/${id}`)
        this.fetchTransactions()
      } catch (error) {
        console.error(error)
      }
    },
    editTransaction(id) {
      // Logic to edit a transaction
    }
  }
}
</script>

<style>
table {
  width: 100%;
  border-collapse: collapse;
}

thead th {
  background-color: #f4f4f4;
  padding: 10px;
  border: 1px solid #ddd;
}

tbody td {
  padding: 10px;
  border: 1px solid #ddd;
}
</style>
