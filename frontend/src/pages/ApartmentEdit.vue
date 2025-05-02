<template>
  <section class="bg-gray-100 min-h-screen flex items-center justify-center py-10 px-4">
    <div class="w-full max-w-2xl bg-white rounded-lg shadow-md p-8">
      <h2 class="text-xl font-bold text-gray-800 mb-6">Edit Apartment</h2>

      <form @submit.prevent="updateApartment">
        <div class="mb-4">
          <label class="block text-sm font-medium mb-1">Name</label>
          <input v-model="form.name" class="w-full border rounded p-2" required />
        </div>

        <div class="mb-4">
          <label class="block text-sm font-medium mb-1">Slug</label>
          <input v-model="form.slug" class="w-full border rounded p-2" readonly /> <!-- Readonly input -->
        </div>

        <div class="mb-4">
          <label class="block text-sm font-medium mb-1">Description</label>
          <textarea v-model="form.description" class="w-full border rounded p-2" rows="3"></textarea>
        </div>

        <div class="mb-4">
          <label class="block text-sm font-medium mb-1">Price</label>
          <input type="number" v-model="form.price" class="w-full border rounded p-2" />
        </div>

        <div class="mb-4">
          <label class="block text-sm font-medium mb-1">Number of Rooms</label>
          <input type="number" v-model="form.number_of_rooms" class="w-full border rounded p-2" />
        </div>

        <div class="mb-4">
          <label class="block text-sm font-medium mb-1">Square (m²)</label>
          <input type="number" v-model="form.square" class="w-full border rounded p-2" />
        </div>

        <div class="mb-4">
          <label class="block text-sm font-medium mb-1">Availability</label>
          <select v-model="form.availability" class="w-full border rounded p-2">
            <option :value="true">Available</option>
            <option :value="false">Not Available</option>
          </select>
        </div>

        <div class="mb-4">
          <label class="block text-sm font-medium mb-1">Image (not editable)</label>
          <img :src="form.image" alt="Apartment Image" class="w-full max-h-64 object-cover rounded border" />
        </div>

        <div class="flex justify-end">
          <button type="submit" class="bg-yellow-600 hover:bg-yellow-700 text-white px-4 py-2 rounded">
            Save Changes
          </button>
        </div>
      </form>
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import axios from 'axios';
import { useRoute, useRouter } from 'vue-router';

const apiUrl = import.meta.env.VITE_API_URL;
const route = useRoute();
const router = useRouter();

const form = ref({
  name: '',
  slug: '',
  description: '',
  price: '',
  number_of_rooms: '',
  square: '',
  availability: true,
  image: '', // тільки для перегляду
});

const fetchApartment = async () => {
  const token = localStorage.getItem('access_token');
  const slug = route.params.slug;

  try {
    const response = await axios.get(`${apiUrl}/apartments/${slug}/`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    form.value = response.data;
  } catch (error) {
    console.error('Error fetching apartment:', error);
    alert('Failed to load apartment data.');
  }
};

const updateApartment = async () => {
  const token = localStorage.getItem('access_token');
  const slug = route.params.slug;

  const { image, slug: slugToRemove, ...dataToUpdate } = form.value;

  try {
    await axios.patch(`${apiUrl}/apartments/${slug}/update/`, dataToUpdate, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    alert('Apartment updated successfully!');
    router.push('/adminPanel');
  } catch (error) {
    console.error('Update failed:', error);
    alert('Failed to update apartment.');
  }
};

onMounted(() => {
  fetchApartment();
});
</script>
