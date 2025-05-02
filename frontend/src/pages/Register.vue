<template>
  <section class="bg-gray-100 min-h-screen flex items-center justify-center">
    <div class="w-full max-w-md bg-white rounded-lg shadow-md p-8">
      <h1 class="text-2xl font-bold text-gray-800 mb-6 text-center">Create your account</h1>
      
      <form class="space-y-5" @submit.prevent="handleRegister">
        
        <div>
          <label for="first_name" class="block mb-2 text-sm font-medium text-gray-700">First Name</label>
          <input type="text" id="first_name" v-model="first_name" placeholder="Enter your first name"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" required>
        </div>

        <div>
          <label for="last_name" class="block mb-2 text-sm font-medium text-gray-700">Last Name</label>
          <input type="text" id="last_name" v-model="last_name" placeholder="Enter your last name"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" required>
        </div>

        <div>
          <label for="login" class="block mb-2 text-sm font-medium text-gray-700">Login</label>
          <input type="text" id="login" v-model="login" placeholder="Enter your login"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" required>
        </div>

        <div>
          <label for="email" class="block mb-2 text-sm font-medium text-gray-700">Email</label>
          <input type="email" id="email" v-model="email" placeholder="Enter your email"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" required>
        </div>

        <div>
          <label for="phone" class="block mb-2 text-sm font-medium text-gray-700">Phone Number</label>
          <input type="tel" id="phone" v-model="phone" placeholder="Enter your phone number"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" required>
        </div>

        <div>
          <label for="password" class="block mb-2 text-sm font-medium text-gray-700">Password</label>
          <input type="password" id="password" v-model="password" placeholder="••••••••"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" required>
        </div>

        <div>
          <label for="confirm_password" class="block mb-2 text-sm font-medium text-gray-700">Confirm Password</label>
          <input type="password" id="confirm_password" v-model="confirm_password" placeholder="••••••••"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" required>
        </div>

        <div v-if="errorMessage" class="text-red-500 text-sm text-center mt-2">
          {{ errorMessage }}
        </div>

        <button type="submit"
          class="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition duration-200">
          Register
        </button>

        <p class="text-sm text-center text-gray-500">
          Already have an account? 
          <router-link to="/login" class="text-blue-600 hover:underline">Sign in</router-link>
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
      first_name: '',
      last_name: '',
      login: '',
      email: '',
      phone: '',
      password: '',
      confirm_password: '',
      errorMessage: null,
    };
  },
  mounted() {
    if (localStorage.getItem('access_token')) {
      this.$router.push('/profile'); // Якщо є токен, перенаправляємо на профіль
    }
  },
  methods: {
    async handleRegister() {
      if (this.password !== this.confirm_password) {
        this.errorMessage = 'Passwords do not match!';
        return;
      }

      try {
        const apiUrl = import.meta.env.VITE_API_URL;
        const response = await axios.post(`${apiUrl}/users/register/`, {
          first_name: this.first_name,
          last_name: this.last_name,
          login: this.login,
          email: this.email,
          phone_number: this.phone,
          password: this.password,
        });

        if (response.status === 201) {
          this.$router.push('/login');
        }
      } catch (error) {
        if (error.response && error.response.data) {
          this.errorMessage = error.response.data.detail || 'An error occurred during registration';
        } else {
          this.errorMessage = 'An error occurred. Please try again later.';
        }
      }
    }
  }
}
</script>
