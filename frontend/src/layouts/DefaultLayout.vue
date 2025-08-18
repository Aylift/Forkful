<template>
  <div>
    <AppNavbar />
    <main>
      <router-view />
    </main>
  </div>
</template>

<script setup>
import AppNavbar from "@/components/AppNavbar.vue";
</script>

<style scoped>
  main {
    padding: 2rem;
  }
</style>