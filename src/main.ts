import { createApp } from 'vue';
import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';
import App from './App.vue';
import LoginForm from './components/auth/LoginForm.vue';
import RegisterForm from './components/auth/RegisterForm.vue';
import Board from './components/Boards/Board.vue';
import AdminBoard from './components/Boards/AdminBoard.vue';

import { FLASK_API_BASE_URL, VUE_API_BASE_URL } from '../config';

const routes: Array<RouteRecordRaw> = [
    { path: '/', redirect: '/login' },
    { path: '/login', component: LoginForm },
    { path: '/register', component: RegisterForm },
    {
        path: '/board', component: Board,
        beforeEnter: (to, from, next) => {

            const IsAuthtenticated = localStorage.getItem('token');

            if (IsAuthtenticated) {
                next();
            } else {
                next('/login');
            }
        },
    },
    {
        path: '/admin_board',
        component: AdminBoard,
        beforeEnter: (to, from, next) => {
            // Asegurarse de que el usuario esté autenticado y sea administrador
            const isAuthenticated = localStorage.getItem('token');
            const userRole = localStorage.getItem("userRole");
            if (isAuthenticated && userRole === "admin") {
                next();
            } else {
                next('/login');
            }
        },
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

const app = createApp(App).provide('FLASK_API_BASE_URL', FLASK_API_BASE_URL).provide('VUE_API_BASE_URL', VUE_API_BASE_URL);
app.use(router);
app.mount('#app');
