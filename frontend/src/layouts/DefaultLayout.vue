<template>
  <div class="app-wrapper min-h-screen bg-gradient-to-br from-yellow-400 via-orange-400 to-red-400">
    <AppNavbar />
    
    <main class="pt-20">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import AppNavbar from "@/components/AppNavbar.vue";
</script>

<style scoped>
.app-wrapper {
  animation: gradientShift 8s ease infinite;
  background-size: 400% 400%;
}

@keyframes gradientShift {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}
</style>