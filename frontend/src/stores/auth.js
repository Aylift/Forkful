import { defineStore } from 'pinia';
import axios from 'axios';


export const useAuthStore = defineStore('auth', {
    state: () => ({
        token: localStorage.getItem('token') || null,
        user: null,
    }),

    // TODO: add try catch blocks, to catch errors

    actions: {
        async login(username, password) {
            const response = await axios.post('/api/auth/login/', { username, password});
            this.token = response.data.access;
            localStorage.setItem('token', this.token);
            await this.fetchUser();
        },

        async register(username, password, password_repeat, email) {
            await axios.post('/api/auth/register/', {username, password, password_repeat, email});
            await this.login(username, password);
        },

        async fetchUser() {
            if (!this.token) return;
            const response = await axios.get('/api/auth/check/');
            this.user = response.data;
        },

        logout() {
            this.token = null;
            this.user = null;
            localStorage.removeItem('token');
        },
    },
});