import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/HomePage.vue'
import Login from '../components/login.vue'
import Register from '../components/register.vue'
import Upload from '../components/UploadPage.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/account/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/account/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/upload',
    name: 'Upload',
    component: Upload
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router