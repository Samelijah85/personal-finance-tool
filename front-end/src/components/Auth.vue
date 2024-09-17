<template>
  <div class="auth-container">
    <!-- Toggle between Login and Register forms based on authMode -->
    <div v-if="authMode === 'login'">
      <h2>Login</h2>
      <form class="auth-form" @submit.prevent="login">
        <input v-model="username" placeholder="Username" required />
        <input v-model="password" type="password" placeholder="Password" required />
        <button type="submit">Login</button>
      </form>
      <p>
        Don't have an account?
        <a href="#" @click="toggleAuthMode">Register</a>
      </p>
    </div>

    <div v-else-if="authMode === 'register'">
      <h2>Register</h2>
      <form class="auth-form" @submit.prevent="register">
        <input v-model="username" placeholder="Username" required />
        <input v-model="full_name" placeholder="Full name" />
        <input v-model="email" placeholder="Email" />
        <input v-model="password" type="password" placeholder="Password" required />
        <button type="submit">Register</button>
      </form>
      <p>
        Already have an account?
        <a href="#" @click="toggleAuthMode">Login</a>
      </p>
    </div>
  </div>
</template>

<script>
import axios from '@/axios'

export default {
  data() {
    return {
      authMode: 'login', // Track whether we are in 'login' or 'register' mode
      username: '',
      full_name: '',
      email: '',
      password: ''
    }
  },
  methods: {
    toggleAuthMode() {
      // Switch between login and register forms
      this.authMode = this.authMode === 'login' ? 'register' : 'login'
    },
    async login() {
      try {
        const params = new URLSearchParams()
        params.append('username', this.username)
        params.append('password', this.password)

        const response = await axios.post('/auth/login', params, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        })

        localStorage.setItem('token', response.data.access_token)
        this.$router.push('/transactions')
      } catch (error) {
        console.error(error.response.data)
      }
    },
    async register() {
      try {
        const response = await axios.post('/auth/register/', {
          username: this.username,
          password: this.password,
          email: this.email,
          full_name: this.full_name
        })

        localStorage.setItem('token', response.data.access_token)
        this.$router.push('/transactions')
      } catch (error) {
        console.error(error.response.data)
      }
    }
  }
}
</script>

<style scoped>
.auth-container {
  max-width: 400px;
  margin: 100px auto;
  padding: 20px;
  background-color: #f4f4f4;
  border-radius: 8px;
  text-align: center;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.auth-form input {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.auth-form button {
  padding: 10px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.auth-form button:hover {
  background-color: #3a8d7d;
}

a {
  color: #42b983;
  cursor: pointer;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
</style>
