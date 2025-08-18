import {createRouter, createWebHistory} from 'vue-router';
import FoodPage from '@/pages/FoodPage.vue';
import HomePage from '@/pages/HomePage.vue';
import ProfilePage from "@/pages/ProfilePage.vue";

const routes = [
    {path: '/', component: HomePage},
    {path: '/food', component: FoodPage},
    {path: '/profile', component: ProfilePage}
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;