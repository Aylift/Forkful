<template>
  <nav class="navbar">
    <router-link to="/">Home</router-link>
    <router-link to="/food">Food</router-link>
    <!-- TODO conditionally redirect to either profile or loginregister, display -->
    <router-link class="profile-link" to="/profile">Profile</router-link>
  </nav>
</template>

<script setup>

</script>

<style scoped>
  .navbar {
    background: #2c3e50;
    padding: 1rem;
  }

  .navbar a {
    color: white;
    margin-right: 1rem;
    margin-left: 1rem;
    text-decoration: none;
  }

  .profile-link {
    float: right;
  }
</style>