<template>
  <div class="home-container bg-gradient-to-r from-blue-500 to-purple-500">
    <!-- 顶部导航栏 -->
    <nav class="nav-bar">
      <div class="nav-content">
        <div class="nav-left">
          <router-link to="/" class="logo">
            <img src="@/assets/logo.svg" alt="Logo" class="logo-image">
            <span class="logo-text">ByInfo - Fs Picture Archieve</span>
          </router-link>
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
    <!-- 主要内容区 -->
    <main class="main-content hgs-container">
      <div class="notice-container glass-card" style="width: 50%; margin-right: 1%;">
        <h1>项目上传须知</h1>
        <p>为了打造一个优质的原创平台，在上传图片时，您需要仔细阅读并遵守以下要求：</p>
        <ul style="font-family: hermit;font-size: 16px;line-height: 50px">
          <li>
            <strong>格式要求</strong>：仅接受 JPG/JPEG 格式图片，其他格式无法识别，请提前完成格式转环换。
          </li>
          <li>
            <strong>大小限制</strong>：单张图片文件大小不得超过 300MB，过大的文件会上传失败，请提前压缩处理。
          </li>
          <li>
            <strong>内容规范</strong>：请勿上传带有明显人脸的照片，以及包含网络梗图的内容。
          </li>
          <li>
            <strong>权益保护</strong>：您上传的图片须确保不侵犯任何个人、组织、企业等主体的合法权益，包括但不限于肖像权、著作权、商标权等。
          </li>
          <li>
            <strong>原创声明</strong>：所有上传图片必须为本人原创拍摄，请勿上传非本人拍摄的图片，禁止任何形式的抄袭。
          </li>
          <li>
            <strong>信息完整性</strong>：若图片涉及特定对象或场景，相关机型、编号、主体名称等信息缺失时，统一标注 “N/A”。
          </li>
          <li>
            <strong>内容合规</strong>：上传内容需严格遵守国家法律法规及平台规定，禁止包含政治敏感、虚假、侮辱、诽谤等违规信息。
          </li>
        </ul>
      </div>
      <div class=" upload-container glass-card">
        <h2>上传图片</h2>
        <form @submit.prevent="handleSubmit" class="upload-form">
          <!-- 图片上传区域 -->
          <div class="image-upload-area" @click="triggerFileInput" @drop.prevent="handleDrop" @dragover.prevent>
            <input type="file" ref="fileInput" @change="handleFileChange" accept="image/*" style="display: none">
            <div v-if="!previewImage" class="upload-placeholder">
              <i class="fas fa-cloud-upload-alt"></i>
              <p>点击或拖拽图片到此处上传</p>
              <p class="upload-hint">支持 JPEG、JPG 格式，最大 300MB</p>
            </div>
            <img v-else :src="previewImage" alt="预览图片" class="preview-image">
          </div>

          <!-- 图片信息表单 -->

          <div class="info-section upload-container glass-card">
            <h3>飞机信息</h3>
            <div class="form-group">
              <label>航班号</label>
              <input type="text" v-model="formData.flightNumber" placeholder="e.g. HU7051 / MU501" required>
            </div>
            <div class="form-group">
              <label>注册号</label>
              <input type="text" v-model="formData.registrationNumber" placeholder="e.g. B-2447 / JA383A" required>
            </div>
            <div class="form-group">
              <label>飞机型号</label>
              <input type="text" v-model="formData.model" placeholder="e.g. Airbus A320-251N / Boeing 787-8" required>
            </div>
            <div class="form-group">
              <label>航司</label>
              <v-select v-model="formData.airlineOperator" :options="airlineOptions" placeholder="请选择或输入航司" searchable
                :reduce="option => option || null" />
            </div>
          </div>

          <div class="upload-container glass-card " style="width: 86.3%;">
            <div class="photo-section">
              <h3>照片信息</h3>
              <div class="form-group">
                <label>拍摄时间</label>
                <input type="datetime-local" style="font-family: hermit;" v-model="formData.shootTime" required>
              </div>
              <div class="form-group">
                <label>拍摄地点</label>
                <input type="text" v-model="formData.location" placeholder="请输入拍摄地点" required>
              </div>
              <div class="form-group">
                <label>天气</label>
                <div class="category-suggestions">
                  <button v-for="condition in ['晴', '多云', '阴', '雨', '雪', '雾', '霾', '雹']" :key="condition" type="button"
                    :class="['category-tag', { active: formData.weatherConditions.includes(condition) }]"
                    @click="toggleWeatherCondition(condition)">
                    {{ condition }}
                  </button>
                </div>
              </div>
              <div class="form-group">
                <label>类型（可以留空）</label>
                <div class="category-suggestions">
                  <button v-for="type in ['机场', '驾驶舱', '艺术', '地服', '货运', '彩绘', '夜摄']" :key="type" type="button"
                    :class="['category-tag', { active: formData.imageTypes.includes(type) }]"
                    @click="toggleImageType(type)">
                    {{ type }}
                  </button>
                </div>
              </div>
            </div>
          </div>


          <div class="upload-container glass-card" style="grid-column: span 2;width: 92.5%; margin-left: -0.6%;">
            <h3>上传附加</h3>
            <div class="form-group">
              <label>图片描述</label>
              <textarea v-model="formData.description" rows="4" placeholder="可以填写表单未提及但值得说明的内容"
                style="resize: none;width: 97%;height: 100%;font-size: 15px;margin-left: -1%;font-family:hermit "></textarea>
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
  </div>
