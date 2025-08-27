<template>
  <nav class="navbar">
    <div>
      <template v-if="auth.isAuthenticated">
        <router-link to="/">Home</router-link>
        <router-link to="/food">Food</router-link>
        <router-link class="profile-link" to="/profile">
          {{ auth.user?.username || 'Profile' }}
        </router-link>
        <button @click="auth.logout">Logout</button>
      </template>
      <template v-else>
        <router-link to="/">Home</router-link>
        <router-link to="/loginregister">Login</router-link>
      </template>
    </div>
  </nav>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth';
import { onMounted } from 'vue';

const auth = useAuthStore();

onMounted(() => {
  if (auth.token && !auth.user) {
    auth.fetchUser();
  }
})

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