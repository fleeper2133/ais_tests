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


export const useStore = defineStore("tasks", () => {

// Variables

const allCourses = ref<Course[]>([])
const selectedCourse = ref<number | undefined>(undefined)

// Variables end


function getCourses() {
  return api.getCourses()
  .then((courses: Course[]) => {
    allCourses.value = courses;
  })
}


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
    selectedCourse,
    getCourses,
    logout,
    sendMail,
    login,
    registration,
  }
});
