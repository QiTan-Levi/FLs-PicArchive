<template>
  <div class="auth-container">
    <div class="notification-bar" :class="{ show: showNotification }">
      <span class="notification-icon">⚠️</span>
      {{ notificationMessage }}
    </div>
    
    <div class="auth-wrapper">
      <div class="glass-card">
        <div class="logo-area">
          <img src="/vite.svg" alt="系统Logo">
        </div>
        <h2>登录ByInfo ID</h2>
        
        <div class="login-method-tabs">
          <button 
            :class="{ active: loginMethod === 'password' }"
            @click="loginMethod = 'password'">
            密码登录
          </button>
          <button 
            :class="{ active: loginMethod === 'code' }"
            @click="loginMethod = 'code'">
            验证码登录
          </button>
        </div>
        
        <form @submit.prevent="login" class="auth-form" novalidate>
          <template v-if="loginMethod === 'password'">
            <input v-model="username" type="text" placeholder="用户名或邮箱" required />
            <input v-model="password" type="password" placeholder="密码" required />
          </template>
          
          <template v-else>
            <input v-model="email" type="email" placeholder="邮箱" required />
            <div class="code-input-group">
              <input v-model="verificationCode" type="text" placeholder="验证码" required />
              <button 
                type="button" 
                class="send-code-btn"
                @click="sendLoginCode"
                :disabled="isSendingCode">
                {{ isSendingCode ? `${countdown}秒后重试` : '获取验证码' }}
              </button>
            </div>
          </template>
          
          <button type="submit" class="primary-button">登录</button>
        </form>
        
        <div class="auth-footer">
          <span>没有账号？</span>
          <router-link to="/account/register">立即注册</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';

const router = useRouter();
const store = useStore();
const username = ref('');
const password = ref('');
const email = ref('');
const verificationCode = ref('');
const loginMethod = ref('password');
const isSendingCode = ref(false);
const countdown = ref(0);

const showNotification = ref(false);
const notificationMessage = ref('');

const showError = (message) => {
  notificationMessage.value = message;
  showNotification.value = true;
  setTimeout(() => {
    showNotification.value = false;
  }, 3000);
};

const validateEmail = (email) => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
};

const sendLoginCode = async () => {
  if (!email.value) {
    showError('请输入邮箱地址');
    return;
  }
  
  if (!validateEmail(email.value)) {
    showError('邮箱格式不正确');
    return;
  }
  
  isSendingCode.value = true;
  countdown.value = 60;
  
  try {
    await axios.post('http://localhost:5000/send-login-code', {
      email: email.value
    });
    
    const timer = setInterval(() => {
      countdown.value--;
      if (countdown.value <= 0) {
        clearInterval(timer);
        isSendingCode.value = false;
      }
    }, 1000);
  } catch (error) {
    showError('发送验证码失败: ' + error.response?.data?.message || '网络错误');
    isSendingCode.value = false;
  }
};

const login = async () => {
  if (loginMethod.value === 'password') {
    if (!username.value.trim()) {
      showError('请输入用户名或邮箱');
      return;
    }
    if (!password.value.trim()) {
      showError('请输入密码');
      return;
    }
  } else {
    if (!email.value.trim()) {
      showError('请输入邮箱地址');
      return;
    }
    if (!validateEmail(email.value)) {
      showError('邮箱格式不正确');
      return;
    }
    if (!verificationCode.value.trim()) {
      showError('请输入验证码');
      return;
    }
  }

  try {
    const payload = loginMethod.value === 'password' 
      ? { 
          username: username.value,
          password: password.value 
        }
      : { 
          email: email.value,
          verificationCode: verificationCode.value 
        };
    
    const response = await axios.post('http://localhost:5000/login', payload);
    
    if (response.data.status === 'success') {
      // 解析返回的 cookie 或 response 中的用户信息
      const userInfo = {
        username: loginMethod.value === 'password' ? username.value : email.value,
        // 如果后端返回了头像信息，使用后端返回的信息
        userAvatar: response.data.userAvatar || '/default-avatar.png'
      };
      
      // 保存用户信息到 Vuex store
      store.dispatch('login', userInfo);
      
      // 成功登录后跳转到首页
      router.push('/');
    } else {
      showError(response.data.message || '登录失败');
    }
  } catch (error) {
    showError('登录失败: ' + (error.response?.data?.message || '网络错误'));
  }
};
</script>

<style scoped>
.notification-bar {
  position: fixed;
  top: -60px;
  left: 50%;
  transform: translateX(-50%);
  background-color: #ff4d4f;
  color: white;
  padding: 12px 24px;
  border-radius: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  transition: top 0.5s ease;
  max-width: 80%;
  text-align: center;
  display: flex;
  align-items: center;
  gap: 8px;
}

.notification-bar.show {
  top: 20px;
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
  width: 420px;
  margin: 0 auto;
}

.logo-area {
  text-align: center;
  margin-bottom: 1.5rem;
}

.logo-area img {
  height: 48px;
}

.glass-card h2 {
  text-align: center;
  margin-bottom: 1.5rem;
  color: #2c3e50;
  font-weight: 500;
}

.login-method-tabs {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.login-method-tabs button {
  flex: 1;
  padding: 0.75rem;
  border: none;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.3);
  color: #2c3e50;
  cursor: pointer;
  transition: all 0.3s ease;
}

.login-method-tabs button.active {
  background: rgba(38, 45, 145, 0.15);
  color: #262d91;
  font-weight: 500;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.auth-form input {
  width: 100%;
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

.code-input-group {
  display: flex;
  gap: 0.5rem;
}

.code-input-group input {
  flex: 1;
}

.send-code-btn {
  padding: 0.75rem 1rem;
  border: none;
  border-radius: 12px;
  background: rgba(38, 45, 145, 0.15);
  color: #262d91;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.send-code-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.primary-button {
  width: 100%;
  padding: 0.75rem;
  border: none;
  border-radius: 12px;
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

.auth-footer {
  text-align: center;
  margin-top: 1.5rem;
  color: #7f8c8d;
  font-size: 0.9rem;
}

.auth-footer a {
  color: #262d91;
  text-decoration: none;
  font-weight: 500;
  margin-left: 0.25rem;
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
  
  .logo-area img {
    height: 40px;
  }
}
</style>