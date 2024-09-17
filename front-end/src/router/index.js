import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/components/Login.vue'
import Register from '@/components/Register.vue'
import Transactions from '@/components/Transactions.vue'
import Budgets from '@/components/Budgets.vue'
import Summary from '@/components/Summary.vue'

const routes = [
  { path: '/login', name: 'Login', component: Login },
  { path: '/register', name: 'Register', component: Register },
  { path: '/transactions', name: 'Transactions', component: Transactions },
  { path: '/budgets', name: 'Budgets', component: Budgets },
  { path: '/summary', name: 'Summary', component: Summary }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
