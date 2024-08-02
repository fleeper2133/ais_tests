import { ref, computed } from "vue";
import { api } from "../api/base";
import { defineStore } from "pinia";
import router from "./router/routes"


export interface Login {
  email: string
  password: string
}

export interface SendMail{
  email?: string,
  title: string,
  description: string
}

export interface Registration {
  email: string
  password: string
  password_confirm: string
}

export interface User {
  id: number
  email: string
  password: string
  last_login: string
  is_superuser: boolean
  first_name: string
  last_name: string
  is_staff: boolean
  is_active: boolean
  date_joined: string
  groups: number[]
  user_permissions: number[]
}

export interface Course {
  id: number
  name: string
  description: string
  version: string
  available_until: string
  question_count: number
  image_link: string
  user_marks: number
  qualification: number
}

export interface Question {
  id?: number
  name?: string
  question_text?: string
  topic?: string
  difficulty?: string
  explanations?: string
  right_answer_count?: number
  answer_count?: number
  course?: number
  explanation_material?: number
  ndocumen?: number
  block?: number
}

export interface UserCourse {
  id: number
  start_date: string
  progress: number
  status: string
  selected: boolean
  review_text: string
  mark: number
  user: number
  course: number
}

export interface GenerateCheck {
  question_count: number
  status?: string
  difficulty: string
  user_id?: number
  user_course_id: number
}

export interface GenerateCheckResponse {
  id: number
  user_check_skills: number
  question: number
  number_in_check: number
  user_answer: null
  answer_items?: []
  correct_answer_items?: []
  status: string
}

export interface QuestionDetail {
  id: number
  name: string
  question_text: string
  explanations: null
  normative_documents: {}
  varients?: []
  selected: boolean
}



export const useStore = defineStore("tasks", () => {

// Variables

const allCourses = ref<Course[]>([])
const selectedCourseId = ref<number | undefined>(undefined)
const selectedCourse = ref<Course[]>([])
const showCourseInfoButton = ref<boolean>(false)
const courseQuestions = ref<Question[]>([])
const favoritesQuestions = ref<Question[]>([])
const startedCourses = ref<UserCourse[]>([])
const questionData = ref<GenerateCheckResponse[]>([])
const questionWorkStats = ref({}) // удалить, не используется
const questionDetailList = ref<QuestionDetail[]>([])
const userCheckSkills = ref<number | undefined>(undefined)
const trainingAnswer = ref({})
const courseStatuses = ref([
  {id: 'All', name: 'Все курсы'},
  {id: 'New', name: 'Начатые'},
])

// Variables end


function getCourses() {
  return api.getCourses()
  .then((courses: Course[]) => {
    allCourses.value = courses;
  })
}

function getCourseQuestions(id) {
  return api.getCourseQuestions(id)
  .then((questions: Question[]) => {
    courseQuestions.value = questions
  })
}

function getUserCourses() {
  return api.getUserCourses()
  .then((courses: UserCourse[]) => {
    return startedCourses.value = courses
  })
}
function setUserCourse(courseData: UserCourse) {
  return api.setUserCourse(courseData)
}
function startCourse(id: number, courseData: UserCourse) {
  return api.startCourse(id, courseData)
}
function smartGenerate(data: GenerateCheck) {
  return api.smartGenerate(data)
  .then((answer: GenerateCheckResponse[]) => {
    userCheckSkills.value = answer[0].user_check_skills
    return questionData.value = answer
  })
}

function getQuestionDetail(id: number) {
  return api.getQuestionDetail(id);
}

function createAnswer(id: number, data: GenerateCheckResponse) {
  return api.createAnswer(id, data)
  .then((answer: GenerateCheckResponse) => {
    trainingAnswer.value = answer
  })
}
function endTraining(id: number) {
  return api.endTraining(id)
}

// Favorite

function getFavoritesQuestions(){
  return api.favoritesQuestions()
  .then((questions: Question[]) => 
    favoritesQuestions.value = questions
  );
}

function markQuestionSelected(id: number){
  return api.markQuestionSelected(id);
}

// Favorite end

// Authentication
function login(loginData: Login) {
  api.login(loginData)
  .then(response => {
    if (response) {
        
        localStorage.setItem('accessToken', response.access);
        localStorage.setItem('refreshToken', response.refresh);
        router.push({path: "/courses"})
    } else {
        console.error('Ошибка:', response.statusText);
        
    }
  })
  .catch(error => {
    console.error('Ошибка отправки данных:', error);
    
  });
}

function logout(token) {
  api.logout(token)
  .then(response => {
    if (response) {
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      localStorage.removeItem('email'); // email
      
      document.location.href = '/login/', true;
    } else {
      console.error('Ошибка:', response.statusText);
  }})
  .catch(error => {
    console.error('Ошибка отправки данных:', error);
  });
}

function registration(registrationData: Registration) {
  api.registration(registrationData)
    .catch(error => {
      console.log(error);
    });
}
// Authentication end

function sendMail(data: SendMail){
  api.sendMail(data)
}


  return {
    allCourses,
    selectedCourseId,
    selectedCourse,
    getCourses,
    getCourseQuestions,
    courseQuestions,
    logout,
    sendMail,
    login,
    registration,
    getUserCourses,
    startedCourses,
    setUserCourse,
    showCourseInfoButton,
    startCourse,
    smartGenerate,
    questionData,
    getQuestionDetail,
    questionDetailList,
    createAnswer,
    trainingAnswer,
    endTraining,
    markQuestionSelected,
    getFavoritesQuestions,
    favoritesQuestions,
    userCheckSkills,
    courseStatuses,
    questionWorkStats
  }
});
