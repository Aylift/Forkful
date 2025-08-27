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
        
        // Store token in localStorage for persistence
        localStorage.setItem('token', this.token);
        
        // Set token in axios headers for future requests
        api.defaults.headers.common['Authorization'] = `Bearer ${this.token}`;
        
        // Fetch user data after successful login
        await this.fetchUser();
        
        return { success: true };
      } catch (error) {
        this.error = error.response?.data?.detail || 'Login failed';
        console.error('Login error:', error);
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
        
        // Auto-login after successful registration
        await this.login(username, password);
        
        return { success: true };
      } catch (error) {
        this.error = error.response?.data?.detail || 
                     error.response?.data?.username?.[0] || 
                     error.response?.data?.email?.[0] || 
                     'Registration failed';
        console.error('Registration error:', error);
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
        console.error('Failed to fetch user:', error);
        // If fetching user fails, token might be invalid
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
      
      // Remove token from localStorage
      localStorage.removeItem('token');
      
      // Remove token from axios headers
      delete api.defaults.headers.common['Authorization'];
    },
    
    // Initialize auth state on app start
    async initializeAuth() {
      if (this.token) {
        // Set token in axios headers
        api.defaults.headers.common['Authorization'] = `Bearer ${this.token}`;
        
        // Try to fetch user data
        await this.fetchUser();
      }
    },
    
    // Clear any errors
    clearError() {
      this.error = null;
    }
  },
});