<template>
  <nav class="nav-bar glass-card">
    <div class="nav-content">
      <div class="nav-left">
        <router-link to="/" class="logo">
          <img src="@/assets/logo.svg" alt="Logo" class="logo-image">
          <span class="logo-text">图库</span>
        </router-link>
        <div class="search-box">
          <input type="text" placeholder="搜索图片..." v-model="searchQuery">
          <button @click="search" class="search-button">
            <i class="fas fa-search"></i>
          </button>
        </div>
      </div>
      <div class="nav-right">
        <div v-if="isLoggedIn" class="user-info">
          <img :src="userAvatar || '/default-avatar.png'" alt="头像" class="user-avatar">
          <span class="user-name">{{ userName }}</span>
          <div class="dropdown-menu">
            <router-link to="/upload" class="dropdown-item">上传图片</router-link>
            <router-link to="/my-profile" class="dropdown-item">个人资料</router-link>
            <button @click="handleLogout" class="dropdown-item">退出登录</button>
          </div>
          <router-link to="/upload" class="nav-button">上传</router-link>
        </div>
        <div v-else>
          <router-link to="/account/login" class="nav-button">登录</router-link>
          <router-link to="/account/register" class="nav-button primary">注册</router-link>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

const store = useStore();
const router = useRouter();
const searchQuery = ref('');

// 使用计算属性获取 Vuex store 中的登录状态
const isLoggedIn = computed(() => store.state.isLoggedIn);
const userName = computed(() => store.state.userName);
const userAvatar = computed(() => store.state.userAvatar);

// 在组件挂载时初始化登录状态
onMounted(() => {
  store.dispatch('initLoginState');
});

// 搜索功能
const search = () => {
  if (searchQuery.value.trim() !== '') {
    // 执行搜索逻辑
    router.push({ 
      path: '/search', 
      query: { q: searchQuery.value }
    });
  }
};

// 处理登出
const handleLogout = async () => {
  try {
    // 可选：调用后端登出 API
    // await axios.post('/api/logout');
    
    // 清除本地登录状态
    store.dispatch('logout');
    
    // 重定向到首页
    router.push('/');
  } catch (error) {
    console.error('登出失败:', error);
  }
};
</script>

<style scoped>
.nav-bar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 70px;
  padding: 0 2rem;
  z-index: 1000;
}

.nav-content {
  max-width: 1200px;
  height: 100%;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-left {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
  color: #262d91;
}

.logo-image {
  height: 32px;
}

.logo-text {
  font-size: 1.5rem;
  font-weight: bold;
}

.search-box {
  position: relative;
  width: 300px;
}

.search-box input {
  width: 100%;
  padding: 0.5rem 2.5rem 0.5rem 1rem;
  border: none;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(5px);
}

.search-button {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  position: relative;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid rgba(255, 255, 255, 0.5);
  cursor: pointer;
}

.user-name {
  font-weight: 500;
  color: #262d91;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  padding: 0.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  min-width: 150px;
  display: none;
  z-index: 1000;
}

.user-info:hover .dropdown-menu {
  display: block;
}

.dropdown-item {
  display: block;
  padding: 0.75rem 1rem;
  color: #262d91;
  text-decoration: none;
  border-radius: 8px;
  transition: background 0.3s ease;
  text-align: left;
  border: none;
  background: none;
  width: 100%;
  font-size: 1rem;
  cursor: pointer;
}

.dropdown-item:hover {
  background: rgba(38, 45, 145, 0.1);
}

.nav-button {
  padding: 0.5rem 1.5rem;
  border-radius: 20px;
  text-decoration: none;
  color: #262d91;
  background: rgba(255, 255, 255, 0.3);
  transition: all 0.3s ease;
}

.nav-button.primary {
  background: rgba(38, 45, 145, 0.8);
  color: white;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .nav-content {
    flex-direction: column;
    gap: 1rem;
    padding: 1rem 0;
  }

  .nav-bar {
    height: auto;
  }

  .search-box {
    width: 100%;
  }
  
  .user-info {
    margin-top: 0.5rem;
  }
}

@media (max-width: 480px) {
  .nav-left {
    flex-direction: column;
    gap: 1rem;
    width: 100%;
  }

  .nav-right {
    width: 100%;
    justify-content: center;
  }
  
  .user-info {
    flex-direction: column;
  }
}
</style>