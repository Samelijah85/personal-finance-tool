<template>
  <div id="app">
    <nav>
      <router-link v-if="!isLoggedIn" to="/login">Login</router-link> |
      <router-link v-if="!isLoggedIn" to="/register">Register</router-link> |
      <router-link to="/transactions">Transactions</router-link> |
      <router-link to="/budgets">Budgets</router-link> |
      <router-link to="/summary">Summary</router-link> |
      <button v-if="isLoggedIn" @click="logout">Logout</button>
    </nav>

    <router-view />
  </div>
</template>

<script>
export default {
  data() {
    return {
      // Track authentication state in a reactive way
      isLoggedIn: !!localStorage.getItem('token')
    }
  },
  mounted() {
    // Listen for login/logout events to dynamically update isLoggedIn
    window.addEventListener('storage', this.syncAuthState)
  },
  beforeUnmount() {
    // Clean up event listener to prevent memory leaks
    window.removeEventListener('storage', this.syncAuthState)
  },
  methods: {
    syncAuthState() {
      // Update the isLoggedIn state when changes happen in localStorage
      this.isLoggedIn = !!localStorage.getItem('token')
    },
    logout() {
      // Clear the token from localStorage and redirect to the login page
      localStorage.removeItem('token')
      this.isLoggedIn = false
      this.$router.push('/login')
    }
  }
}
</script>

<style>
/* Add some basic styling */
nav {
  padding: 10px;
  background-color: #f4f4f4;
  margin-bottom: 20px;
}

nav a {
  margin-right: 10px;
  text-decoration: none;
  color: #42b983;
}

button {
  background-color: #42b983;
  color: white;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
}

button:hover {
  background-color: #3a8d7d;
}
</style>
