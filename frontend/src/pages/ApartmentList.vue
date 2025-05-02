<template>
  <div class="bg-white">
    <main class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="border-b border-gray-200 py-6">
        <h1 class="text-2xl font-bold text-gray-900 text-center mb-4">Apartments</h1>
        <div class="flex flex-col sm:flex-row sm:justify-end sm:items-center gap-2 max-w-md mx-auto">
          <input
            v-model="searchQuery"
            placeholder="Search by name"
            class="p-2 border border-gray-300 rounded-lg w-full"
          />
          <button
            @click="searchApartments"
            class="w-full sm:w-auto px-4 py-2 bg-blue-500 text-white rounded-lg hover:scale-105 hover:bg-blue-700 transition"
          >
            Search
          </button>
        </div>
      </div>

      <!-- Content -->
      <section class="pt-6 pb-24">
        <div class="grid grid-cols-1 lg:grid-cols-4 gap-x-8 gap-y-10">
          <!-- Filters -->
          <aside class="space-y-6">
            <div>
              <h3 class="font-medium text-gray-900">Price (₴)</h3>
              <div class="flex gap-2 mt-2">
                <input v-model.number="draftPriceMin" type="number" min="0" placeholder="From" class="w-1/2 p-2 border rounded" />
                <input v-model.number="draftPriceMax" type="number" min="0" placeholder="To" class="w-1/2 p-2 border rounded" />
              </div>
            </div>

            <div>
              <h3 class="font-medium text-gray-900">Rooms</h3>
              <div class="flex gap-2 mt-2">
                <input v-model.number="draftRoomsMin" type="number" min="1" placeholder="Min" class="w-1/2 p-2 border rounded" />
                <input v-model.number="draftRoomsMax" type="number" min="1" placeholder="Max" class="w-1/2 p-2 border rounded" />
              </div>
            </div>

            <div class="flex items-center">
              <input v-model="draftAvailable" type="checkbox" id="available" class="mr-2" />
              <label for="available">Only available</label>
            </div>

            <button @click="applyFilters" class="w-full px-4 py-2 bg-blue-500 text-white rounded hover:scale-105 hover:bg-blue-700 transition">
              Apply Filters
            </button>
          </aside>

          <!-- Apartments -->
          <div class="lg:col-span-3 grid gap-6">
            <router-link
              v-for="apartment in apartments"
              :key="apartment.slug"
              :to="{ name: 'ApartmentDetail', params: { slug: apartment.slug } }"
              :class="{
                'flex border border-gray-300 rounded-lg overflow-hidden shadow-sm hover:shadow-md transition cursor-pointer h-36': true,
                'bg-gray-200 bg-opacity-50 pointer-events-none': !apartment.availability
              }"
            >
              <img :src="apartment.image" alt="Apartment" class="w-36 h-36 object-cover" />
              <div class="p-4 flex flex-col justify-between">
                <div>
                  <h3 class="font-semibold text-lg truncate">{{ apartment.name }}</h3>
                  <p class="text-gray-600 text-sm">{{ apartment.square }} m²</p>
                </div>
                <div>
                  <p class="text-blue-600 font-bold text-lg">{{ formatPrice(apartment.price) }} ₴</p>
                  <p :class="apartment.availability ? 'text-green-600' : 'text-red-500'" class="text-sm font-medium">
                    {{ apartment.availability ? 'Available' : 'Not available' }}
                  </p>
                </div>
              </div>
            </router-link>

            <p v-if="apartments.length === 0" class="text-gray-500">No apartments found.</p>
          </div>
        </div>

        <!-- Pagination -->
        <div class="flex justify-center mt-10">
          <button
            @click="changePage(currentPage - 1)"
            :disabled="!previousPageUrl"
            class="px-4 py-2 mx-1 bg-gray-200 hover:bg-gray-300 rounded"
          >
            Previous
          </button>
          <span class="px-4 py-2 bg-blue-500 text-white rounded">{{ currentPage }}</span>
          <button
            @click="changePage(currentPage + 1)"
            :disabled="!nextPageUrl"
            class="px-4 py-2 mx-1 bg-gray-200 hover:bg-gray-300 rounded"
          >
            Next
          </button>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      apartments: [],
      currentPage: 1,
      totalCount: 0,
      nextPageUrl: null,
      previousPageUrl: null,

      // Filters
      searchQuery: '',
      draftPriceMin: 0,
      draftPriceMax: 999999,
      draftRoomsMin: 1,
      draftRoomsMax: 30,
      draftAvailable: false,
    };
  },
  methods: {
    async fetchApartments() {
      try {
        const params = {
          page: this.currentPage,
          search: this.searchQuery,
          price_min: this.draftPriceMin,
          price_max: this.draftPriceMax,
          rooms_min: this.draftRoomsMin,
          rooms_max: this.draftRoomsMax,
          available: this.draftAvailable,
        };
        
        const apiUrl = import.meta.env.VITE_API_URL;
        const response = await axios.get(`${apiUrl}/apartments/`, { params });
        
        this.apartments = response.data.results;
        this.totalCount = response.data.count;
        this.nextPageUrl = response.data.next;
        this.previousPageUrl = response.data.previous;
      } catch (error) {
        console.error('Failed to fetch apartments:', error);
      }
    },
    searchApartments() {
      this.currentPage = 1;
      this.fetchApartments();
    },
    applyFilters() {
      this.currentPage = 1;
      this.fetchApartments();
    },
    changePage(page) {
      this.currentPage = page;
      this.fetchApartments();
    },
    formatPrice(price) {
      const num = parseFloat(price);
      return num.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    },
  },
  mounted() {
    this.fetchApartments();
  },
};

</script>
