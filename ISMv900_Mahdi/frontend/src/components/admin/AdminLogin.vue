<template>
  <div class="login-container">
    <h2>ورود به سیستم لغو سفارشات</h2>
    <form @submit.prevent="login" class="login-form">
      <div class="form-group">
        <label for="username">نام کاربری:</label>
        <input type="text" id="username" v-model="username" required placeholder="نام کاربری را وارد کنید" />
      </div>
      <div class="form-group">
        <label for="password">رمز عبور:</label>
        <input type="password" id="password" v-model="password" required placeholder="رمز عبور را وارد کنید" />
      </div>
      <button type="submit" :disabled="loading">
        {{ loading ? 'در حال ورود...' : 'ورود' }}
      </button>
    </form>
    <div v-if="error" class="error-message">{{ error }}</div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AdminLogin',
  data() {
    return {
      username: '',
      password: '',
      error: '',
      loading: false
    }
  },
  mounted() {
    document.title = 'ورود به سیستم لغو سفارشات';
  },
  methods: {
    async login() {
      this.loading = true
      this.error = ''

      try {
        const formData = new FormData()
        formData.append('username', this.username)
        formData.append('password', this.password)

        const response = await axios.post(`${window.location.origin}/myapp/admin/login/`, formData)


        if (response.data.success) {
          // ذخیره توکن و وضعیت ادمین
          localStorage.setItem('token', 'dummy-token')
          localStorage.setItem('is_superuser', 'true')

          // هدایت به صفحه مورد نظر
          const redirectPath = this.$route.query.redirect || '/myapp/admin/cancel/'
          // اگر مسیر report است، به صفحه report هدایت کن
          if (redirectPath.includes('report')) {
            this.$router.push('/myapp/admin/report/')
          } else {
            this.$router.push(redirectPath)
          }
        } else {
          this.error = response.data.error || 'نام کاربری یا رمز عبور اشتباه است'
        }
      } catch (error) {
        this.error = error.response?.data?.error || 'خطا در ارتباط با سرور'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
@font-face {
  font-family: 'BNazanin';
  src: url('../../assets/fonts/BNazanin.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
  font-display: swap;
}

.login-container {
  max-width: 400px;
  margin: 2rem auto;
  padding: 2rem;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  font-family: 'BNazanin', Arial, sans-serif !important;
}

h2 {
  text-align: center;
  color: #333;
  margin-bottom: 2rem;
  font-family: 'BNazanin', Arial, sans-serif !important;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  font-family: 'BNazanin', Arial, sans-serif !important;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  font-family: 'BNazanin', Arial, sans-serif !important;
}

label {
  font-weight: bold;
  color: #555;
  font-family: 'BNazanin', Arial, sans-serif !important;
}

input {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  font-family: 'BNazanin', Arial, sans-serif !important;
}

input:focus {
  outline: none;
  border-color: #4CAF50;
}

button {
  padding: 0.75rem;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
  font-family: 'BNazanin', Arial, sans-serif !important;
}

button:hover {
  background-color: #45a049;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.error-message {
  margin-top: 1rem;
  padding: 0.75rem;
  background-color: #ffebee;
  color: #c62828;
  border-radius: 4px;
  text-align: center;
  font-family: 'BNazanin', Arial, sans-serif !important;
}

/* RTL Support */
[dir="rtl"] .login-container {
  text-align: right;
}

[dir="rtl"] input {
  text-align: right;
}
</style>