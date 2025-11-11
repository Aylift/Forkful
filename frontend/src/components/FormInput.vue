<template>
    <div>
      <label class="block text-sm font-medium text-gray-300 mb-1">{{ label }}</label>
      <input 
        :type="type || 'text'"
        :value="modelValue"
        @input="$emit('update:modelValue', $event.target.value)"
        :disabled="disabled"
        :step="step"
        class="block w-full bg-gray-700 text-white border border-gray-600 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-orange-500 disabled:bg-gray-600 disabled:cursor-not-allowed"
      >
    </div>
  </template>
  
  <script setup>
  defineProps({
    label: String,
    modelValue: [String, Number],
    type: String,
    disabled: Boolean,
    step: String
  });
  defineEmits(['update:modelValue']);
  </script>