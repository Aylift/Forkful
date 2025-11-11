<template>
  <div class="p-4 md:p-8 max-w-4xl mx-auto text-white">
    <div v-if="auth.isLoading && !user" class="text-center">
      <p>Loading profile...</p>
    </div>

    <div v-else-if="user" class="space-y-8">
      <h1 class="text-3xl font-bold mb-6">Your Profile</h1>

      <form @submit.prevent="handleUserUpdate" class="bg-gray-800 p-6 rounded-lg shadow-lg">
        <h2 class="text-2xl font-semibold mb-4">Account Details</h2>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <FormInput label="Username" v-model="user.username" :disabled="true" />
          <FormInput label="Email" v-model="user.email" :disabled="true" />
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <FormInput label="First Name" v-model="userForm.first_name" />
          <FormInput label="Last Name" v-model="userForm.last_name" />
          <FormInput label="Phone Number" v-model="userForm.phone_number" />
          <FormInput label="Address" v-model="userForm.address" />
        </div>

        <div class="mt-6">
          <button type="submit" :disabled="isUpdatingUser"
            class="px-5 py-2 bg-orange-500 text-white font-medium rounded hover:bg-orange-600 disabled:bg-gray-500 transition-colors">
            {{ isUpdatingUser ? 'Saving...' : 'Save Account Details' }}
          </button>
          <p v-if="userUpdateSuccess" class="text-green-400 mt-2">Account updated successfully!</p>
          <p v-if="userUpdateError" class="text-red-400 mt-2">{{ userUpdateError }}</p>
        </div>
      </form>

      <form v-if="profile" @submit.prevent="handleProfileUpdate" class="bg-gray-800 p-6 rounded-lg shadow-lg">
        <h2 class="text-2xl font-semibold mb-4">Fitness Profile</h2>
        
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6 bg-gray-700 p-4 rounded-md">
          <StatDisplay label="Age" :value="profile.age || 'N/A'" />
          <StatDisplay label="BMI" :value="profile.bmi || 'N/A'" />
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <FormInput label="Height (cm)" type="number" v-model.number="profileForm.height" />
          <FormInput label="Weight (kg)" type="number" step="0.1" v-model.number="profileForm.weight" />
          <FormInput label="Date of Birth" type="date" v-model="profileForm.date_of_birth" />
          <FormSelect label="Gender" v-model="profileForm.gender" :options="genderOptions" />
          <FormSelect label="Activity Level" v-model.number="profileForm.activity_level" :options="activityOptions" />
          <FormSelect label="Fitness Goal" v-model="profileForm.fitness_goal" :options="goalOptions" />
          <FormInput label="Target Weight (kg)" type="number" step="0.1" v-model.number="profileForm.target_weight" />
        </div>

        <h3 class="text-xl font-semibold mt-8 mb-4">Macro Targets</h3>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <FormInput label="Calories (kcal)" type="number" v-model.number="profileForm.target_calories" />
          <FormInput label="Protein (g)" type="number" v-model.number="profileForm.target_protein" />
          <FormInput label="Carbs (g)" type="number" v-model.number="profileForm.target_carbs" />
          <FormInput label="Fat (g)" type="number" v-model.number="profileForm.target_fat" />
        </div>

        <div class="mt-6">
          <button type="submit" :disabled="isUpdatingProfile"
            class="px-5 py-2 bg-orange-500 text-white font-medium rounded hover:bg-orange-600 disabled:bg-gray-500 transition-colors">
            {{ isUpdatingProfile ? 'Saving...' : 'Save Fitness Profile' }}
          </button>
          <p v-if="profileUpdateSuccess" class="text-green-400 mt-2">Profile updated successfully!</p>
          <p v-if="profileUpdateError" class="text-red-400 mt-2">{{ profileUpdateError }}</p>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watchEffect } from 'vue';
import { useAuthStore } from '@/stores/auth';
import FormInput from '@/components/FormInput.vue';
import FormSelect from '@/components/FormSelect.vue';
import StatDisplay from '@/components/StatDisplay.vue';



// --- Main Component Logic ---
const auth = useAuthStore();

// Computed properties to safely access nested user/profile data
const user = computed(() => auth.user?.user);
const profile = computed(() => auth.user?.user?.profile);

