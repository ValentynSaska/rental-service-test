<template>
  <section class="bg-gray-100 min-h-screen py-10 px-4 flex items-start justify-center">
    <div class="w-full max-w-6xl bg-white rounded-lg shadow-md p-8">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold text-gray-800">Apartment Bookings</h2>
        <router-link
          :to="{ name: 'adminPanel' }"
          class="bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-lg transition"
        >
          ← Back to Admin Panel
        </router-link>
      </div>

      <div v-if="bookings.length > 0" class="space-y-4">
        <div
          v-for="(booking, index) in bookings"
          :key="booking.id"
          class="border border-gray-300 rounded-lg p-4 shadow-sm bg-white hover:shadow-md transition"
        >
          <div class="flex justify-between items-center mb-2">
            <h3 class="text-lg font-semibold text-gray-700">{{ booking.apartment_name }}</h3>
          </div>
          <p class="text-sm text-gray-600">
            Booked by: <strong>{{ booking.user_first_name }}</strong>
          </p>
        </div>
      </div>

      <div v-else class="text-center text-gray-500 mt-10">
        No bookings found.
      </div>

      <!-- Pagination -->
      <div v-if="pagination" class="flex justify-center mt-6 space-x-4">
        <button
          v-if="pagination.previous"
          @click="fetchBookings(pagination.previous)"
          class="bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700"
        >
          Previous
        </button>
        <button
          v-if="pagination.next"
          @click="fetchBookings(pagination.next)"
          class="bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700"
        >
          Next
        </button>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'


const bookings = ref([])
const pagination = ref(null)

const apiUrl = import.meta.env.VITE_API_URL;
async function fetchBookings(url = `${apiUrl}/bookings/`) {
  const token = localStorage.getItem('access_token')

  if (!token) {
    console.error('No token found. Please log in first.')
    return
  }

  try {
    const response = await axios.get(url, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    bookings.value = response.data.results
    pagination.value = {
      next: response.data.next,
      previous: response.data.previous
    }
  } catch (error) {
    console.error('Failed to fetch bookings:', error)
  }
}

onMounted(() => {
  fetchBookings()
})
</script>
