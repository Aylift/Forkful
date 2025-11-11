<template>
  <nav class="absolute top-0 w-full z-10 bg-transparent">
    <div class="px-6 py-4">
      <div class="flex items-center justify-between">

        <div class="flex items-center space-x-6">
          <router-link 
            to="/" 
            class="text-white font-medium px-4 py-2 rounded-full hover:bg-white/20 transition-all duration-200"
          >
            Home
          </router-link>
          
          <template v-if="auth.isAuthenticated">
            <router-link 
              to="/dashboard" 
              class="text-white font-medium px-4 py-2 rounded-full hover:bg-white/20 transition-all duration-200"
            >
              Dashboard
            </router-link>
            <router-link 
              to="/meals" 
              class="text-white font-medium px-4 py-2 rounded-full hover:bg-white/20 transition-all duration-200"
            >
              Meal Library
            </router-link>
          </template>
        </div>

        <div class="flex items-center space-x-6">
          <template v-if="auth.isAuthenticated">
            <router-link 
              to="/profile" 
              class="text-white font-medium px-4 py-2 rounded-full hover:bg-white/20 transition-all duration-200"
            >
              {{ auth.user?.user?.username || 'Profile' }}
            </router-link>
            <button 
              @click="handleLogout"
              class="text-white font-medium px-4 py-2 rounded-full bg-orange-500 hover:bg-orange-600 transition-all duration-200"
            >
              Logout
            </button>
          </template>
          
          <template v-else>
            <router-link 
              to="/loginregister" 
              class="text-white font-medium px-4 py-2 rounded-full bg-orange-500 hover:bg-orange-600 transition-all duration-200"
            >
              Login/Register
            </router-link>
          </template>
          <div class="text-white font-bold text-xl">
            🍴 Forkful
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';

const auth = useAuthStore();
const router = useRouter();

const handleLogout = () => {
  auth.logout();
  router.push('/');
};
</script>

<style scoped>
</style>