<template>
  <div class="min-h-screen flex flex-col">
    <!-- Header -->
    <Header />

    <!-- Main Content -->
    <router-view class="flex-grow" />

    <Footer v-if="showFooter" />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

import Header from './components/Header.vue'
import Footer from './components/Footer.vue'

const route = useRoute()
const showFooter = computed(() => route.name !== 'ApartmentDetail')
</script>
