<template>
  <div class="home-container bg-gradient-to-r from-blue-500 to-purple-500">
    <!-- 顶部导航栏 -->
    <nav class="nav-bar">
      <div class="nav-content">
        <div class="nav-left">
          <router-link to="/" class="logo">
            <img src="@/assets/logo.svg" alt="Logo" class="logo-image">
            <span class="logo-text" style="font-family: Maple Mono NF CN;">ByInfo - Fs Picture Archieve</span>
          </router-link>
        </div>
        <div class="nav-right">
          <div v-if="isLoggedIn" class="user-info">
            <span class="user-name">{{ userName }}</span>
            <div class="dropdown-menu">
              <router-link to="/upload" class="dropdown-item">上传照片</router-link>
              <router-link to="/my-profile" class="dropdown-item">个人资料</router-link>
              <button @click="handleLogout" class="dropdown-item logout-button">退出登录</button>
            </div>
          </div>
          <div v-else>
            <router-link to="/account/login" class="nav-button">登录</router-link>
            <router-link to="/account/register" class="nav-button primary">注册</router-link>
          </div>
        </div>
      </div>
    </nav>
    <!-- 主要内容区 -->
    <main class="main-content hgs-container">

      <div class="profile-content glass-card">
        <div class="reviewed-images">
          <h3>已审核的图片</h3>
          <div v-for="image in reviewedImages" :key="image.id" class="image-card">
            <img :src="image.url" alt="Reviewed Image" class="grid-image">
          </div>
          
        </div>
        <div class="pending-images">
          <h3>待审核的图片</h3>
          <div v-for="image in pendingImages" :key="image.id" class="image-card">
            <img :src="image.url" alt="Pending Image" class="grid-image">
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const userName = ref('');
const userAvatar = ref('');
const reviewedImages = ref([]);
const pendingImages = ref([]);
const isLoggedIn = ref(false);

onMounted(async () => {
  // 从 localStorage 或 API 获取用户信息
  userName.value = localStorage.getItem('userName') || '';
  userAvatar.value = localStorage.getItem('userAvatar') || '';
  isLoggedIn.value = localStorage.getItem('isLoggedIn') === 'true';

  // 从 API 获取已审核和待审核的图片
  const reviewedResponse = await fetch('/api/reviewed-images');
  reviewedImages.value = await reviewedResponse.json();

  const pendingResponse = await fetch('/api/pending-images');
  pendingImages.value = await pendingResponse.json();
});

const editInfo = () => {
  // 编辑用户信息的逻辑
  alert('编辑信息功能尚未实现');
};

const handleLogout = async () => {
  try {
    localStorage.removeItem('isLoggedIn');
    localStorage.removeItem('userName');
    localStorage.removeItem('token');
    isLoggedIn.value = false;
    userName.value = '';
    router.push('/');
  } catch (error) {
    console.error('登出操作失败:', error);
    router.push('/');
  }
};
</script>

<style scoped>
.home-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding-top: 80px;
}

/* 导航栏样式 */
.nav-bar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 70px;
  padding: 0 2rem;
  z-index: 1000;
  backdrop-filter: blur(12px);
}

.nav-content {
  max-width: 1750px;
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
  gap: 1rem;
}

.nav-button {
  padding: 0.5rem 1.5rem;
  border-radius: 20px;
  text-decoration: none;
  color: #262d91;
  transition: all 0.3s ease;
}

.nav-button.primary {
  background: rgba(38, 45, 145, 0.8);
  color: white;
}

/* 主要内容区样式 */
.nav-content {
  max-width:1750px;
  height: 100%;
  margin: 0 auto;
}

.filters {
  padding: 1rem;
  margin-bottom: 2rem;
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.filter-button {
  padding: 0.5rem 1.5rem;
  border: none;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.2);
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-button.active {
  background: rgba(38, 45, 145, 0.8);
  color: white;
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

.image-card {
  overflow: hidden;
  transition: transform 0.3s ease;
}

.image-card:hover {
  transform: translateY(-5px);
}

.grid-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.image-info {
  padding: 1rem;
}

.image-info h3 {
  margin: 0;
  color: #262d91;
}

.image-info p {
  margin: 0.5rem 0 0;
  color: #666;
}

/* 页脚样式 */
.footer {
  padding: 2rem;
  margin-top: 4rem;
}

.footer-content {
  max-width: 1750px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.footer-section {
  display: flex;
  gap: 1.5rem;
}

.social-link {
  color: #262d91;
  text-decoration: none;
  transition: all 0.3s ease;
}

.social-link:hover {
  opacity: 0.8;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  position: relative;
  padding: 10px; /* 增加padding以扩大悬停区域 */
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
  top: 20px;
  right: 0;
  transform: translateX(3%);
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  padding: 0.45rem;
  box-shadow: 3px 4px 12px rgba(0, 0, 0, 0.1);
  min-width: 150px;
  display: none;
  z-index: 1000;
  margin-top: 25px;
  transition: opacity 0.3s ease;
  opacity: 10;
}

.user-info:hover .dropdown-menu {
  display: block;
  opacity: 10;
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
  font-size: 1rem;
  cursor: pointer;
}

.dropdown-item:hover {
  background: rgba(38, 45, 145, 0.1);
}


.logout-button {
  display: block;
  padding: 0.75rem 1rem;
  color: #262d91;
  text-decoration: none;
  border-radius: 8px;
  transition: background 0.3s ease;
  text-align: left;
  border: none;
  background: none;
  font-size: 1rem;
  cursor: pointer;
  width: 100%;
}
.featured-section {
  margin-bottom: 2rem;
}

.section-title {
  font-size: 1.5rem;
  color: #262d91;
  margin-bottom: 1rem;
}

.featured-image {
  position: relative;
  height: 500px;
  overflow: hidden;
  border-radius: 12px;
}

.main-featured-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-info-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 2rem;
  background: linear-gradient(transparent, rgba(0,0,0,0.7));
  color: white;
}

.latest-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}

.image-card {
  position: relative;
  overflow: hidden;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.1);
  transition: transform 0.3s ease;
}

.image-card:hover {
  transform: translateY(-5px);
}

.grid-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.image-info {
  padding: 0.75rem;
}

.image-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.875rem;
  margin-top: 0.5rem;
}

.stats {
  display: flex;
  gap: 1rem;
}

.photographer {
  color: #666;
}

@media (max-width: 1024px) {
  .latest-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .latest-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .latest-grid {
    grid-template-columns: 1fr;
  }
}
</style>