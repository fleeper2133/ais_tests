import { ref, computed } from "vue"
import { api } from "../api/base"
import { defineStore } from "pinia"
import router from "./router/routes"

export interface Proposal {
  id: number
  fio: string
  email: string
  phone: string
  course: Course
  created_at?: string
  updated_at?: string
  is_checked: boolean
}

export interface Login {
  email: string
  password: string
}

export interface SendMail {
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
  testing?: []
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
  id?: number
  start_date?: string
  progress?: number
  status?: string
  selected?: boolean
  review_text?: string
  mark?: number
  user?: number
  course?: number
}

export interface GenerateCheck {
  question_count?: number
  status?: string
  difficulty?: string
  user_id?: number
  user_course_id: number
  type?: string
  created_at?: string
}

export interface GenerateCheckResponse {
  id: number
  user_check_skills: number
  question: number
  number_in_check: number
  user_answer: null
  answer_items?: []
  correct_answer_items?: []
  isRated?: boolean
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

export interface Schedule {
  id: number;
  user: number;
  user_course: number;
  monday: boolean;
  tuesday: boolean;
  wednesday: boolean;
  thursday: boolean;
  friday: boolean;
  saturday: boolean;
  sunday: boolean;
  week_start: string;
}



export const useStore = defineStore("tasks", () => {

  // Variables
  const allProposals = ref<Proposal[]>([])
  const currentUser = ref({})
  const allCourses = ref<Course[]>([])
  const selectedCourseId = ref<number | undefined>(undefined)
  const selectedCourse = ref<Course[]>([])
  const showCourseInfoButton = ref<boolean>(false)
  const courseQuestions = ref<Question[]>([])
  const favoritesQuestions = ref<Question[]>([])
  const filteredFavouriteQuestions = ref<Question[]>([])
  const startedCourses = ref<UserCourse[]>([])
  const questionData = ref<GenerateCheckResponse[]>([])
  const selectedTestIndex = ref<number>(0)
  const selectedTestId = ref<number>(0)
  const testingInfo = ref({})
  const testingDetail = ref({})
  const whatTicketSelectedId = ref<number>(0)
  const allQuestionsData = ref<GenerateCheckResponse[]>([])
  const allMistakes = ref<GenerateCheckResponse[]>([])
  const questionDetailList = ref<QuestionDetail[]>([])
  const userCheckSkills = ref<number | undefined>(undefined)
  const trainingAnswer = ref({})
  const lastCheckSkills = ref({})
  const lastCourse = ref({})
  const isLoading = ref<boolean>(true)
  const courseHistory = ref<GenerateCheck[]>([])
  const weekActivityData = ref<Schedule>({} as Schedule)
  const isQuestionComplanePopupVisible = ref(false)
  const questionDataForComplane = ref<QuestionDetail>({} as QuestionDetail)
  const courseStatuses = ref([
    { id: 'All', name: 'Все курсы' },
    { id: 'New', name: 'Начатые' },
  ])

  // Variables end

  function getProposals() {
    return api.getProposals()
      .then((proposals: Proposal[]) => {
        allProposals.value = proposals;
      })
  }

  function setProposal(proposalData: Proposal) {
    return api.setProposal(proposalData)
  }


  function getCurrentUser() {
    return api.getCurrentUser()
      .then((user: Course[]) => {
        currentUser.value = user
      })
  }

  function getCourses() {
    return api.getCourses()
      .then((courses: Course[]) => {
        allCourses.value = courses;
      })
  }

  function getLastUserCheckSkills() {
    return api.getUserCheckSkills()
      .then((userCheckSkills) => {
        lastCheckSkills.value = userCheckSkills[userCheckSkills.length - 1]
      })
  }

  function getCourseQuestions(id) {
    return api.getCourseQuestions(id)
      .then((questions: Question[]) => {
        courseQuestions.value = questions
      }).finally(() => {
        isLoading.value = false
      })
  }

  function getCourseById(id) {
    return api.getCourseById(id)
  }

  function getUserCourses() {
    return api.getUserCourses()
      .then((courses: UserCourse[]) => {
        const course = courses.filter(c => c.user === currentUser.value['id'])
        return startedCourses.value = course
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

  function generateFavouriteCheck(data: GenerateCheck) {
    return api.generateFavouriteCheck(data)
      .then((answer: GenerateCheckResponse[]) => {
        userCheckSkills.value = answer[0].user_check_skills
        return questionData.value = answer
      })
  }
  function generateBadCheck(data: GenerateCheck) {
    return api.generateBadCheck(data)
      .then((answer: GenerateCheckResponse[]) => {
        userCheckSkills.value = answer[0].user_check_skills
        return questionData.value = answer
      })
  }
  function generateRandomTicket(data) {
    return api.generateRandomTicket(data)
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

  function getCourseHistory(id: number) {
    return api.getCourseHistory(id)
      .then((answer: GenerateCheck) => {
        if (courseHistory) courseHistory.value = []
        courseHistory.value = answer.reverse()
      })
  }
  function getUserCkeckSkillsQuestions() {
    return api.getUserCkeckSkillsQuestions()
      .then((answer: GenerateCheckResponse[]) => {
        return allQuestionsData.value = answer
      })
  }

  function getMistakes(body) {
    return api.getMistakes(body)
      .then((answer: GenerateCheckResponse[]) => {
        return allMistakes.value = answer.reverse()
      })
      .finally(() => {
        isLoading.value = false
      })
  }

  function getTestingInfo(id) {
    return api.getTestingInfo(id)
      .then((answer) => {
        return testingInfo.value = answer
      })
  }
  function getTestingDetail(id) {
    return api.getTestingDetail(id, null)
  }
  function createTicketAnswer(id, body) {
    return api.createTicketAnswer(id, body)
  }
  function makeEndTicket(id, body) {
    return api.endTicket(id, body)
  }

  function getFavoritesQuestions() {
    return api.favoritesQuestions()
      .then((questions: Question[]) =>
        favoritesQuestions.value = questions
      )
  }

  function getLastCourse() {
    return api.getLastCourse()
    .then((course) => {
      if (course) lastCourse.value = course
      else console.log('Курс не найден')
    });
  }

  function markQuestionSelected(id: number) {
    return api.markQuestionSelected(id);
  }

  function giveRating(id: number, body: string) {
    return api.giveRating(id, body)
  }

  function getWeekActivity() {
    return api.getWeekActivity()
      .then((answer) => {
        return weekActivityData.value = answer
      })
  }

  function issueСomplain(body) {
    return api.issueСomplain(body)
  }

  // Favorite end


  // Authentication
  function login(loginData: Login) {
    api.login(loginData)
      .then(response => {
        if (response) {

          localStorage.setItem('accessToken', response.access);
          localStorage.setItem('refreshToken', response.refresh);
          localStorage.removeItem('demo');
          router.push({ path: "/courses" })
        } else {
          console.error('Ошибка:', response.statusText);

        }
      })
      .catch(error => {
        console.error('Ошибка отправки данных:', error);

      });
  }

  async function demo() {
    await api.demo()
      .then(response => {
        if (response) {
          console.log("demo create");
          localStorage.setItem('accessToken', response.access);
          localStorage.setItem('refreshToken', response.refresh);
          localStorage.setItem('accessTokenDemo', response.access);
          localStorage.setItem('refreshTokenDemo', response.refresh);
          localStorage.setItem('demo', 'true');
          router.push({ path: "/courses" })
        } else {
          console.error('Ошибка:', response.statusText);

        }
      })
      .catch(error => {
        console.error('Ошибка отправки данных:', error);

      });

  }

  function logout() {


    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('email'); // email


  }

  function registration(registrationData: Registration) {
    api.registration(registrationData)
      .catch(error => {
        console.log(error);
      });
  }
  // Authentication end

  function sendMail(data: SendMail) {
    api.sendMail(data)
  }


  return {
    getProposals,
    allProposals,
    setProposal,
    allCourses,
    selectedCourseId,
    selectedCourse,
    getCourses,
    getCourseQuestions,
    courseQuestions,
    logout,
    sendMail,
    login,
    demo,
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
    filteredFavouriteQuestions,
    userCheckSkills,
    courseStatuses,
    getCurrentUser,
    currentUser,
    giveRating,
    lastCheckSkills,
    getLastUserCheckSkills,
    lastCourse,
    getLastCourse,
    isLoading,
    getCourseById,
    courseHistory,
    getCourseHistory,
    getUserCkeckSkillsQuestions,
    allQuestionsData,
    getMistakes,
    allMistakes,
    testingInfo,
    getTestingInfo,
    testingDetail,
    getTestingDetail,
    selectedTestIndex,
    selectedTestId,
    whatTicketSelectedId,
    createTicketAnswer,
    makeEndTicket,
    generateFavouriteCheck,
    generateBadCheck,
    generateRandomTicket,
    getWeekActivity,
    weekActivityData,
    issueСomplain,
    isQuestionComplanePopupVisible,
    questionDataForComplane
  }
});
