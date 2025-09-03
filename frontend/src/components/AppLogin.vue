<template>
    <div class="max-w-sm mx-auto p-6 border bg-white rounded-lg shadow-xl">
      <h2 class="text-xl font-bold mb-4">Login</h2>
      
      <div v-if="successMessage" class="mb-4 p-3 bg-green-500 text-white rounded text-center">
        {{ successMessage }}
      </div>

      <div class="mb-3">
        <input 
          v-model="username" 
          placeholder="Username" 
          class="w-full px-3 py-2 border rounded"
        />
        <p v-if="auth.error?.username" class="text-red-500 text-sm"> {{ auth.error.username[0] }} </p>
      </div>
      
      <div class="mb-4">
        <input 
          type="password"
          v-model="password" 
          placeholder="Password" 
          class="w-full px-3 py-2 border rounded"
        />
        <p v-if="auth.error?.password" class="text-red-500 text-sm">
          {{ auth.error.password[0] }}
        </p>
      </div>
      
      <div class="m-2 mt-8 mb-8">
        <p v-if="auth.error?.detail " class="text-red-500 text-sm text-center">
          {{ auth.error?.detail }}
        </p>
      </div>

      <button 
        @click="loginUser"
        :disabled="auth.isLoading"
        class="w-full bg-white text-orange-500 py-2 rounded font-medium hover:bg-orange-50 transition-colors duration-200 disabled:opacity-50"
      >
        {{ auth.isLoading ? 'Logging in...' : 'Login' }}
      </button>
    </div>
  </template>
<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const username = ref('');
const password = ref('');
const successMessage = ref('');

const router = useRouter();
const auth = useAuthStore();

const loginUser = async () => {
  auth.clearError();
  successMessage.value = '';

  const result = await auth.login(username.value, password.value);

  if (result.success && auth.token) {
        successMessage.value = 'Logged in successfully! Redirecting...';
        setTimeout(() => {
            router.push('/profile');
        }, 1500);
    }
}

</script>

<style scoped>

</style>