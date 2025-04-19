<template>
  <div class="home-container">
    <!-- 顶部导航栏 -->
    <nav class="nav-bar glass-card">
      <div class="nav-content">
        <div class="nav-left">
          <router-link to="/" class="logo">
            <img src="@/assets/logo.svg" alt="Logo" class="logo-image">
            <span class="logo-text">图库</span>
          </router-link>
        </div>
        <div class="nav-right">
          <div v-if="isLoggedIn">
            <img :src="userAvatar" alt="头像" class="user-avatar">
            <span class="user-name">{{ userName }}</span>
            <button @click="handleUpload" class="nav-button">Upload</button>
          </div>
          <div v-else>
            <router-link to="/account/login" class="nav-button">登录</router-link>
            <router-link to="/account/register" class="nav-button primary">注册</router-link>
          </div>
        </div>
      </div>
    </nav>

    <!-- 主要内容区 -->
    <main class="main-content">
      <div class="upload-container glass-card">
        <h2>上传图片</h2>
        <form @submit.prevent="handleSubmit" class="upload-form">
          <!-- 图片上传区域 -->
          <div class="image-upload-area" @click="triggerFileInput" @drop.prevent="handleDrop" @dragover.prevent>
            <input type="file" ref="fileInput" @change="handleFileChange" accept="image/*" style="display: none">
            <div v-if="!previewImage" class="upload-placeholder">
              <i class="fas fa-cloud-upload-alt"></i>
              <p>点击或拖拽图片到此处上传</p>
              <p class="upload-hint">支持 JPEG、PNG 格式，最大 10MB</p>
            </div>
            <img v-else :src="previewImage" alt="预览图片" class="preview-image">
          </div>

          <!-- 图片信息表单 -->
          <div class="form-group">
            <label>飞机型号</label>
            <input type="text" v-model="formData.model" placeholder="请输入飞机型号" required>
          </div>

          <div class="form-group">
            <label>拍摄地点</label>
            <input type="text" v-model="formData.location" placeholder="请输入拍摄地点" required>
          </div>

          <div class="form-group">
            <label>拍摄时间</label>
            <input type="datetime-local" v-model="formData.shootTime" required>
          </div>

          <div class="form-group">
            <label>图片描述</label>
            <textarea v-model="formData.description" placeholder="请输入图片描述" rows="4"></textarea>
          </div>

          <!-- 分类建议 -->
          <div class="form-group" v-if="suggestedCategories.length">
            <label>推荐分类</label>
            <div class="category-suggestions">
              <button 
                v-for="category in suggestedCategories" 
                :key="category"
                type="button"
                :class="['category-tag', { active: formData.categories.includes(category) }]"
                @click="toggleCategory(category)"
              >
                {{ category }}
              </button>
            </div>
          </div>

          <!-- 上传进度 -->
          <div class="upload-progress" v-if="uploadProgress > 0 && uploadProgress < 100">
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: uploadProgress + '%' }"></div>
            </div>
            <span>{{ uploadProgress }}%</span>
          </div>

          <button type="submit" class="submit-button" :disabled="uploading">{{ uploading ? '上传中...' : '提交' }}</button>
        </form>
      </div>
    </main>

    <!-- 底部页脚 -->
    <footer class="footer glass-card">
      <div class="footer-content">
        <div class="footer-section">
          <a href="#" class="social-link">关于我们</a>
          <a href="#" class="social-link">使用条款</a>
          <a href="#" class="social-link">隐私政策</a>
        </div>
        <div class="footer-section">
          <span>© 2024 图库. All rights reserved.</span>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue';
import axios from 'axios';
import { useStore } from 'vuex';

const fileInput = ref(null);
const previewImage = ref('');
const uploadProgress = ref(0);
const uploading = ref(false);

const formData = reactive({
  model: '',
  location: '',
  shootTime: '',
  description: '',
  categories: []
});

const suggestedCategories = ref(['军用', '民用', '客机', '货机', '战斗机', '直升机']);

const triggerFileInput = () => {
  fileInput.value.click();
};

const handleFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    validateAndPreviewFile(file);
  }
};

const handleDrop = (event) => {
  const file = event.dataTransfer.files[0];
  if (file) {
    validateAndPreviewFile(file);
  }
};

