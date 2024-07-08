import { createRouter, createWebHistory } from 'vue-router'
import Authentication from "../components/ProjectAuthentication.vue"
import Courses from "../components/CourseChoosing.vue"
import SelectedCourse from '../components/SelectedCourse.vue'
import CourseInfo from '../components/CourseInfo.vue'

const routes = [
    {
      path: '/',
      name: 'Authentication',
      component: Authentication
    },
    {
      path: '/courses',
      name: 'Courses',
      component: Courses
    },
    {
      path: '/course',
      name: 'Course',
      component: SelectedCourse
    },
    {
      path: '/course-info',
      name: 'CourseInfo',
      component: CourseInfo
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router