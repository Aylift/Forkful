<template>
  <div class="p-8">
    <div class="mb-4 flex gap-2">
      <button 
        @click="showLogin = true"
        class="px-4 py-2 border rounded"
        :class="showLogin ? 'bg-blue-500 text-white' : 'bg-white'"
      >
        Login
      </button>
      <button 
        @click="showLogin = false"
        class="px-4 py-2 border rounded"
        :class="!showLogin ? 'bg-blue-500 text-white' : 'bg-white'"
      >
        Register
      </button>
    </div>
    
    <AppLogin v-if="showLogin" />
    <AppRegister v-else />
  </div>
</template>
  
<script setup>
import { ref } from 'vue';
import AppLogin from '@/components/AppLogin.vue';
import AppRegister from '@/components/AppRegister.vue';

const showLogin = ref(true);
</script>

<style scoped>

</style>