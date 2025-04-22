<template>
  <div class="home-container bg-gradient-to-r from-blue-500 to-purple-500">
    <!-- 顶部导航栏 -->
    <nav class="nav-bar ">
      <div class="nav-content">
        <div class="nav-left">
          <router-link to="/" class="logo">
            <img src="@/assets/logo.svg" alt="Logo" class="logo-image">
            <span class="logo-text" style="font-family: Maple Mono NF CN;">ByInfo - Fs Picture
              Archieve</span></router-link>

        </div>
        <div class="nav-right">
          <div v-if="isLoggedIn" class="user-info">
            <span class="user-name">{{ userName }}</span>
            <div class="dropdown-menu">
              <router-link to="/upload" class="dropdown-item">上传图片</router-link>
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
    <!-- 轮播图区域 -->
    <div class="carousel">
      <div v-for="(image, index) in featuredImages" :key="index" class="carousel-item">
        <img :src="image.url" :alt="image.title" class="carousel-image">
        <div class="carousel-info">
          <h3>{{ image.title }}</h3>
          <p>{{ image.description }}</p>
        </div>
      </div>
      <div class="carousel-indicators">
        <span v-for="(image, index) in featuredImages" :key="index" :class="{ 'active': currentSlide === index }"
          @click="goToSlide(index)"></span>
      </div>
    </div>
    <!-- 分类筛选区 -->
    <div class="filters">
      <button v-for="category in categories" :key="category"
        :class="['filter-button', { active: selectedCategory === category }]" @click="selectCategory(category)">
        {{ category }}
      </button>
    </div>
    <!-- 热门图片展示区 -->
    <div class="image-grid">
      <div v-for="image in images.data" :key="image.id" class="image-card">
        <img :src="'data:image/jpeg;base64,' + image.filedata" :alt="image.aircraft_model" class="grid-image">
        <div class="status-indicator" :style="{ backgroundColor: getStatusColor(image.rating) }" v-html="getStarDisplay(image.rating)">
        </div>
        <div class="image-info">
          <div class="image-meta">
            <span class="model">{{ image.reg_number + ' | ' + image.aircraft_model }}</span>
            <span class="airline">{{ image.airline || '' }}</span>

          </div>
          <div class="image-details" style=" color: #262d91;">
            <span class="photographer" style=" color: #262d91;">{{ image.username }}</span>
            <span class="photographer views" style=" color: #262d91;">
              <img src="@/assets/views.svg" alt="Views" class="views-icon"
                style="margin-top: 0.00788rem  ;margin-right: -0.06rem; " />
                &hairsp;
                {{ image.views || 'No' }}
              &nbsp;&nbsp;&thinsp;
              <img src="@/assets/likie.svg" alt="Likes" class="views-icon"
                style="margin-top: 0.00788rem ;margin-right: -0.06rem; height: 12px; width: 12px; " />
                &hairsp;
                {{ image.likes || 'No' }}
            </span>
          </div>
        </div>
      </div>
    </div>
    <!-- 底部页脚 -->
    <footer class="footer">
      <div class="footer-content">
        <div class="footer-section">
          <a href="#" class="social-link">关于我们</a>
          <a href="#" class="social-link">使用条款</a>
          <a href="#" class="social-link">隐私政策</a>
        </div>
        <div class="footer-section">
          <span>Copyright 2025 by TanQi. All rights reserved.</span>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, reactive } from 'vue';
// import { useStore } from 'vuex'; // Removed Vuex import
import { useRouter } from 'vue-router';

// const store = useStore(); // Removed store instance
const router = useRouter();
const searchQuery = ref('');

// Removed Vuex state dependencies
// const isLoggedIn = computed(() => store.state.isLoggedIn);
// const userName = computed(() => store.state.userName);
// const userAvatar = computed(() => store.state.userAvatar);
// const images = computed(() => store.state.images);

// Placeholder for login state (can be replaced with localStorage or other methods)
const isLoggedIn = ref(false); // Example: Default to false
const userName = ref(''); // Example: Default empty
const userAvatar = ref(''); // 初始为空
const featuredImages = ref([]); // 初始化为空数组


const images = ref([]); // Example: Default empty array

// Category logic
const categories = ['全部', '民航', '军用', '通用'];
const selectedCategory = ref('全部');



