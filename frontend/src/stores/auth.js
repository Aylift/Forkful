import { defineStore } from 'pinia';
import api from '@/axios';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: null,
    isLoading: false,
    error: null
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
  },

  actions: {
    async login(username, password) {
      this.isLoading = true;
      this.error = null;
      
      try {
        const response = await api.post('/api/auth/login/', { username, password });
        this.token = response.data.access;
        localStorage.setItem('token', this.token);
        api.defaults.headers.common['Authorization'] = `Bearer ${this.token}`;
        await this.fetchUser();
        
        return { success: true };
      } catch (error) {
        if (error.response?.data) {
          this.error = error.response.data;
        }
        console.log('ERROR LOGIN:', this.error)
        return { success: false, error: this.error };
      } finally {
        this.isLoading = false;
      }
    },

    async register(username, password, password_repeat, email) {
      this.isLoading = true;
      this.error = null;
      
      try {
        await api.post('/api/auth/register/', { 
          username, 
          password, 
          password_repeat, 
          email 
        });
        
        await this.login(username, password);
        
        return { success: true };
      } catch (error) {
        if (error.response?.data) {
          this.error = error.response.data;
        }
        console.log('ERROR REGISTER', this.error)
        return { success: false, error: this.error };
      } finally {
        this.isLoading = false;
      }
    },

    async fetchUser() {
      if (!this.token) return;
      
      this.isLoading = true;
      
      try {
        const response = await api.get('/api/auth/check/');
        this.user = response.data;
      } catch (error) {
        if (error.response?.status === 401) {
          this.logout();
        }
      } finally {
        this.isLoading = false;
      }
    },

    logout() {
      this.token = null;
      this.user = null;
      this.error = null;
      localStorage.removeItem('token');
      delete api.defaults.headers.common['Authorization'];
    },
    
    async initializeAuth() {
      if (this.token) {
        api.defaults.headers.common['Authorization'] = `Bearer ${this.token}`;
        await this.fetchUser();
      }
    },
    
    clearError() {
      this.error = null;
    }
  },
});