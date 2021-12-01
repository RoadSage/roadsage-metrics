import { RouteRecordRaw } from 'vue-router';
import type { RouteLocationNormalized, RouteLocationRaw } from 'vue-router';
import { Cookies } from 'quasar';

const requireAuth = (to: RouteLocationNormalized): RouteLocationRaw | true => {
  if (!Cookies.get('user'))
    return {
      path: '/signin',
      query: { redirect: to.fullPath },
    };

  return true;
};

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/Landing.vue') },
      { path: '/signin', component: () => import('pages/SignIn.vue') },
      { path: '/signup', component: () => import('pages/SignUp.vue') },
      {
        path: '/dashboard',
        component: () => import('pages/Dashboard.vue'),
        beforeEnter: requireAuth,
      },
    ],
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/Error404.vue'),
  },
];

export default routes;
