import { createRouter, createWebHistory } from 'vue-router'
import StudentView from '../views/StudentView.vue'
import TeacherView from '../views/TeacherView.vue'

const routes = [
  {
    path: '/',
    name: 'student',
    component: StudentView
  },
  {
    path: '/teacher',
    name: 'teacher',
    component: TeacherView
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
