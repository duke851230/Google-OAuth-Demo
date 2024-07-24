<template>
  <div class="login-container">
    <h1>Welcome to My Login Page</h1>
    <button class="login-button" @click="loginWithGoogle">Login with Google</button>
  </div>
</template>

<script>
export default {
  methods: {
    loginWithGoogle() {
      const googleClientId = '993916594104-loigj3go0osnqhuqihnollrarvmtieij.apps.googleusercontent.com';
      const redirectUri = 'http://localhost:3000/callback';
      const responseType = 'code';
      const state = Math.random().toString(36).substring(2);  // 防 CSRF 用
      const scope = 'https://www.googleapis.com/auth/userinfo.email';
      const googleAuthUrl = 'https://accounts.google.com/o/oauth2/v2/auth';

      // 將 state 保存到本地存儲，供之後 callback 時驗證
      localStorage.setItem('google_oauth_state', state);

      const url = `${googleAuthUrl}?response_type=${responseType}&client_id=${googleClientId}&redirect_uri=${redirectUri}&scope=${scope}&state=${state}`;
      window.location.href = url;
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background-color: #f0f2f5;
  padding: 20px;
  box-sizing: border-box;
}

h1 {
  color: #333;
  font-size: 2.5em;
  margin-bottom: 20px;
}

.login-button {
  background-color: #4285F4;
  color: white;
  border: none;
  padding: 15px 30px;
  font-size: 1.2em;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.login-button:hover {
  background-color: #357ae8;
}

.login-button:focus {
  outline: none;
}
</style>
