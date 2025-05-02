<template>
  <section class="bg-gray-100 min-h-screen flex items-center justify-center py-10 px-4">
    <div class="w-full max-w-7xl bg-white rounded-lg shadow-md p-8">
      <div class="flex justify-between mb-6">
        <a
          href="http://localhost:8000/admin/"
          class="bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-lg transition"
        >
          Add Apartment
        </a>
        <router-link
          :to="{ name: 'ViewBookings' }"
          class="bg-green-600 hover:bg-green-700 text-white py-2 px-4 rounded-lg transition"
        >
          View Bookings
        </router-link>
      </div>

      <h2 class="text-xl font-bold text-gray-800 mb-4">List of Apartments</h2>

      <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <div
          v-for="apartment in apartments"
          :key="apartment.slug"
          class="flex flex-col border border-gray-300 rounded-lg overflow-hidden shadow-sm hover:shadow-md transition cursor-pointer"
        >
          <img :src="apartment.image" alt="Apartment" class="w-full h-36 object-cover" />

          <div class="p-4 flex flex-col justify-between w-full">
            <div>
              <h3 class="font-semibold text-lg truncate">{{ apartment.name }}</h3>
              <p class="text-gray-600 text-sm">{{ apartment.square }} m²</p>
            </div>
            <div>
              <p class="text-blue-600 font-bold text-lg">{{ formatPrice(apartment.price) }} ₴</p>
              <p
                :class="apartment.availability ? 'text-green-600' : 'text-red-500'"
                class="text-sm font-medium"
              >
                {{ apartment.availability ? 'Available' : 'Not available' }}
              </p>
            </div>
            <div class="flex justify-between mt-3 space-x-2">
              <router-link
                :to="{ name: 'ApartmentDetail', params: { slug: apartment.slug } }"
                class="bg-blue-600 hover:bg-blue-700 text-white py-1 px-3 rounded-lg"
              >
                View
              </router-link>
              <router-link
                :to="{ name: 'ApartmentEdit', params: { slug: apartment.slug } }"
                class="bg-yellow-600 hover:bg-yellow-700 text-white py-1 px-3 rounded-lg"
              >
                Edit
              </router-link>
              <button
                @click="deleteApartment(apartment.slug)"
                class="bg-red-600 hover:bg-red-700 text-white py-1 px-3 rounded-lg"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="pagination" class="flex justify-center mt-6 space-x-4">
        <button
          v-if="pagination.previous"
          @click="fetchApartments(pagination.previous)"
          class="bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700"
        >
          Previous
        </button>
        <button
          v-if="pagination.next"
          @click="fetchApartments(pagination.next)"
          class="bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700"
        >
          Next
        </button>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const apartments = ref([]);
const pagination = ref(null);
const apiUrl = import.meta.env.VITE_API_URL;

async function fetchApartments(url = `${apiUrl}/apartments`) {
  const token = localStorage.getItem('access_token');

  if (!token) {
    console.error('No token found. Please log in first.');
    return;
  }

  try {
    const response = await axios.get(url, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    apartments.value = response.data.results;
    pagination.value = {
      next: response.data.next,
      previous: response.data.previous,
    };
  } catch (error) {
    console.error('Failed to fetch apartments:', error);
  }
}

const formatPrice = (price) => {
  return parseFloat(price).toFixed(2);
};

const deleteApartment = async (slug) => {
  const token = localStorage.getItem('access_token');

  if (!token) {
    console.error('No token found. Please log in first.');
    return;
  }

  try {
    const confirmation = confirm('Are you sure you want to delete this apartment?');
    if (!confirmation) return;

    await axios.delete(`${apiUrl}/apartments/${slug}/delete/`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    fetchApartments();
    alert('Apartment deleted successfully.');
  } catch (error) {
    console.error('Failed to delete apartment:', error);
    alert('Error deleting apartment.');
  }
};

onMounted(() => {
  fetchApartments();
});
</script>
