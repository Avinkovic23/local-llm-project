import { createRouter, createWebHistory } from 'vue-router';
import ChatWindow from './components/ChatWindow.vue';
import LoginForm from './components/LoginForm.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: ChatWindow,
    meta: { requiresAuth: true },
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginForm,
    meta: { requiresAuth: false },
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/',
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
    const userLoggedIn = localStorage.getItem('access_token');

    if(to.name === 'Login' && userLoggedIn) {
        next({ name: 'Home' });
    }
    else if(to.meta.requiresAuth && !userLoggedIn) {
        next({ name: 'Login' });
    }
    else {
        next();
    }
});

export default router;