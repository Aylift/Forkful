import {createRouter, createWebHistory} from 'vue-router';
import FoodPage from '@/pages/FoodPage.vue';
import HomePage from '@/pages/HomePage.vue';

const routes = [
    {path: '/', component: HomePage},
    {path: '/food', component: FoodPage},
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;