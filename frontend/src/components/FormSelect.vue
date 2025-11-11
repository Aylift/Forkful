<template>
    <div>
      <label class="block text-sm font-medium text-gray-300 mb-1">{{ label }}</label>
      <select
        :value="modelValue"
        @change="$emit('update:modelValue', $event.target.value)"
        class="block w-full bg-gray-700 text-white border border-gray-600 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-orange-500"
      >
        <option v-for="option in options" :key="option.value" :value="option.value">
          {{ option.text }}
        </option>
      </select>
    </div>
  </template>
  
  <script setup>
  defineProps({
    label: String,
    modelValue: [String, Number],
    options: Array
  });
  defineEmits(['update:modelValue']);
  </script>