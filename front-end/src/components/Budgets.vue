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
    <div>
      <div v-for="(budget, index) in budgets" :key="index" class="all-budgets">
        <div>
          <div class="desc-amount">
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
      budgetId: ''
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

    async getAmountSpent(id) {
      try {
        const response = await axios.get(`/budgets/${id}`)
        this.amountSpent[id] = response.data.breakdown.used_amount
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
  flex-direction: column;
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
</style>
