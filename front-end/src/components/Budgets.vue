<template>
  <div>
    <h2>Budgets</h2>
    <div class="add-new-budget">
      <form @submit.prevent="handleSubmit">
        <input v-model="description" placeholder="Description" required />
        <input v-model="amount" type="number" step="0.01" placeholder="Amount" required />
        <div class="to-from">
          <label for="start_date">From: </label>
          <input v-model="startDate" type="date" required id="start_date" />
        </div>
        <div class="to-from">
          <label for="end_date">To: </label>
          <input v-model="endDate" type="date" required id="end_date" />
        </div>
        <button type="submit">{{ isEditing ? 'Save Budget' : 'Add Budget' }}</button>
      </form>
    </div>
    <h3>All Budgets</h3>
    <div class="budget">
      <div class="all-budgets">
        <div v-for="(budget, index) in budgets" :key="index">
          {{ index + 1 }}
          <div>
            <div @click="getFullBudget(budget.id)" class="desc-amount" role="button" tabindex="0">
              <h4>{{ budget.description }}</h4>
              <p>
                Amount: <b>${{ budget.limit_amount.toFixed(2) }}</b>
              </p>
            </div>
            <div class="period-ed">
              <span
                >From <i>{{ formatDate(budget.start_date) }}</i> to
                <i>{{ formatDate(budget.end_date) }}</i></span
              >
              <div class="edit-delete">
                <button @click="editButtonClicked(budget)" class="edit-button">
                  {{ isEditing && budgetId === budget.id ? 'Cancel' : 'Edit' }}
                </button>
                <button @click="deleteBudget(budget.id)" class="delete-button">Delete</button>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-if="fullBudget.isFetched" class="budget-breakdown">
        <h3>{{ fullBudget.budget.description }}</h3>
        <div class="breakdown">
          <p>Limit:</p>
          <p>${{ fullBudget.breakdown.limit_amount.toFixed(2) }}</p>
        </div>
        <div class="breakdown">
          <p>Used:</p>
          <p>${{ fullBudget.breakdown.used_amount.toFixed(2) }}</p>
        </div>
        <div class="breakdown">
          <p>Remaining:</p>
          <p>${{ fullBudget.breakdown.balance.toFixed(2) }}</p>
        </div>
        <div class="breakdown">
          <p>Usage percent:</p>
          <p>{{ fullBudget.breakdown.percentage }}%</p>
        </div>
      </div>
      <p v-else class="loading-data">{{ fullBudget.message }}</p>
    </div>
  </div>
</template>

<script>
import axios from '@/axios'

export default {
  data() {
    return {
      budgets: [],
      description: '',
      amount: '',
      startDate: '',
      endDate: '',
      amountSpent: {},
      isEditing: false,
      budgetId: '',
      fullBudget: {
        isFetched: false,
        message: 'No data to display',
        breakdown: {},
        budget: {}
      }
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
      try {
        await axios.post('/budgets/', {
          description: this.description,
          limit_amount: this.amount,
          start_date: this.startDate,
          end_date: this.endDate
        })
        this.fetchBudgets()
      } catch (error) {
        console.error(error)
      }
      this.description = ''
      this.amount = ''
      this.startDate = ''
      this.endDate = ''
    },

    async deleteBudget(id) {
      try {
        await axios.delete(`/budgets/${id}`)
        this.fetchBudgets()
      } catch (error) {
        console.error(error)
      }
    },

    async editBudget(id) {
      try {
        await axios.put(`/budgets/${id}`, {
          description: this.description,
          limit_amount: this.amount,
          start_date: this.startDate,
          end_date: this.endDate
        })
        this.fetchBudgets()
      } catch (error) {
        console.error(error)
      }
      this.description = ''
      this.amount = ''
      this.startDate = ''
      this.endDate = ''
      this.budgetId = ''
      this.isEditing = false
    },

    async getFullBudget(id) {
      if (id === this.fullBudget.budget.id) {
        return
      }
      this.fullBudget.isFetched = false
      this.fullBudget.message = 'Fetching details...'
      try {
        const response = await axios.get(`/budgets/${id}`)
        const budget = response.data
        this.fullBudget.breakdown = budget.breakdown
        this.fullBudget.budget = budget.budget
        this.fullBudget.isFetched = true
      } catch (error) {
        console.error(error)
      }
    },
    async handleSubmit() {
      if (this.isEditing) {
        await this.editBudget(this.budgetId)
      } else {
        await this.addBudget()
      }
    },
    editButtonClicked(budget) {
      if (this.isEditing && this.budgetId === budget.id) {
        this.isEditing = false
        this.budgetId = ''
        this.description = ''
        this.amount = ''
        this.startDate = ''
        this.endDate = ''
        return
      }
      this.isEditing = true
      this.budgetId = budget.id
      this.description = budget.description
      this.amount = budget.limit_amount
      this.startDate = this.formatDate(budget.start_date)
      this.endDate = this.formatDate(budget.end_date)
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

form {
  display: flex;
  justify-content: space-evenly;
  background: #ccd;
  padding: 20px;
}

form label {
  padding: 5px;
}

input {
  padding: 5px;
  border: 1px solid #ddd;
  height: 45px;
}

form button {
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
}

.all-budgets {
  display: flex;
  justify-content: space-between;
  padding: 10px;
  border: 1px solid #ddd;
  margin: 10px;
  width: 60%;
  flex-direction: column;
}

.all-budgets div {
  padding: 10px;
  border: 1px solid #ddd;
}

.desc-amount,
.period-ed {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.edit-button {
  color: green;
  transition: 0.3s;
}

.edit-button:hover {
  background: green;
  color: white;
}

.delete-button {
  color: red;
  transition: 0.3s;
}

.delete-button:hover {
  background: red;
  color: white;
}

div .budget {
  display: flex;
}

.budget-breakdown {
  display: flex;
  flex-direction: column;
  justify-content: center;
  width: 40%;
  padding: 30px;
}

.budget-breakdown .breakdown {
  display: flex;
  justify-content: space-between;
  max-width: 500px;
}

.budget-breakdown .breakdown p {
  font-size: 1.4rem;
}

.loading-data {
  width: 40%;
  text-align: center;
  font-size: 1.5rem;
}

.desc-amount {
  cursor: pointer;
  background-color: white;
  color: #007bff;
  transition: background-color 0.3s ease;
}

.desc-amount:hover {
  background-color: #0056b3;
  color: white;
}

.desc-amount:active {
  background-color: #004080;
}
</style>
