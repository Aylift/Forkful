<template>
    <div class="max-w-sm mx-auto p-6 border bg-white rounded-lg shadow-xl">
      <h2 class="text-xl font-bold mb-4">Register</h2>
      
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
      
      <div class="mb-3">
        <input 
          type="password"
          v-model="password" 
          placeholder="Password" 
          class="w-full px-3 py-2 border rounded"
        />
        <p v-if="auth.error?.password" class="text-red-500 text-sm"> {{ auth.error.password[0] }} </p>
      </div>
      
      <div class="mb-3">
        <input 
          type="password"
          v-model="password_repeat" 
          placeholder="Repeat password" 
          class="w-full px-3 py-2 border rounded"
        />
        <p v-if="auth.error?.password_repeat" class="text-red-500 text-sm"> {{ auth.error.password_repeat[0] }} </p>
      </div>
      
      <div class="mb-4">
        <input 
          type="email"
          v-model="email" 
          placeholder="Email" 
          class="w-full px-3 py-2 border rounded"
        />
        <p v-if="auth.error?.email" class="text-red-500 text-sm"> {{ auth.error.email[0] }} </p>
      </div>
      
      <div class="m-2 mt-8 mb-8">
        <p v-if="auth.error?.detail || auth.error?.non_field_errors " class="text-red-500 text-sm text-center">
          {{ auth.error?.detail || auth.error?.non_field_errors[0] }}
        </p>
      </div>

      <button 
        @click="registerUser"
        :disabled="auth.isLoading"
        class="w-full bg-white text-orange-500 py-2 rounded font-medium hover:bg-orange-50 transition-colors duration-200 disabled:opacity-50"
      >
        {{ auth.isLoading ? 'Registering...' : 'Register' }}
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
const email = ref('');
const successMessage = ref('');

const router = useRouter();
const auth = useAuthStore();

const registerUser = async () => {
  auth.clearError();
  successMessage.value = '';

  const result = await auth.register(username.value, password.value, password_repeat.value, email.value);

  if (result.success && auth.token) {
        successMessage.value = 'Registration successful! Redirecting...';
        setTimeout(() => {
            router.push('/profile');
        }, 1500);
    }
}

</script>

<style scoped>

</style>