// Simplified onMounted - remove store actions
onMounted(async () => {
  isLoggedIn.value = localStorage.getItem('isLoggedIn') === 'true';
  userName.value = localStorage.getItem('userName') || '';
  try {
    const featuredResponse = await fetch('/api/featured-images');
    console.log('Featured Images Response:', featuredResponse);
    if (!featuredResponse.ok) throw new Error('Failed to fetch featured images');
    featuredImages.value = await featuredResponse.json();
    console.log('Featured Images Data:', featuredImages.value);

    const imagesResponse = await fetch('/api/images');
    console.log('Images Response:', imagesResponse);
    if (!imagesResponse.ok) throw new Error('Failed to fetch images');
    images.value = await imagesResponse.json();
    console.log('Images Data:', images.value);
    


  } catch (error) {
    console.error('Error fetching data:', error);
  }
});
const previewImage = ref('');
const uploadProgress = ref(0);
const uploading = ref(false);
const getStatusColor = (rating) => {
  switch (rating) {
    case '':
      return '#e74c3c';
    case 1 :
      return '#2ecc71';
    case 2:
      return '#2ecc71';
    case 3:
      return '#2ecc71';
    case '未知用途':
      return '#2ecc71';
    default:
      return '#e74c3c'; // 默认颜色
  }
};

const getStarDisplay = (rating) => {
  switch (rating) {
    case 1:
      return '&emsp;★&emsp;';
    case 2:
      return '&ensp;★★&ensp;';
    case 3:
      return '★★★';
    default:
      return '未审核'; // 默认无星星
  }
};
const formData = reactive({
  model: '',
  location: '',
  shootTime: '',
  description: '',
  categories: []
});

// 搜索功能 (kept)
const search = () => {
  if (searchQuery.value.trim() !== '') {
    router.push({
      path: '/search',
      query: { q: searchQuery.value }
    });
  }
};

const handleLogout = async () => {
  try {
    // Clear all auth related local storage
    localStorage.removeItem('isLoggedIn');
    localStorage.removeItem('userName');
    localStorage.removeItem('token');
    isLoggedIn.value = false;
    userName.value = '';
    // Redirect
    router.push('/');
  } catch (error) {
    console.error('登出失败:', error);
  }
};
// Add this with your other ref declarations
const currentSlide = ref(0);

// Add this function to handle slide navigation
const goToSlide = (index) => {
  currentSlide.value = index;
};
// Example function to fetch images without Vuex (if needed)
// async function fetchImages() {
//   try {
//     const response = await fetch('/api/images'); // Adjust API endpoint
//     if (!response.ok) throw new Error('Network response was not ok');
//     images.value = await response.json();
//   } catch (error) {
//     console.error('Failed to fetch images:', error);
//     images.value = []; // Reset or handle error
//   }
// }
// Add this function
const likeImage = async (imageId) => {
  try {
    // Implement like functionality here
    console.log('Liking image with ID:', imageId);
    // You can add API call here when you implement the backend
  } catch (error) {
    console.error('Error liking image:', error);
  }
};
</script>


<style scoped>
.home-container {
  min-height: 1000vh;
  background: linear-gradient(200deg, #e2e9f3 0%, #c3cfe2 100%);
  padding-top: 50px;
}

/* 导航栏样式 */
.nav-bar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 70px;
  padding: 0 rem;
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
  max-width: 1750px;
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
  max-width: 1750px;
  margin-left: 398px;
  margin-right: 398px;
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
  margin-top: -0.5rem;
  margin-bottom: 0.5rem;
  margin-left: 0.3rem;
  margin-right: 0.3rem;
}
.status-indicator {
  position: absolute;
  top: 10px;
  right: 10px;
  color: white;
  padding: 4px 9px;
  border-radius: 20px;
  font-size: 0.875rem;
  font-size: 13px;
}
.image-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
}

.image-details {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.875rem;
}

.like-button {
  background: none;
  border: none;
  cursor: pointer;
  color: #262d91;
  display: flex;
  align-items: center;
}

.like-button i {
  margin-right: 0.5rem;
}

.image-info h3 {
  margin: 0;
  color: #262d91;
}

.image-info p {
  margin: 0.5rem 0 0;
  color: #666;
}

.views-icon {
  width: 14px;
  height: 14px;
  vertical-align: middle;
  margin-right: 4px;
  filter: invert(24%) sepia(100%) saturate(1000%) hue-rotate(180deg) brightness(55%) contrast(190%);
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
  padding: 10px;
  /* 增加padding以扩大悬停区域 */
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
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.7));
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

.views {
  display: flex;
  justify-content: flex-end;
  align-items: center;
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
