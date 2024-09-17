<template>
  <div>
    <h2>Login</h2>
    <form @submit.prevent="login">
      <input v-model="username" placeholder="Username" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <button type="submit">Login</button>
    </form>
  </div>
</template>

<script>
import axios from '@/axios'

export default {
  data() {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
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
    }
  }
}
</script>