</template>

<script setup>
import { ref, computed, onMounted, reactive } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import vSelect from 'vue-select';
import 'vue-select/dist/vue-select.css';

const router = useRouter();
const searchQuery = ref('');
// Remove these unnecessary lines:
// const app = createApp(App);
// app.use(Antd);
// app.mount('#app');

// Removed Vuex state dependencies
// const isLoggedIn = computed(() => store.state.isLoggedIn);
// const userName = computed(() => store.state.userName);
// const userAvatar = computed(() => store.state.userAvatar);

// Placeholder for login state (can be replaced with localStorage or other methods)
const isLoggedIn = ref(false); // Example: Default to false
const userName = ref(''); // Example: Default empty


// Simplified onMounted - remove store actions
onMounted(() => {
  // store.dispatch('initLoginState'); // Removed store action
  // Check local storage for login state, for example
  isLoggedIn.value = localStorage.getItem('isLoggedIn') === 'true';
  userName.value = localStorage.getItem('userName') || '';

});
const fileInput = ref(null);
const previewImage = ref('');
const uploadProgress = ref(0);
const uploading = ref(false);



const airlineOptions = ref([
  { label: '中国南方航空', value: '中国南方航空' },
  { label: '厦门航空', value: '厦门航空' },
  { label: '中国国际航空', value: '中国国际航空' },
  { label: '海南航空', value: '海南航空' }
]);

const formData = reactive({
  model: '',
  location: '',
  shootTime: '',
  description: '',
  categories: [],
  // 新增字段
  registrationNumber: '',
  flightNumber: '',
  airlineOperator: '',
  imageTypes: [],
  weatherConditions: [],
  locationInfo: ''
});

const suggestedCategories = ref(['军用', '民用', '客机', '货机', '战斗机', '直升机']);

const triggerFileInput = () => {
  //限制input的文件类型
  fileInput.value.click();

};

// 添加一个变量来存储选中的文件
const selectedFile = ref(null);

const handleFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    selectedFile.value = file;
    validateAndPreviewFile(file);
  }
};

const handleDrop = (event) => {
  const file = event.dataTransfer.files[0];
  if (file) {
    selectedFile.value = file;
    validateAndPreviewFile(file);
  }
};

const validateAndPreviewFile = (file) => {
  // 验证文件类型
  if (!['image/jpeg'].includes(file.type)) {
    alert('请上传 JPEG 格式的图片');
    return;
  }

  // 验证文件大小（300MB）
  if (file.size > 300 * 1024 * 1024) {
    alert('图片大小不能超过 300MB');
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
  if (!selectedFile.value) {
    alert('请选择要上传的图片');
    return;
  }

  if (!formData.model || !formData.location || !formData.shootTime) {
    alert('请填写完整的图片信息');
    return;
  }

  if (!isLoggedIn.value) {
    alert('请先登录再上传图片');
    router.push('/account/login');
    return;
  }

  if (!localStorage.getItem('token')) {
    alert('登录状态已过期，请重新登录');
    router.push('/account/login');
    return;
  }

  uploading.value = true;
  uploadProgress.value = 0;

  const uploadData = new FormData();
  uploadData.append('image', selectedFile.value);
  uploadData.append('model', formData.model);
  uploadData.append('location', formData.location);
  uploadData.append('shootTime', formData.shootTime);
  uploadData.append('description', formData.description);
  uploadData.append('categories', JSON.stringify(formData.categories));

  try {
    const response = await axios.post('/api/upload', uploadData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      onUploadProgress: (progressEvent) => {
        uploadProgress.value = Math.round((progressEvent.loaded * 100) / progressEvent.total);
      }
    });

    if (response.status === 200 || response.status === 201) {
      alert('上传成功！');
      formData.model = '';
      formData.location = '';
      formData.shootTime = '';
      formData.description = '';
      formData.categories = [];
      previewImage.value = '';
      selectedFile.value = null;
      fileInput.value.value = '';
      router.push('/');
    } else {
      throw new Error(response.data.message || '上传失败');
    }
  } catch (error) {
    console.error('上传失败:', error);
    alert(`上传失败: ${error.response?.data?.message || error.message || '请重试'}`);
  } finally {
    uploading.value = false;
    uploadProgress.value = 0;
  }
};

// Simplified logout - remove store action
const handleLogout = async () => {
  try {
    // Clear all authentication related data
    localStorage.removeItem('isLoggedIn');
    localStorage.removeItem('userName');
    localStorage.removeItem('token');

    // Reset state
    isLoggedIn.value = false;
    userName.value = '';

    // Redirect to home
    router.push('/');
  } catch (error) {
    console.error('登出操作失败:', error);
    // Ensure redirect even if error occurs
    router.push('/');
  }
};


