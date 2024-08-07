import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import signupView from '../views/signupView.vue'
import loginView from '../views/loginView.vue'
import ClientView from '../views/ClientView.vue'
import OpenView from '../views/OpenView.vue'
import LawyerView from '../views/LawyerView.vue'
import SearchView from '../views/SearchView.vue'
import ProfileView from '../views/ProfileView.vue'
import VideoView from '../views/VideoView.vue'


import NotificationsView from '../views/NotificationsView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/signup',
      name: 'signup',
      component: signupView
    },
    {
      path: '/login',
      name: 'login',
      component: loginView
    },
    {
        path: '/open',
        name: 'open',
        component: OpenView
    },
    {
        path: '/vdo',
        name: 'vdo',
        component: VideoView
    },
    {
        path: '/lawyer',
        name: 'lawyer',
        component: LawyerView
    },
    {
      path: '/feed',
      name: 'feed',
      component: feedView
    },
    {
      path: '/messages',
      name: 'messages',
      component: MessagesView
    },
    {
      path: '/search',
      name: 'search',
      component: SearchView
    },
    {
      path: '/notifications',
      name: 'notifications',
      component: NotificationsView
    },
    {
      path: '/profile/:id',
      name: 'profile',
      component: ProfileView
    },
    // {
    //   path: '/profile/:id/friends',
    //   name: 'friends',
    //   component: FriendsView
    // },
    // {
    //   path: '/:id',
    //   name: 'postview',
    //   component: postView
    // },

    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    }
  ]
})

export default router