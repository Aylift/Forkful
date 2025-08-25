import { defineStore } from 'pinia';
import api from "@/axios";


export const useAuthStore = defineStore('auth', {
    state: () => ({
        token: localStorage.getItem('token') || null,
        user: null,
    }),

    // TODO: add try catch blocks, to catch errors
    // TODO: add loading states

    getters: {
        isAuthenticated: (state) => !!state.token,
    },

    actions: {
        async login(username, password) {
            const response = await api.post('/api/auth/login/', { username, password});
            this.token = response.data.access;
            localStorage.setItem('token', this.token);
            await this.fetchUser();
        },

        async register(username, password, password_repeat, email) {
            await api.post('/api/auth/register/', {username, password, password_repeat, email});
            await this.login(username, password);
        },

        async fetchUser() {
            if (!this.token) return;
            const response = await api.get('/api/auth/check/');
            this.user = response.data;
        },

        logout() {
            this.token = null;
            this.user = null;
            localStorage.removeItem('token');
        },
    },
});