// Define toggleImageType and toggleWeatherCondition methods
const toggleImageType = (type) => {
  const index = formData.imageTypes.indexOf(type);
  if (index === -1) {
    formData.imageTypes.push(type);
  } else {
    formData.imageTypes.splice(index, 1);
  }
};

const toggleWeatherCondition = (condition) => {
  const index = formData.weatherConditions.indexOf(condition);
  if (index === -1) {
    formData.weatherConditions.push(condition);
  } else {
    formData.weatherConditions.splice(index, 1);
  }
};

</script>


<style scoped>
.home-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding-top: 80px;
  padding-left: 1rem;
  /* 减少左边距 */
  padding-right: 1rem;
  /* 减少右边距 */
}

.my-v-select {
  z-index: 9990 !important;
  /* 设置一个较大的值，确保在其他元素之上 */
}

.my-v-select.v-select__dropdown {
  z-index: 9991 !important;
  /* 确保下拉菜单也在顶层 */
}

.hgs-container {
  display: grid;
  grid-template-columns: 1fr;
}

.form-group {
  position: relative;
  /* 确保子元素的 z - index 能正常生效 */
  z-index: 1;
  /* 若值过大可能会导致子元素被限制在一定层级内 */
  margin-bottom: 1rem;

}


label {
  display: block;
  margin-bottom: 0.5rem;
}

.v-select {
  width: 100%;
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
  max-width: 1750px;
  padding: 0.2rem;
  margin: 0 auto;
  display: flex;
  /*左右布局*/
  justify-content: center;
  /*内容居中*/
  gap: 2rem;
  height: 100%;
  width: 100%;
}



.upload-container {
  width: 82%;
  z-index: 10;
  /* 设置宽度为100%以确保两个框等宽 */
}

.upload-container h2 {
  text-align: center;
  margin-bottom: 2rem;
  color: #262d91;
}

.notice-container {
  width: 120%;
  /* 设置宽度为100%以确保两个框等宽 */
}

.upload-form {
  display: grid;
  grid-template-columns: 1fr 1.5fr;
  gap: 1rem;
}

.image-upload-area,
.submit-button {
  grid-column: span 2;
}

.form-group {
  margin-bottom: 1rem;
  gap: 0.5rem;
}

.form-group input,
.form-group textarea {
  width: 93.5%;
  padding: 0.75rem;
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.3);
  color: #2c3e50;
  font-size: 0.95rem;
  transition: all 0.3s ease;
  gap: 15rem;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: rgba(0, 122, 255, 0.5);
  box-shadow: 0 0 0 3px rgba(0, 122, 255, 0.1);
  gap: 15rem;
}

.submit-button {
  width: 100%;
  padding: 0.75rem;
  border: none;
  border-radius: 12px;
  background: rgba(38, 45, 145, 0.8);
  color: white;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.submit-button:hover {
  background: rgba(38, 45, 145, 0.9);
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.submit-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
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

.auth-container {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.auth-wrapper {
  display: flex;
  justify-content: center;
  width: 100%;
  max-width: 520px;
  padding: 2rem;
}

.glass-card {
  background: rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(12px);
  border-radius: 24px;
  padding: 2.5rem;
  margin: 0 auto;
  z-index: 11;
}

.glass-card h2 {
  text-align: center;
  margin-bottom: 1.5rem;
  color: #2c3e50;
  font-weight: 500;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.auth-form input {
  width: 93.5%;
  padding: 0.75rem;
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.3);
  color: #2c3e50;
  font-size: 0.95rem;
  transition: all 0.3s ease;
}

.auth-form input:focus {
  outline: none;
  border-color: rgba(0, 122, 255, 0.5);
  box-shadow: 0 0 0 3px rgba(0, 122, 255, 0.1);
}

.primary-button {
  width: 100%;
  padding: 0.75rem;
  border: none;
  border-radius: 12px;
  min-width: 150px;
  z-index: 1000;



  background: rgba(38, 45, 145, 0.8);
  color: white;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 0.5rem;
}

.primary-button:hover {
  background: rgba(38, 45, 145, 0.9);
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

@media (max-width: 768px) {
  .glass-card {
    padding: 1.5rem;
    border-radius: 20px;
  }

  .glass-card h2 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
  }
}

@media (max-width: 480px) {
  .glass-card {
    padding: 1.25rem;
    border-radius: 16px;
  }

  .auth-form input,
  .primary-button {
    padding: 0.65rem;
  }
}


.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  position: relative;
  padding: 10px;
  /* 增加padding以扩大悬停区域 */
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

.dropdown-item button {
  width: auto;
}

.dropdown-item button:hover {
  background: rgba(38, 45, 145, 0.1);
  width: auto;
}

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
    font-size: 16px;
  }
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  position: relative;
}

.user-name {
  font-weight: 500;
  color: #262d91;
}
</style>
