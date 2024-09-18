<template>
  <div>
    <h2>Transactions</h2>
    <div class="add-new-transaction">
      <form @submit.prevent="handleSubmit">
        <div class="select-category">
          <label>Category: </label>
          <div class="custom-select-wrapper">
            <select v-model="selectedCategory" class="custom-select">
              <option disabled value="">Please select one</option>
              <option>Income</option>
              <option>Expense</option>
            </select>
          </div>
        </div>
        <input v-model="description" placeholder="Description" required />
        <input v-model="amount" type="number" step="0.01" placeholder="Amount" required />
        <input v-model="date" type="date" required />
        <button type="submit">{{ isEditing ? 'Save Transaction' : 'Add Transaction' }}</button>
      </form>
    </div>
    <h3>All Transactions</h3>
    <div class="transaction-table">
      <table>
        <thead>
          <tr>
            <th class="category">Category</th>
            <th class="desc">Description</th>
            <th class="amount">Amount</th>
            <th class="date">Date</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(transaction, index) in transactions" :key="index">
            <td>{{ transaction.category }}</td>
            <td>{{ transaction.description }}</td>
            <td>${{ transaction.amount.toFixed(2) }}</td>
            <td>{{ formatDate(transaction.date) }}</td>
            <td class="edit-delete">
              <button @click="editButtonClicked(transaction)" class="edit-button">
                {{ isEditing && transactionId === transaction.id ? 'Cancel' : 'Edit' }}
              </button>
              <button @click="deleteTransaction(transaction.id)" class="delete-button">
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from '@/axios'

export default {
  data() {
    return {
      selectedCategory: 'Income',
      description: '',
      amount: '',
      date: '',
      transactionId: '',
      isEditing: false,
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
        this.$router.push('/auth')
      }
    },
    async addTransaction() {
      try {
        await axios.post('/transactions/', {
          category: this.selectedCategory,
          description: this.description,
          amount: this.amount,
          date: this.date
        })
        this.fetchTransactions()
      } catch (error) {
        console.error(error)
      }
      this.description = ''
      this.amount = ''
      this.date = ''
    },
    async deleteTransaction(id) {
      try {
        await axios.delete(`/transactions/${id}`)
        this.fetchTransactions()
      } catch (error) {
        console.error(error)
      }
    },
    async editTransaction(id) {
      try {
        await axios.put(`/transactions/${id}`, {
          category: this.selectedCategory,
          description: this.description,
          amount: this.amount,
          date: this.date
        })
        this.fetchTransactions()
      } catch (error) {
        console.error(error)
      }
      this.description = ''
      this.amount = ''
      this.date = ''
      this.isEditing = false
      this.transactionId = ''
    },
    async handleSubmit() {
      if (this.isEditing) {
        await this.editTransaction(this.transactionId)
      } else {
        await this.addTransaction()
      }
    },
    editButtonClicked(transaction) {
      if (this.isEditing && this.transactionId === transaction.id) {
        this.isEditing = false
        this.transactionId = ''
        this.description = ''
        this.amount = ''
        this.date = ''
        return
      }
      this.isEditing = true
      this.transactionId = transaction.id
      this.description = transaction.description
      this.amount = transaction.amount
      this.selectedCategory = transaction.category
      this.date = this.formatDate(transaction.date)
    },
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('en-CA')
    }
  }
}
</script>

<style scoped>
h2,
h3 {
  text-align: center;
  margin: 20px;
}
.transaction-table {
  margin: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead th {
  background-color: #f4f4f4;
  padding: 10px;
  border: 1px solid #ddd;
}

thead th.category {
  width: 20%;
}

thead th.desc {
  width: 35%;
}

thead th.amount {
  width: 20%;
}

thead th.date {
  width: 25%;
}

tbody td {
  padding: 10px;
  border: 1px solid #ddd;
}

form {
  display: flex;
  justify-content: space-evenly;
  background: #ccd;
  padding: 20px;
}

form label {
  padding: 5px;
}

form input {
  padding: 5px;
  border: 1px solid #ddd;
}

form button {
  min-width: 150px;
  padding: 10px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

form button:hover {
  background-color: #3a8d7d;
}

.select-category {
  display: flex;
  align-items: center;
}

.custom-select-wrapper {
  position: relative;
  width: 100%;
}

.custom-select {
  width: 100%;
  padding-left: 10px;
  appearance: none; /* Remove native dropdown icon */
  -webkit-appearance: none;
  -moz-appearance: none;
  background: url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA0MCA0MCI+PHBvbHlnb24gcG9pbnRzPSIyMCAzMCAxMCAyMCAzMCAyMCIgZmlsbD0iI2NjYyIvPjwvc3ZnPg==')
    no-repeat right 10px center;
  background-color: white;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 16px;
  height: 45px;
}

/* Adjust padding to show custom dropdown arrow */
.custom-select:focus {
  outline: none;
  border-color: #5cb85c;
}

.edit-delete {
  display: flex;
  justify-content: space-evenly;
  padding: 5px;
}

.edit-button {
  width: 70px;
  color: green;
  transition: 0.3s;
}

.edit-button:hover {
  background: green;
  color: white;
}

.delete-button {
  width: 70px;
  color: red;
  transition: 0.3s;
}

.delete-button:hover {
  background: red;
  color: white;
}
</style>
