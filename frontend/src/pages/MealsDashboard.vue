<template>
    <div class="p-4 md:p-8 max-w-4xl mx-auto text-white">
      <div class="flex flex-col md:flex-row justify-between md:items-center gap-4 mb-6">
        <h1 class="text-3xl font-bold">Food Log</h1>
        <div class="flex items-center gap-2">
          <label for="log-date" class="font-medium">Selected Date:</label>
          <input 
            type="date" 
            id="log-date" 
            v-model="selectedDate" 
            @change="fetchLogEntries"
            class="bg-gray-700 text-white border border-gray-600 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-orange-500"
          >
        </div>
      </div>
  
      <div class="bg-gray-800 p-6 rounded-lg shadow-lg mb-8">
        <h2 class="text-2xl font-semibold mb-4 text-center">Today's Summary</h2>
        <div class="text-center mb-4">
          <span class="text-5xl font-bold text-orange-400">{{ consumedCalories.toFixed(0) }}</span>
          <span class="text-xl text-gray-400"> / {{ targetCalories }} kcal</span>
        </div>
        <div class="w-full bg-gray-700 rounded-full h-4">
          <div 
            class="bg-orange-500 h-4 rounded-full transition-all duration-500" 
            :style="{ width: calorieProgress + '%' }"
          ></div>
        </div>
      </div>
  
      <div class="bg-gray-800 p-6 rounded-lg shadow-lg">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-2xl font-semibold">Logged Meals</h2>
          <button 
            @click="openAddModal"
            class="px-5 py-2 bg-orange-500 text-white font-medium rounded hover:bg-orange-600 transition-colors"
          >
            + Add Meal
          </button>
        </div>
  
        <div v-if="isLoading" class="text-center text-gray-400">Loading entries...</div>
        <div v-if="!isLoading && dailyEntries.length === 0" class="text-center text-gray-400">
          No meals logged for this day.
        </div>
  
        <ul v-else class="divide-y divide-gray-700">
          <li v-for="entry in dailyEntries" :key="entry.id" class="py-4 flex justify-between items-center">
            <div>
              <h3 class="text-xl font-medium">{{ entry.meal.name }}</h3>
              <p class="text-gray-400">
                {{ entry.servings }} serving(s)
                &bull; 
                {{ (getMealCalories(entry.meal) * entry.servings).toFixed(0) }} kcal
              </p>
            </div>
            <button @click="handleDeleteEntry(entry.id)" class="text-sm text-red-400 hover:text-red-300">
              Remove
            </button>
          </li>
        </ul>
      </div>
  
      <div v-if="showModal" class="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
        <div class="bg-gray-800 text-white rounded-lg p-8 w-full max-w-md">
          <form @submit.prevent="handleAddEntry">
            <h2 class="text-2xl font-bold mb-6">Add Meal to Log</h2>
            
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-1">Meal</label>
                <select v-model.number="logForm.meal_id"
                  class="block w-full bg-gray-700 text-white border border-gray-600 rounded px-3 py-2" required>
                  <option :value="null" disabled>Select a meal</option>
                  <option v-for="meal in allMeals" :key="meal.id" :value="meal.id">
                    {{ meal.name }}
                  </option>
                </select>
              </div>
              
              <FormInput 
                label="Servings" 
                type="number" 
                step="0.1" 
                v-model.number="logForm.servings" 
                required 
              />
            </div>
  
            <div class="mt-8 flex justify-end gap-4">
              <button @click.prevent="showModal = false" type="button"
                class="px-5 py-2 bg-gray-600 rounded hover:bg-gray-500">
                Cancel
              </button>
              <button type="submit" :disabled="isSaving"
                class="px-5 py-2 bg-orange-500 rounded hover:bg-orange-600 disabled:bg-gray-500">
                {{ isSaving ? 'Logging...' : 'Log Meal' }}
              </button>
            </div>
          </form>
        </div>
      </div>
  
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, computed } from 'vue';
  import { useAuthStore } from '@/stores/auth';
  import api from '@/axios';
  import FormInput from '@/components/FormInput.vue';
  
  const auth = useAuthStore();
  const dailyEntries = ref([]);
  const allMeals = ref([]);
  const selectedDate = ref(new Date().toISOString().split('T')[0]);
  const isLoading = ref(true);
  const isSaving = ref(false);
  
  const showModal = ref(false);
  const logForm = ref({
    meal_id: null,
    servings: 1.0
  });
  
  const targetCalories = computed(() => {
    return auth.user?.user?.profile?.target_calories || 0;
  });
  
  const consumedCalories = computed(() => {
    return dailyEntries.value.reduce((sum, entry) => {
      const mealCals = getMealCalories(entry.meal);
      return sum + (mealCals * entry.servings);
    }, 0);
  });
  
  const calorieProgress = computed(() => {
    if (targetCalories.value === 0) return 0;
    const progress = (consumedCalories.value / targetCalories.value) * 100;
    return Math.min(progress, 100);
  });
  
  function getMealCalories(meal) {
    return meal.total_nutrients?.Calories?.amount || 0;
  }
  
  async function fetchLogEntries() {
    isLoading.value = true;
    try {
      const response = await api.get(`/api/daily-entries/?date=${selectedDate.value}`);
      dailyEntries.value = response.data;
    } catch (error) {
      console.error('Failed to fetch log entries:', error);
    } finally {
      isLoading.value = false;
    }
  }
  
  async function fetchAllMeals() {
    try {
      const response = await api.get('/api/meals/');
      allMeals.value = response.data;
    } catch (error) {
      console.error('Failed to fetch all meals:', error);
    }
  }
  
  async function handleAddEntry() {
    isSaving.value = true;
    try {
      const payload = {
        ...logForm.value,
        date: selectedDate.value
      };
      const response = await api.post('/api/daily-entries/', payload);
      dailyEntries.value.unshift(response.data);
      showModal.value = false;
    } catch (error) {
      console.error('Failed to add entry:', error);
    } finally {
      isSaving.value = false;
    }
  }
  
  async function handleDeleteEntry(entryId) {
    if (!window.confirm('Are you sure you want to remove this entry?')) {
      return;
    }
    try {
      await api.delete(`/api/daily-entries/${entryId}/`);
      dailyEntries.value = dailyEntries.value.filter(e => e.id !== entryId);
    } catch (error) {
      console.error('Failed to delete entry:', error);
    }
  }
  
  function openAddModal() {
    logForm.value = { meal_id: null, servings: 1.0 };
    showModal.value = true;
  }
  
  onMounted(() => {
    fetchLogEntries();
    fetchAllMeals();
  });
  </script>