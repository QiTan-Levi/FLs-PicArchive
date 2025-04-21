import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/HomePage.vue'
import Login from '../components/login.vue'
import Register from '../components/register.vue'
import Upload from '../components/UploadPage.vue'
import Profile from '../components/ProfilePage.vue'

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
    component: Upload,
    meta: { requiresAuth: true } // 这个路由需要认证

  },
  {
    path: '/my-profile',
    name: 'Profile',
    component: Profile,
    meta: { requiresAuth: true }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
})


// 路由守卫
router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // 检查用户是否登录
    if (!localStorage.getItem('token')) {
      next({
        path: '/account/login',
        query: { redirect: to.fullPath }
      })
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router