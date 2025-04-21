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
      <div class="profile-header glass-card">
        <img :src="userAvatar" alt="Avatar" class="avatar">
        <div class="user-info">
          <h2>{{ userName }}</h2>
          <button @click="editInfo" class="primary-button">编辑信息</button>
        </div>
      </div>
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

.logo-image {
  width: 50px; /* 调整宽度 */
  height: auto; /* 自动调整高度以保持比例 */
}

.profile-header {
  display: flex;
  align-items: center;
  padding: 20px;
}

.avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  margin-right: 20px;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.profile-content {
  display: flex;
  justify-content: space-between;
  padding: 20px;
}

.image-card {
  width: 150px;
  height: 150px;
  overflow: hidden;
  border-radius: 8px;
  margin: 10px;
}

.grid-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>