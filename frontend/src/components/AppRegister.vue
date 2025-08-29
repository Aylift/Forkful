<template>
    <div class="max-w-sm mx-auto p-6 border bg-white rounded-lg shadow-xl">
      <h2 class="text-xl font-bold mb-4">Register</h2>
      
      <div class="mb-3">
        <input 
          v-model="username" 
          placeholder="Username" 
          class="w-full px-3 py-2 border rounded"
        />
      </div>
      
      <div class="mb-3">
        <input 
          type="password"
          v-model="password" 
          placeholder="Password" 
          class="w-full px-3 py-2 border rounded"
        />
      </div>
      
      <div class="mb-3">
        <input 
          type="password"
          v-model="password_repeat" 
          placeholder="Repeat password" 
          class="w-full px-3 py-2 border rounded"
        />
      </div>
      
      <div class="mb-4">
        <input 
          type="email"
          v-model="mail" 
          placeholder="Email" 
          class="w-full px-3 py-2 border rounded"
        />
      </div>
      
      <button 
        @click="registerUser"
        class="w-full bg-white text-orange-500 py-2 rounded font-medium hover:bg-orange-50 transition-colors duration-200"
      >
        Register
      </button>
    </div>
  </template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const username = ref('');
const password = ref('');
const password_repeat = ref('');
const mail = ref('');

const router = useRouter();
const auth = useAuthStore();

const registerUser = async () => {
    await auth.register(username.value, password.value, password_repeat.value, mail.value);
    if (auth.token) router.push('/profile');
}

</script>

<style scoped>

</style>