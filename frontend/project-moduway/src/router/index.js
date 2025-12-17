import { createRouter, createWebHistory } from 'vue-router'
import IndexPage from '@/pages/IndexPage.vue'
import CourseListPage from '@/pages/CourseListPage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: IndexPage,
    },
    {
      path: '/courses',
      name: 'courses',
      component: CourseListPage,
    },
    // 다른 라우트들은 작업하면서 추가
  ],
})

export default router