<template>
    <div class="text-center">
      <dt class="text-sm font-medium text-gray-400">{{ label }}</dt>
      <dd class="text-2xl font-semibold text-white">{{ value }}</dd>
    </div>
  </template>
  
  <script setup>
  defineProps({
    label: String,
    value: [String, Number]
  });
  </script>