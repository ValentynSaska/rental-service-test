<template>
  <div class="p-6 max-w-4xl mx-auto">
    <button @click="$router.push({ name: 'ApartmentList' })" class="mb-4 text-blue-600 hover:underline flex items-center gap-2">
      Back to Listings
    </button>

    <h1 class="text-2xl font-bold mb-6">Apartment Details</h1>

    <div v-if="apartment">
      <div class="flex flex-col md:flex-row gap-6 mb-6">
        <img :src="apartment.image" alt="Apartment" class="w-full md:w-2/3 h-64 object-cover rounded" />
        <div class="flex flex-col justify-between">
          <div>
            <h2 class="text-2xl font-semibold mb-2">{{ apartment.name }}</h2>
            <p class="text-blue-600 font-bold text-xl mb-4">{{ formatPrice(apartment.price) }} ₴</p>
          </div>
          <button
            class="bg-blue-600 text-white py-2 px-4 rounded hover:scale-105 hover:bg-blue-700 transition"
            @click="handleBooking"
          >
            Book now
          </button>
        </div>
      </div>

      <!-- Tabs -->
      <div>
        <div class="border-b border-gray-200 mb-4">
          <button @click="activeTab = 'description'" :class="activeTab === 'description' ? activeClass : inactiveClass">
            Description
          </button>
          <button @click="activeTab = 'info'" :class="activeTab === 'info' ? activeClass : inactiveClass">
            Information
          </button>
        </div>

        <div v-if="activeTab === 'description'" class="mb-6">
          <p class="text-gray-700">{{ apartment.description }}</p>
        </div>

        <div v-else>
          <div class="overflow-x-auto rounded-lg shadow-md">
            <table class="w-full text-left border border-gray-200 bg-white">
              <tbody>
                <tr class="hover:bg-gray-50">
                  <td class="px-4 py-3 font-medium text-gray-700 border-b">Number of Rooms</td>
                  <td class="px-4 py-3 border-b">{{ apartment.number_of_rooms }}</td>
                </tr>
                <tr class="hover:bg-gray-50">
                  <td class="px-4 py-3 font-medium text-gray-700 border-b">Square Meters</td>
                  <td class="px-4 py-3 border-b">{{ apartment.square }} m²</td>
                </tr>
                <tr class="hover:bg-gray-50">
                  <td class="px-4 py-3 font-medium text-gray-700 border-b">Availability</td>
                  <td class="px-4 py-3 border-b">
                    <span :class="apartment.availability ? 'text-green-600' : 'text-red-600'">
                      {{ apartment.availability ? 'Available' : 'Unavailable' }}
                    </span>
                  </td>
                </tr>
                <tr class="hover:bg-gray-50">
                  <td class="px-4 py-3 font-medium text-gray-700 border-b">Created At</td>
                  <td class="px-4 py-3 border-b">{{ formatDate(apartment.created_at) }}</td>
                </tr>
                <tr class="hover:bg-gray-50">
                  <td class="px-4 py-3 font-medium text-gray-700">Updated At</td>
                  <td class="px-4 py-3">{{ formatDate(apartment.updated_at) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <p v-else class="text-red-500">Apartment not found</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      apartment: null,
      activeTab: 'description',
      activeClass: 'px-4 py-2 border-b-2 border-blue-600 text-blue-600 font-semibold',
      inactiveClass: 'px-4 py-2 text-gray-600 hover:text-blue-600',
    };
  },
  methods: {
    async fetchApartment() {
      try {
        const slug = this.$route.params.slug;
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/apartments/${slug}/`);
        this.apartment = response.data;
      } catch (error) {
        console.error('Failed to fetch apartment details:', error);
      }
    },
    formatPrice(price) {
      const num = parseFloat(price);
      return num.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      const options = {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
      };
      return date.toLocaleString('uk-UA', options).replace(',', '');
    },
    async handleBooking() {
      const token = localStorage.getItem('access_token');
      if (!token) {
        // Якщо користувач не авторизований, пересилаємо на сторінку логіну
        this.$router.push({ name: 'Login' });
        return;
      }

      try {
        // Виконуємо POST-запит на бронювання квартири
        await axios.post(
          `${import.meta.env.VITE_API_URL}/bookings/`,
          { apartment: this.apartment.id },
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        alert('Apartment successfully booked!');
        this.fetchApartment(); // Оновлюємо доступність квартири після бронювання
      } catch (error) {
        console.error('Booking failed:', error);
        alert('Booking failed. Please try again.');
      }
    },
  },
  created() {
    this.fetchApartment();
  },
};
</script>