const validateAndPreviewFile = (file) => {
  // 验证文件类型
  if (!['image/jpeg', 'image/png'].includes(file.type)) {
    alert('请上传 JPEG 或 PNG 格式的图片');
    return;
  }

  // 验证文件大小（10MB）
  if (file.size > 10 * 1024 * 1024) {
    alert('图片大小不能超过 10MB');
    return;
  }

  // 预览图片
  const reader = new FileReader();
  reader.onload = (e) => {
    previewImage.value = e.target.result;
  };
  reader.readAsDataURL(file);
};

const toggleCategory = (category) => {
  const index = formData.categories.indexOf(category);
  if (index === -1) {
    formData.categories.push(category);
  } else {
    formData.categories.splice(index, 1);
  }
};

const handleSubmit = async () => {
  uploading.value = true;
  // 模拟上传进度
  const interval = setInterval(() => {
    if (uploadProgress.value < 90) {
      uploadProgress.value += 10;
    }
  }, 500);

  try {
    // TODO: 实现实际的上传逻辑
    await new Promise(resolve => setTimeout(resolve, 3000));
    uploadProgress.value = 100;
    alert('上传成功！');
    // 重置表单
    formData.model = '';
    formData.location = '';
    formData.shootTime = '';
    formData.description = '';
    formData.categories = [];
    previewImage.value = '';
  } catch (error) {
    alert('上传失败，请重试');
  } finally {
    clearInterval(interval);
    uploading.value = false;
    uploadProgress.value = 0;
  }
};
// 使用计算属性来获取登录状态
const loggedIn = computed(() => isLoggedIn.value);

const handleUpload = () => {
  // 上传逻辑
};

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

const isLoggedIn = ref(false);
const userName = ref('');
const userAvatar = ref('');

onMounted(() => {
  const userCookie = getCookie('user-info');
  if (userCookie) {
    const userInfo = JSON.parse(userCookie);
    isLoggedIn.value = true;
    userName.value = userInfo.username;
    userAvatar.value = userInfo.userAvatar;
  }
});

const store = useStore();

const isLoggedInStore = computed(() => store.state.isLoggedIn);
const userNameStore = computed(() => store.state.userName);
const userAvatarStore = computed(() => store.state.userAvatar);

onMounted(() => {
  store.dispatch('initLoginState');
});


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
.main-content {
  max-width: 800px;
  margin: 2rem auto;
  padding: 0 2rem;
}

.upload-container {
  padding: 2rem;
}

.upload-container h2 {
  text-align: center;
  margin-bottom: 2rem;
  color: #262d91;
}

.upload-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.image-upload-area {
  border: 2px dashed rgba(38, 45, 145, 0.3);
  border-radius: 12px;
  padding: 2rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.image-upload-area:hover {
  border-color: rgba(38, 45, 145, 0.8);
}

.upload-placeholder {
  color: #666;
}

.upload-placeholder i {
  font-size: 3rem;
  margin-bottom: 1rem;
  color: #262d91;
}

.upload-hint {
  font-size: 0.875rem;
  color: #666;
  margin-top: 0.5rem;
}

.preview-image {
  max-width: 100%;
  max-height: 300px;
  border-radius: 8px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  color: #262d91;
  font-weight: 500;
}

.form-group input,
.form-group textarea {
  padding: 0.75rem;
  border-radius: 12px;
  border: none;
  background: rgba(255, 255, 255, 0.3);
  transition: all 0.3s ease;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(38, 45, 145, 0.3);
}

.category-suggestions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.category-tag {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  border: none;
  background: rgba(255, 255, 255, 0.3);
  color: #262d91;
  cursor: pointer;
  transition: all 0.3s ease;
}

.category-tag.active {
  background: rgba(38, 45, 145, 0.8);
  color: white;
}

.upload-progress {
  margin-top: 1rem;
}

.progress-bar {
  height: 8px;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: #262d91;
  transition: width 0.3s ease;
}

.submit-button {
  padding: 1rem;
  border-radius: 12px;
  border: none;
  background: rgba(38, 45, 145, 0.8);
  color: white;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.submit-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.submit-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* 页脚样式 */
.footer {
  padding: 2rem;
  margin-top: 4rem;
}

.footer-content {
  max-width: 1200px;
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

/* 玻璃卡片基础样式 */
.glass-card {
  background: rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(12px);
  border-radius: 24px;
  border: 1px solid rgba(255, 255, 255, 0.3);
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

  .footer-content {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
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

  .upload-container {
    padding: 1rem;
  }

  .form-group input,
  .form-group textarea {
    font-size: 16px; /* 防止iOS缩放 */
  }
}
</style>