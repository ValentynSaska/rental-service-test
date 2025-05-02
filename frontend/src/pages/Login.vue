<template>
  <section class="bg-gray-100 min-h-screen flex items-center justify-center">
    <div class="w-full max-w-md bg-white rounded-lg shadow-md p-8">
      <h1 class="text-2xl font-bold text-gray-800 mb-6 text-center">Sign in to your account</h1>

      <form class="space-y-5" @submit.prevent="handleLogin">
        <div>
          <label for="login" class="block mb-2 text-sm font-medium text-gray-700">Login</label>
          <input
            type="text"
            id="login"
            v-model="login"
            placeholder="Enter your login"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>

        <div>
          <label for="password" class="block mb-2 text-sm font-medium text-gray-700">Password</label>
          <input
            type="password"
            id="password"
            v-model="password"
            placeholder="••••••••"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>

        <div v-if="errorMessage" class="text-red-500 text-sm text-center mt-2">
          {{ errorMessage }}
        </div>

        <button
          type="submit"
          class="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition duration-200"
        >
          Sign in
        </button>

        <p class="text-sm text-center text-gray-500">
          Don’t have an account yet?
          <router-link to="/register" class="text-blue-600 hover:underline">Sign up</router-link>
        </p>
      </form>
    </div>
  </section>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      login: '',
      password: '',
      errorMessage: null,
    };
  },
  mounted() {
    if (localStorage.getItem('access_token')) {
      this.$router.push('/profile');
    }
  },
  methods: {
    async handleLogin() {
    try {
      const apiUrl = import.meta.env.VITE_API_URL;

      const response = await axios.post(`${apiUrl}/users/token/`, {
        login: this.login,
        password: this.password,
      });

      const { access, refresh } = response.data;

      if (access && refresh) {
        localStorage.setItem('access_token', access);
        localStorage.setItem('refresh_token', refresh);

        const profileResponse = await axios.get(`${apiUrl}/users/profile/`, {
          headers: {
            Authorization: `Bearer ${access}`,
          },
        });

        const isAdmin = profileResponse.data.is_admin;
        localStorage.setItem('user_role', isAdmin ? 'admin' : 'user');

        this.$router.push('/profile');
      } else {
        this.errorMessage = 'Incorrect login or password.';
      }
    } catch (error) {
      if (error.response && error.response.status === 401) {
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
          try {
            const refreshResponse = await axios.post(`${apiUrl}/users/token/refresh/`, {
              refresh: refreshToken,
            });

            const newAccess = refreshResponse.data.access;
            localStorage.setItem('access_token', newAccess);

            const profileResponse = await axios.get(`${apiUrl}/users/profile/`, {
              headers: {
                Authorization: `Bearer ${newAccess}`,
              },
            });

            const isAdmin = profileResponse.data.is_admin;
            localStorage.setItem('user_role', isAdmin ? 'admin' : 'user');

            this.$router.push('/profile');
          } catch (refreshError) {
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('user_role');
            this.$router.push('/login');
            this.errorMessage = 'Session expired. Please log in again.';
          }
        } else {
          this.errorMessage = 'Session expired. Please log in again.';
          this.$router.push('/login');
        }
      } else {
        this.errorMessage = 'An error occurred. Please try again later.';
      }
    }
  }
,
  },
};
</script>
