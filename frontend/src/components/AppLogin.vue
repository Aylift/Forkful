<template>
    <div>
        <input v-model="username" placeholder="Username" />
        <input v-model="password" placeholder="Password" />
        <button @click="loginUser">Login</button>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const username = ref('');
const password = ref('');

const router = useRouter();
const auth = useAuthStore();

const loginUser = async () => {
    await auth.login(username.value, password.value);
    if (auth.token) router.push('/profile');
}

</script>

<style scoped>

</style>