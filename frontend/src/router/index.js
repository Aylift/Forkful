import {createRouter, createWebHistory} from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import FoodPage from '@/pages/FoodPage.vue';
import HomePage from '@/pages/HomePage.vue';
import ProfilePage from "@/pages/ProfilePage.vue";
import LoginRegisterPage from '@/pages/LoginRegisterPage.vue';

const routes = [
    {path: '/', component: HomePage},
    {path: '/food', component: FoodPage},
    {path: '/profile', component: ProfilePage},
    {path: '/loginregister', component: LoginRegisterPage},
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach((to, from, next) => {
    const auth = useAuthStore();
    const publicPages = ['/', '/loginregister'];
    const authRequired = !publicPages.includes(to.path);

    if (authRequired && !auth.token) {
        return next('/loginregister');
    }

    next();
});

export default router;