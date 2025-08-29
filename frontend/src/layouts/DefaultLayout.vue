<template>
  <div>
    <AppNavbar />
    <main class="min-h-screen bg-gradient-to-br from-orange-300 to-orange-500">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import AppNavbar from "@/components/AppNavbar.vue";
</script>

<style scoped>
main {
  animation: gradientShift 8s ease infinite;
  background-size: 400% 400%;
}

@keyframes gradientShift {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}
</style>