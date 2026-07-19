import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/DataView.vue'),
    },
    {
      path: '/create-animal',
      name: 'create-animal',
      component: () => import('../views/CreateAnimalView.vue'),
    },
    {
      path: '/animals/:animalId/edit',
      name: 'update-animal',
      component: () => import('../components/UpdateAnimal.vue'),
    },
    {
      path: '/data',
      name: 'data',
      component: () => import('../views/DataView.vue'),
    }
  ],
})

export default router
