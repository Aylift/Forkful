<template>
  <nav class="absolute top-0 w-full z-10 bg-transparent">
    <div class="px-6 py-4">
      <div class="flex items-center justify-between">

        <div class="flex space-x-6">
          <router-link 
            to="/" 
            class="text-white font-medium px-4 py-2 rounded-full hover:bg-white/20 transition-all duration-200"
          >
            Home
          </router-link>
          
          <router-link 
            v-if="!auth.isAuthenticated" 
            to="/loginregister" 
            class="text-white font-medium px-4 py-2 rounded-full hover:bg-white/20 transition-all duration-200"
          >
            Login/Register
          </router-link>
          
          <router-link 
            v-else
            to="/profile" 
            class="text-white font-medium px-4 py-2 rounded-full hover:bg-white/20 transition-all duration-200"
          >
            {{ auth.user?.username || 'Profile' }}
          </router-link>
          <button 
            v-if="auth.isAuthenticated"
            @click="auth.logout"
            class="text-white font-medium px-4 py-2 rounded-full hover:bg-white/20 transition-all duration-200"
          >
            Logout
          </button>
        </div>
        
        <!-- TODO: Add logo -->
        <div class="text-white font-bold text-xl">
          🍎 WellnessApp
        </div>
      </div>
    </div>
  </nav>
</template>


<script setup>
import { useAuthStore } from '@/stores/auth';
import { onMounted } from 'vue';

const auth = useAuthStore();

onMounted(() => {
  if (auth.token && !auth.user) {
    auth.fetchUser();
  }
})

</script>

<style scoped>

</style>