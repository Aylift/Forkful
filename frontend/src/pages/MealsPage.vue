<template>
  <div classfs="p-4 md:p-8 max-w-7xl mx-auto">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-white">Your Meals Dashboard</h1>
      <button @click="openCreateModal"
        class="px-5 py-2 bg-orange-500 text-white font-medium rounded hover:bg-orange-600 transition-colors">
        + Create New Meal
      </button>
    </div>

    <div v-if="isLoading" class="text-center text-white">
      <p>Loading meals...</p>
    </div>

    <div v-if="error" class="bg-red-900 text-white p-4 rounded-lg">
      <p><strong>Error:</strong> {{ error }}</p>
    </div>

    <div v-if="!isLoading && meals.length > 0" class="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
      <div v-for="meal in meals" :key="meal.id" class="bg-gray-800 text-white rounded-lg shadow-lg overflow-hidden">
        <div class="p-6">
          <div class="flex justify-between items-start">
            <h2 class="text-2xl font-semibold mb-2">{{ meal.name }}</h2>
            <div class="flex-shrink-0 flex gap-2">
              <button @click="openEditModal(meal)"
                class="text-sm text-orange-400 hover:text-orange-300 transition-colors">Edit</button>
              <button @click="handleDeleteMeal(meal.id)"
                class="text-sm text-red-400 hover:text-red-300 transition-colors">Delete</button>
            </div>
          </div>
          <p class="text-gray-400 mb-4">{{ meal.description || 'No description.' }}</p>

          <div class="mb-4">
            <h3 class="text-lg font-semibold mb-2">Ingredients</h3>
            <ul v-if="meal.meal_ingredients.length > 0" class="list-disc list-inside text-gray-300 space-y-1">
              <li v-for="ing in meal.meal_ingredients" :key="ing.ingredient.id">
                {{ ing.ingredient.name }} ({{ ing.amount_in_grams }}g)
              </li>
            </ul>
            <p v-else class="text-gray-500">No ingredients added.</p>
          </div>

          <div>
            <h3 class="text-lg font-semibold mb-2">Total Nutrients</h3>
            <div v-if="Object.keys(meal.total_nutrients).length > 0" class="grid grid-cols-2 gap-x-4 gap-y-1">
              <div v-for="(nutrient, name) in meal.total_nutrients" :key="name"
                class="text-sm text-gray-300 flex justify-between">
                <span>{{ name }}:</span>
                <span class="font-medium">{{ nutrient.amount.toFixed(1) }} {{ nutrient.unit }}</span>
              </div>
            </div>
            <p v-else class="text-gray-500">No nutrient data.</p>
          </div>
        </div>
      </div>
    </div>

    <div v-if="!isLoading && meals.length === 0" class="text-center bg-gray-800 text-white p-10 rounded-lg">
      <h2 class="text-2xl font-semibold mb-2">No Meals Found</h2>
      <p class="text-gray-400">Get started by creating a new meal!</p>
    </div>

    <div v-if="showModal"
      class="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4 transition-opacity">
      <div class="bg-gray-800 text-white rounded-lg p-8 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <form @submit.prevent="handleSaveMeal">
          <h2 class="text-2xl font-bold mb-6">{{ isEditing ? 'Edit Meal' : 'Create New Meal' }}</h2>

          <div class="space-y-4">
            <FormInput label="Meal Name" v-model="form.name" required />
            <FormInput label="Description" v-model="form.description" />
          </div>

          <h3 class="text-xl font-semibold mt-8 mb-4">Ingredients</h3>
          <div v-if="form.meal_ingredients.length === 0" class="text-gray-500 mb-4">
            No ingredients added yet.
          </div>

          <div v-for="(ing, index) in form.meal_ingredients" :key="index" class="flex gap-2 items-end mb-3">
            <div class="flex-grow">
              <label class="block text-sm font-medium text-gray-300 mb-1">Ingredient</label>
              <select v-model.number="ing.ingredient_id"
                class="block w-full bg-gray-700 text-white border border-gray-600 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-orange-500"
                required>
                <option :value="null" disabled>Select an ingredient</option>
                <option v-for="ingredient in allIngredients" :key="ingredient.id" :value="ingredient.id">
                  {{ ingredient.name }}
                </option>
              </select>
            </div>

            <div class="w-1/4">
              <FormInput label="Amount (g)" v-model.number="ing.amount_in_grams" type="number" step="0.1" required />
            </div>

            <button @click.prevent="removeIngredientFromForm(index)"
              class="px-3 py-2 bg-red-600 text-white rounded hover:bg-red-700 h-[42px] flex-shrink-0">
              Remove
            </button>
          </div>

          <button @click.prevent="addIngredientToForm"
            class="mt-2 text-sm px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-500">
            + Add Ingredient
          </button>

          <div class="mt-8 flex justify-end gap-4">
            <button @click.prevent="closeModal" type="button"
              class="px-5 py-2 bg-gray-600 text-white rounded hover:bg-gray-500">
              Cancel
            </button>
            <button type="submit" :disabled="isSaving"
              class="px-5 py-2 bg-orange-500 text-white rounded hover:bg-orange-600 disabled:bg-gray-500">
              {{ isSaving ? 'Saving...' : 'Save Meal' }}
            </button>
          </div>
        </form>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/axios';
