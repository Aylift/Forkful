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
            to="/loginregister" 
            class="text-white font-medium px-4 py-2 rounded-full hover:bg-white/20 transition-all duration-200"
          >
            Login
          </router-link>
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
/* .navbar {
  background: #2c3e50;
  padding: 1rem;
}

.navbar a {
  color: white;
  margin-right: 1rem;
  margin-left: 1rem;
  text-decoration: none;
}

.profile-link {
  float: right;
} */
</style>