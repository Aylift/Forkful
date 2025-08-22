<template>
    <div>
        <input v-model="username" placeholder="Username" />
        <input v-model="password" placeholder="Password" />
        <input v-model="password_repeat" placeholder="Repeat password" />
        <input v-model="mail" placeholder="Mail" />
        <button @click="registerUser">Register</button>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const username = ref('');
const password = ref('');
const password_repeat = ref('');
const mail = ref('');

const router = useRouter();
const auth = useAuthStore();

const registerUser = async () => {
    await auth.register(username.value, password.value, password_repeat.value, mail.value);
    if (auth.token) router.push('/profile');
}

</script>

<style scoped>

</style>