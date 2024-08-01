import { createRouter, createWebHistory } from 'vue-router'
import Authentication from "../components/ProjectAuthentication.vue"
import Courses from "../components/CourseChoosing.vue"
import SelectedCourse from '../components/SelectedCourse.vue'
import CourseInfo from '../components/CourseInfo.vue'
import AllQuestions from '../components/AllQuestions.vue'
import TicketSelection from '../components/TicketSelection.vue'
import Testing from '../components/Testing.vue'
import History from '../components/History.vue'
import Mistakes from '../components/Mistakes.vue'
import FavoriteQuestions from '../components/FavoriteQuestions.vue'

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
    },
    {
      path: '/testing',
      name: 'Testing',
      component: Testing
    },
    {
      path: '/history',
      name: 'History',
      component: History
    },
    {
      path: '/mistakes',
      name: 'Mistakes',
      component: Mistakes
    },
    {
      path: '/favorite-questions',
      name: 'FavoriteQuestions',
      component: FavoriteQuestions
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router