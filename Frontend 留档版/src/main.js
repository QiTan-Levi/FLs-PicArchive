import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createStore } from 'vuex'

const store = createStore({
  state() {
    return {
      isLoggedIn: false,
      userAvatar: '',
      userName: ''
    }
  },
  mutations: {
    setUser(state, userInfo) {
      state.isLoggedIn = true;
      state.userAvatar = userInfo.userAvatar;
      state.userName = userInfo.username;
    }
  },
  actions: {
    login({ commit }, userInfo) {
      commit('setUser', userInfo);
      localStorage.setItem('isLoggedIn', 'true');
      localStorage.setItem('userAvatar', userInfo.userAvatar);
      localStorage.setItem('userName', userInfo.username);
    },
    logout({ commit }) {
      commit('setUser', { userAvatar: '', username: '' });
      localStorage.removeItem('isLoggedIn');
      localStorage.removeItem('userAvatar');
      localStorage.removeItem('userName');
    },
    initLoginState({ commit }) {
      const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';
      const userAvatar = localStorage.getItem('userAvatar');
      const userName = localStorage.getItem('userName');
      if (isLoggedIn) {
        commit('setUser', { userAvatar, username: userName });
      }
    }
  }
})

const app = createApp(App)
app.use(router)
app.use(store)
app.mount('#app')