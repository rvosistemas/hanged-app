import { createApp } from 'vue';
import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';
import App from './App.vue';
import LoginForm from './components/LoginForm.vue';
import RegisterForm from './components/RegisterForm.vue';
import Board from './components/Board.vue';

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
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

const app = createApp(App).provide('FLASK_API_BASE_URL', FLASK_API_BASE_URL).provide('VUE_API_BASE_URL', VUE_API_BASE_URL);
app.use(router);
app.mount('#app');
