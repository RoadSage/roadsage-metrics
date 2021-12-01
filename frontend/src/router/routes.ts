import { RouteRecordRaw } from 'vue-router';

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
