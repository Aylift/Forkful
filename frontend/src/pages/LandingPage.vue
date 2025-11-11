<template>
    <div class="min-h-screen flex flex-col items-center justify-center text-white text-center p-8"
         style="background: linear-gradient(to bottom, #fd8a4f, #f96c5c);">
      <h1 class="text-6xl font-bold mb-4">
        Welcome to 🍎 WellnessApp
      </h1>
      <p class="text-2xl mb-8">
        Your all-in-one solution for tracking meals, calories, and fitness goals.
      </p>
      <div v-if="!auth.isAuthenticated">
        <router-link 
          to="/loginregister"
          class="px-8 py-3 bg-white text-orange-500 font-bold rounded-full text-xl hover:bg-gray-200 transition-colors"
        >
          Get Started
        </router-link>
      </div>
      <div v-else>
        <router-link 
          to="/home"
          class="px-8 py-3 bg-white text-orange-500 font-bold rounded-full text-xl hover:bg-gray-200 transition-colors"
        >
          Go to Your Dashboard
        </router-link>
      </div>
    </div>
  </template>
  
  <script setup>
  import { useAuthStore } from '@/stores/auth';
  const auth = useAuthStore();
  </script>