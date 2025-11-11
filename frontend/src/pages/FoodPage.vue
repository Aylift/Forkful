<template>
  <div v-if="meal">
    <h1>{{ meal.name }}</h1>
    <p>{{ meal.description }}</p>

    <h2>Ingredients</h2>
    <ul>
      <li v-for="(mi, index) in meal.meal_ingredients" :key="index">
        {{ mi.ingredient.name }} - {{ mi.amount_in_grams }}g
      </li>
    </ul>

    <h2>Total Nutrients</h2>
    <ul>
      <li>{{ meal.total_nutrients.Calories.amount }} {{ meal.total_nutrients.Calories.unit }}</li>
      <li>Protein: {{ meal.total_nutrients.Protein.amount }} {{ meal.total_nutrients.Protein.unit }}</li>
      <li>Fat: {{ meal.total_nutrients.Fat.amount }} {{ meal.total_nutrients.Fat.unit }}</li>
      <li>Carbs: {{ meal.total_nutrients.Carbohydrates.amount }} {{ meal.total_nutrients.Carbohydrates.unit }}</li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const meal = ref(null)

onMounted(async () => {
  const res = await axios.get('http://localhost:8000/api/meals/1/')
  meal.value = res.data
})
</script>