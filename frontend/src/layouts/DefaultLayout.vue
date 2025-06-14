<script setup>
import AppNavbar from "@/components/AppNavbar.vue";
</script>

<template>
  <div>
    <AppNavbar />
    <main>
      <router-view />
    </main>
  </div>
</template>

<style scoped>
  main {
    padding: 2rem;
  }
</style>