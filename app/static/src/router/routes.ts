import { createRouter, createWebHistory } from 'vue-router'
import Authentication from "../components/ProjectAuthentication.vue"
import Courses from "../components/CourseChoosing.vue"
import SelectedCourse from '../components/SelectedCourse.vue'
import CourseInfo from '../components/CourseInfo.vue'
import AllQuestions from '../components/AllQuestions.vue'
import TicketSelection from '../components/TicketSelection.vue'

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
    },
    {
      path: '/all-questions',
      name: 'AllQuestions',
      component: AllQuestions
    },
    {
      path: '/ticket-selection',
      name: 'TicketSelection',
      component: TicketSelection
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router