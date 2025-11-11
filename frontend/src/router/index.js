import {createRouter, createWebHistory} from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import MealsDashboard from '@/pages/MealsDashboard.vue';
import ProfilePage from "@/pages/ProfilePage.vue";
import LoginRegisterPage from '@/pages/LoginRegisterPage.vue';
import MealsPage from '@/pages/MealsPage.vue';
import LandingPage from '@/pages/LandingPage.vue';

const routes = [
    {path: '/', component: LandingPage },
    {path: '/dashboard', component: MealsDashboard},
    {path: '/meals', component: MealsPage},
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