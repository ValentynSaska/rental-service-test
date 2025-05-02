import { createRouter, createWebHistory } from 'vue-router'
import ApartmentList from '../pages/ApartmentList.vue'
import ApartmentDetail from '../pages/ApartmentDetail.vue'
import Profile from '@/pages/Profile.vue'
import Login from '@/pages/Login.vue'
import Register from '@/pages/Register.vue'
import AdminPanel from '@/pages/AdminPanel.vue'
import ViewBookings from '@/pages/ViewBookings.vue'
import ApartmentEdit from '@/pages/ApartmentEdit.vue'

const routes = [
  {
    path: '/',
    name: 'ApartmentList',
    component: ApartmentList
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: { requiresAuth: true }
  },
  {
    path: '/apartment/:slug',
    name: 'ApartmentDetail',
    component: ApartmentDetail,
    props: true,
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
  },
  {
    path: '/adminPanel',
    name: 'adminPanel',
    component: AdminPanel,
    meta: { requiresAuth: true, isAdmin: true }
  },
  {
    path: '/bookings',
    name: 'ViewBookings',
    component: ViewBookings,
    meta: { requiresAuth: true }
  }
  ,
  {
    path: '/editApartment/:slug',
    name: 'ApartmentEdit',
    component: ApartmentEdit,
    meta: { requiresAuth: true , isAdmin: true }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});


router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('access_token');
  const isAdmin = localStorage.getItem('user_role') === 'admin';

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login');
  }

  else if (to.meta.isAdmin && !isAdmin) {
    next('/');
  } else {
    next();
  }
});

export default router;
