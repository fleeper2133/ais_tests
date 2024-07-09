import { ref, computed } from "vue";
import { api } from "../api/base";
import { defineStore } from "pinia";
import router from "../src/router/routes"


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


export const useTasksStore = defineStore("tasks", () => {

function sendMail(data: SendMail){
    api.sendMail(data)
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


  return {
    logout,
    sendMail,
    login,
    registration,
  }
});
