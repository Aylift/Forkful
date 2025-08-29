<template>
    <div class="max-w-sm mx-auto p-6 border bg-white rounded-lg shadow-xl">
      <h2 class="text-xl font-bold mb-4">Login</h2>
      
      <div class="mb-3">
        <input 
          v-model="username" 
          placeholder="Username" 
          class="w-full px-3 py-2 border rounded"
        />
      </div>
      
      <div class="mb-4">
        <input 
          type="password"
          v-model="password" 
          placeholder="Password" 
          class="w-full px-3 py-2 border rounded"
        />
      </div>
      
      <button 
        @click="loginUser"
        class="w-full bg-white text-orange-500 py-2 rounded font-medium hover:bg-orange-50 transition-colors duration-200"
      >
        Login
      </button>
    </div>
  </template>
<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const username = ref('');
const password = ref('');

const router = useRouter();
const auth = useAuthStore();

const loginUser = async () => {
    await auth.login(username.value, password.value);
    if (auth.token) router.push('/profile');
}

</script>

<style scoped>

</style>