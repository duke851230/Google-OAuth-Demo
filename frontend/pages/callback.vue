<template>
    <div class="auth-container">
        <h1>Authenticating...</h1>
        <div class="loader"></div>
    </div>
</template>
  
<script>
  import Cookies from 'js-cookie';

  export default {
    async mounted() {
        const code = this.$route.query.code;
        const state = this.$route.query.state;

        // 從本地存儲中獲取並刪除 state
        const storedState = localStorage.getItem('google_oauth_state');
        localStorage.removeItem('google_oauth_state');

        console.log(`${code}`)
        console.log(`${state}, ${storedState}`)
        if (state !== storedState) {
            console.error('Invalid state parameter');
            return;
        }

        if (code) {
            const response = await this.$axios.get(
                '/auth/csrf_token/',
                {
                    withCredentials: true  // 一定要帶，不然會被瀏覽器擋下 Cookies
                }
            )
            const csrfToken = Cookies.get('csrftoken');

            try {
                const response = await this.$axios.post(
                    '/auth/oauth/login/', 
                    {
                        code: code,
                        redirect_uri: 'http://localhost:3000/callback'
                    },
                    {
                        headers: {'X-CSRFToken': csrfToken},
                        withCredentials: true  // 一定要帶，不然會被瀏覽器擋下 Cookies
                    }
                );

                console.log(response.data);
                const token = response.data.access;
                localStorage.setItem('jwt_token', token);
                this.$router.push('/user');
            } catch (error) {
                console.error('Error authenticating:', error);
            }
        } else {
            console.error('No code found in URL');
            this.$router.push('/');
        }
    }
  }
</script>

<style scoped>
.auth-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background-color: #f9f9f9;
  color: #333;
  font-family: Arial, sans-serif;
  text-align: center;
}

h1 {
  font-size: 2em;
  margin-bottom: 20px;
}

.loader {
  border: 8px solid #f3f3f3;
  border-top: 8px solid #3498db;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 2s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>