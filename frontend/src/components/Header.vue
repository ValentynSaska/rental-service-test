<template>
  <header>
    <nav class="bg-white border-gray-200 px-4 lg:px-6 py-2.5 dark:bg-sky-600">
      <div class="flex flex-wrap justify-between items-center mx-auto max-w-screen-xl">
        <a href="/" class="flex items-center">
          <img src="/Logo.png" class="mr-3 h-10 sm:h-15" alt="Logo" />
        </a>

        <!-- Menu for larger screens -->
        <div class="hidden lg:flex items-center space-x-4 mx-auto">
          <button @click="$router.push({ name: 'ApartmentList' })" class="text-white hover:bg-blue-400 px-4 py-2 rounded-lg transition-colors duration-400">
            List Apartments
          </button>
          <button @click="$router.push({ name: 'Profile' })" class="text-white hover:bg-blue-400 px-4 py-2 rounded-lg transition-colors duration-400">
            Profile
          </button>
        </div>

        <!-- Burger Menu Button -->
        <button @click="toggleMenu" data-collapse-toggle="mobile-menu" type="button" class="inline-flex items-center p-2 text-gray-500 rounded-lg lg:hidden hover:bg-blue-400 focus:ring-2 focus:bg-blue-400 dark:text-blue-700 dark:hover:bg-blue-400">
          <span class="sr-only">Open main menu</span>
          <svg v-if="isMenuOpen" class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path>
          </svg>
          <svg v-else class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
            <path fill-rule="evenodd" d="M3 5a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 10a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 15a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd"></path>
          </svg>
        </button>
      </div>

      <!-- Mobile Menu -->
      <div v-if="isMenuOpen" class="lg:hidden" id="mobile-menu">
        <ul class="flex flex-col space-y-4 p-4">
          <li>
            <button @click="$router.push({ name: 'ApartmentList' })" class="block text-white py-2 rounded hover:bg-blue-400 transition-colors duration-400">List Apartments</button>
          </li>
          <li>
            <button @click="$router.push({ name: 'Profile' })" class="block dark:text-white py-2 rounded hover:bg-blue-400 transition-colors duration-400">Profile</button>
          </li>
        </ul>
      </div>
    </nav>
  </header>
</template>

<script>
export default {
  data() {
    return {
      isMenuOpen: false,
    };
  },
  methods: {
    toggleMenu() {
      this.isMenuOpen = !this.isMenuOpen;
    }
  }
};
</script>