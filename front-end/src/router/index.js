import { createRouter, createWebHistory } from 'vue-router'
import Auth from '@/components/Auth.vue'
import Transactions from '@/components/Transactions.vue'
import Budgets from '@/components/Budgets.vue'
import Summary from '@/components/Summary.vue'

const routes = [
  { path: '/transactions', name: 'Transactions', component: Transactions },
  { path: '/budgets', name: 'Budgets', component: Budgets },
  { path: '/summary', name: 'Summary', component: Summary },
  { path: '/auth', name: 'Auth', component: Auth },
  { path: '/' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Global Navigation Guard
router.beforeEach((to, from, next) => {
  // Check if the user is logged in (i.e., if token exists)
  const isLoggedIn = !!localStorage.getItem('token')

  if (to.path === '/') {
    // If user is logged in, redirect to /transactions, otherwise to /auth
    if (isLoggedIn) {
      next('/transactions')
    } else {
      next('/auth')
    }
  } else {
    next() // Continue to the route
  }
})

export default router