// Form state for CustomUser
const userForm = ref({
  first_name: '',
  last_name: '',
  phone_number: '',
  address: ''
});

// Form state for UserProfile
const profileForm = ref({
  height: 170,
  weight: 70,
  date_of_birth: null,
  gender: 'M',
  activity_level: 2,
  target_weight: 70,
  fitness_goal: 'maintain',
  target_calories: 2000,
  target_protein: 150,
  target_carbs: 250,
  target_fat: 65
});

// Form submission states
const isUpdatingUser = ref(false);
const userUpdateSuccess = ref(false);
const userUpdateError = ref(null);
const isUpdatingProfile = ref(false);
const profileUpdateSuccess = ref(false);
const profileUpdateError = ref(null);

// Populate forms when auth.user data is available
watchEffect(() => {
  if (user.value) {
    userForm.value.first_name = user.value.first_name || '';
    userForm.value.last_name = user.value.last_name || '';
    userForm.value.phone_number = user.value.phone_number || '';
    userForm.value.address = user.value.address || '';
  }
  if (profile.value) {
    // Copy all relevant fields from the store's profile to the local form
    Object.assign(profileForm.value, {
      height: profile.value.height,
      weight: profile.value.weight,
      date_of_birth: profile.value.date_of_birth,
      gender: profile.value.gender,
      activity_level: profile.value.activity_level,
      target_weight: profile.value.target_weight,
      fitness_goal: profile.value.fitness_goal,
      target_calories: profile.value.target_calories,
      target_protein: profile.value.target_protein,
      target_carbs: profile.value.target_carbs,
      target_fat: profile.value.target_fat,
    });
  }
});

// --- Select Options (from your Django models) ---
const genderOptions = [
  { value: 'M', text: 'Male' },
  { value: 'F', text: 'Female' },
];

const activityOptions = [
  { value: 0, text: 'No activity' },
  { value: 1, text: 'Little activity (1-2 light workouts)' },
  { value: 2, text: 'Medium activity (3-4 medium workouts)' },
  { value: 3, text: 'High activity (4-5 heavy workouts)' },
  { value: 4, text: 'Extreme activity (5+ intense workouts)' },
];

const goalOptions = [
  { value: 'lose', text: 'Lose weight' },
  { value: 'maintain', text: 'Maintain weight' },
  { value: 'gain', text: 'Gain weight' },
];

// --- Form Handlers ---
async function handleUserUpdate() {
  isUpdatingUser.value = true;
  userUpdateSuccess.value = false;
  userUpdateError.value = null;

  const result = await auth.updateUser(userForm.value);

  if (result.success) {
    userUpdateSuccess.value = true;
    setTimeout(() => userUpdateSuccess.value = false, 3000);
  } else {
    userUpdateError.value = result.error?.detail || 'Failed to update account.';
  }
  isUpdatingUser.value = false;
}

async function handleProfileUpdate() {
  isUpdatingProfile.value = true;
  profileUpdateSuccess.value = false;
  profileUpdateError.value = null;

  // Convert types before sending, as form inputs can be strings
  const payload = {
    ...profileForm.value,
    height: Number(profileForm.value.height),
    weight: Number(profileForm.value.weight),
    target_weight: Number(profileForm.value.target_weight),
    activity_level: Number(profileForm.value.activity_level),
    target_calories: Number(profileForm.value.target_calories),
    target_protein: Number(profileForm.value.target_protein),
    target_carbs: Number(profileForm.value.target_carbs),
    target_fat: Number(profileForm.value.target_fat),
  };

  const result = await auth.updateProfile(payload);

  if (result.success) {
    profileUpdateSuccess.value = true;
    setTimeout(() => profileUpdateSuccess.value = false, 3000);
  } else {
    // Handle validation errors (e.g., "Target weight should be less...")
    if (typeof result.error === 'object' && result.error !== null) {
      profileUpdateError.value = Object.values(result.error).join(' ');
    } else {
      profileUpdateError.value = result.error?.detail || 'Failed to update profile.';
    }
  }
  isUpdatingProfile.value = false;
}
</script>

<style scoped>
/* You can add component-specific styles here */
</style>