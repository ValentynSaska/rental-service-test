<template>
    <footer class="bg-sky-600 text-white p-4">
      <div class="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center">
        <div class="text-lg font-semibold mb-4 md:mb-0">
          &copy; 2025 Apartment Rental Service
        </div>
  
        <nav class="flex space-x-4">
          <router-link :to="{ name: 'ApartmentList' }" class="hover:bg-blue-400 px-4 py-2 rounded-lg transition-colors duration-400">
            Apartments List
          </router-link>
          <router-link :to="{ name: 'Profile' }" class="hover:bg-blue-400 px-4 py-2 rounded-lg transition-colors duration-400">
            Profile
          </router-link>
        </nav>
      </div>
    </footer>
  </template>