import FormInput from '@/components/FormInput.vue';

const meals = ref([]);
const allIngredients = ref([]);
const isLoading = ref(true);
const isSaving = ref(false);
const error = ref(null);

const showModal = ref(false);
const isEditing = ref(false);
const form = ref(getFreshForm());

function getFreshForm() {
  return {
    id: null,
    name: '',
    description: '',
    meal_ingredients: []
  };
}

async function fetchMeals() {
  try {
    const response = await api.get('/api/meals/');
    meals.value = response.data;
  } catch (err) {
    error.value = 'Failed to load meals. ' + (err.response?.data?.detail || err.message);
  }
}

async function fetchIngredients() {
  try {
    const response = await api.get('/api/ingredients/');
    allIngredients.value = response.data;
  } catch (err) {
    error.value = 'Failed to load ingredients. ' + (err.response?.data?.detail || err.message);
  }
}

async function handleSaveMeal() {
  isSaving.value = true;
  error.value = null;

  const payload = {
    name: form.value.name,
    description: form.value.description,
    meal_ingredients: form.value.meal_ingredients
  };

  try {
    if (isEditing.value) {
      const response = await api.put(`/api/meals/${form.value.id}/`, payload);
      const index = meals.value.findIndex(m => m.id === form.value.id);
      if (index !== -1) {
        meals.value[index] = response.data;
      }
    } else {
      const response = await api.post('/api/meals/', payload);
      meals.value.unshift(response.data);
    }
    closeModal();
  } catch (err) {
    error.value = 'Failed to save meal. ' + (err.response?.data?.detail || JSON.stringify(err.response?.data) || err.message);
  } finally {
    isSaving.value = false;
  }
}

async function handleDeleteMeal(mealId) {
  if (!window.confirm('Are you sure you want to delete this meal?')) {
    return;
  }

  try {
    await api.delete(`/api/meals/${mealId}/`);
    meals.value = meals.value.filter(m => m.id !== mealId);
  } catch (err) {
    error.value = 'Failed to delete meal. ' + (err.response?.data?.detail || err.message);
  }
}

function openCreateModal() {
  isEditing.value = false;
  form.value = getFreshForm();
  showModal.value = true;
}

function openEditModal(meal) {
  isEditing.value = true;
  form.value = {
    id: meal.id,
    name: meal.name,
    description: meal.description,
    meal_ingredients: meal.meal_ingredients.map(ing => ({
      ingredient_id: ing.ingredient.id,
      amount_in_grams: ing.amount_in_grams
    }))
  };
  showModal.value = true;
}

function closeModal() {
  showModal.value = false;
  error.value = null;
}

function addIngredientToForm() {
  form.value.meal_ingredients.push({
    ingredient_id: null,
    amount_in_grams: ''
  });
}

function removeIngredientFromForm(index) {
  form.value.meal_ingredients.splice(index, 1);
}

onMounted(async () => {
  isLoading.value = true;
  error.value = null;
  await Promise.all([
    fetchMeals(),
    fetchIngredients()
  ]);
  isLoading.value = false;
});
</script>

<style scoped>
</style>