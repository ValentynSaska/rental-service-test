<template>
  <section class="min-h-screen bg-gray-100">
    <header class="bg-white shadow-md py-6 px-6 md:px-12 lg:px-20">
      <div class="max-w-6xl mx-auto">
        <div class="flex flex-col md:flex-row md:justify-between md:items-center space-y-4 md:space-y-0">
          <div>
            <h2 class="text-2xl font-bold text-gray-800">Welcome, {{ user.name }}</h2>
            <p class="text-gray-500">
              Role: {{ user.isAdmin ? 'Admin' : 'User' }}
            </p>
          </div>
          <div class="flex flex-col sm:flex-row sm:space-x-4 space-y-2 sm:space-y-0">
            <button
              @click="deleteAccount"
              class="bg-red-600 hover:bg-red-700 text-white px-5 py-2 rounded-lg"
            >
              Delete Account
            </button>
            <button
              @click="logout"
              class="bg-gray-600 hover:bg-gray-700 text-white px-5 py-2 rounded-lg"
            >
              Logout
            </button>
            <router-link
              v-if="user.isAdmin"
              :to="{ name: 'adminPanel' }"
              class="bg-green-600 hover:bg-green-700 text-white px-5 py-2 rounded-lg"
            >
              Admin Panel
            </router-link>
          </div>
        </div>
      </div>
    </header>

    <div class="max-w-6xl mx-auto px-6 md:px-12 lg:px-20 mt-8">
      <h2 class="text-xl font-semibold text-gray-800 mb-4">Your Bookings</h2>
      <div v-if="bookings.length === 0" class="text-center text-gray-500">You have no bookings yet.</div>
      <ul class="space-y-4">
        <li
          v-for="booking in bookings"
          :key="booking.id"
          class="flex justify-between items-center p-4 bg-white rounded-lg shadow"
        >
          <span class="text-gray-700">Apartment: {{ booking.apartment_name }}</span>
          <span class="text-gray-700">User: {{ booking.user_first_name }}</span>
          <button
            @click="cancelBooking(booking.id)"
            class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg"
          >
            Cancel Booking
          </button>
        </li>
      </ul>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const user = ref({ name: '', isAdmin: false });
const bookings = ref([]);

const API_URL = import.meta.env.VITE_API_URL;

const logout = () => {
  localStorage.removeItem('access_token');
  router.push('/login');
};

const cancelBooking = async (bookingId) => {
  try {
    const token = localStorage.getItem('access_token');
    await axios.delete(`${API_URL}/bookings/${bookingId}/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    bookings.value = bookings.value.filter(booking => booking.id !== bookingId);
    alert('Booking canceled successfully.');
  } catch (err) {
    console.error("Error canceling booking:", err);
    alert('Failed to cancel booking.');
  }
};

const getCurrentUser = async () => {
  const token = localStorage.getItem('access_token');
  if (!token) {
    router.push({ name: 'Login' });
    return;
  }

  try {
    const { data } = await axios.get(`${API_URL}/users/profile/`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    user.value = {
      name: `${data.first_name} ${data.last_name}`,
      isAdmin: data.is_admin, 
    };

    const bookingsResponse = await axios.get(`${API_URL}/bookings/`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    bookings.value = bookingsResponse.data.results.map((booking) => ({
      id: booking.id,
      apartment_name: booking.apartment_name,
      user_first_name: booking.user_first_name,
    }));
  } catch (err) {
    console.error("Error fetching user profile:", err);
    localStorage.removeItem('access_token');
    router.push({ name: 'Login' });
  }
};

const deleteAccount = async () => {
  const confirmed = confirm('Are you sure you want to delete your account? This action cannot be undone.');
  if (!confirmed) return;

  const token = localStorage.getItem('access_token');
  try {
    await axios.delete(`${API_URL}/users/profile/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    alert('Account deleted successfully.');
    logout();
  } catch (err) {
    console.error("Error deleting account:", err);
    alert('Failed to delete account.');
  }
};

onMounted(() => {
  getCurrentUser();
});
</script>
