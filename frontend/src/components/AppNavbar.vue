<script setup>

</script>

<template>
  <nav class="navbar">
    <router-link to="/">Home</router-link>
    <router-link to="/about">About</router-link>
  </nav>
</template>

<style scoped>
  .navbar {
    background: #2c3e50;
    padding: 1rem;
  }
  .navbar a {
    color: white;
    margin-right: 1rem;
    text-decoration: none;
  }
</style>