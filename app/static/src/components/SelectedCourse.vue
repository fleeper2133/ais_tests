<template>
    <div class="content" @click="closeAllDroppers">
        <div>
            <Header />
            <div class="container container__bg">
                <div class="manage link-line">
                    <button class="button-back" @click="goBack">
                        <svg class="button-back__arrow" width="30px" height="30px" viewBox="0 0 24 24" fill="none">
                            <path d="M14.2893 5.70708C13.8988 5.31655 13.2657 5.31655 12.8751 5.70708L7.98768 10.5993C7.20729 11.3805 7.2076 12.6463 7.98837 13.427L12.8787 18.3174C13.2693 18.7079 13.9024 18.7079 14.293 18.3174C14.6835 17.9269 14.6835 17.2937 14.293 16.9032L10.1073 12.7175C9.71678 12.327 9.71678 11.6939 10.1073 11.3033L14.2893 7.12129C14.6799 6.73077 14.6799 6.0976 14.2893 5.70708Z"/>
                        </svg>
                        <p class="fw-bold">Назад</p>
                    </button>
                </div>
            </div>
            <div class="container-name">
                <div class="container-name__title fs-20 fw-bold">{{aisStore.selectedCourse[0].name}}</div>
            </div>
            <div class="container container__flex">
                <div class="info">
                    <div class="progress-bar">
                        <p class="fw-bold">Ваш прогресс</p>
                        <div class="progress-bar__content">
                            <div class="statistic">
                                <!-- <div class="statistic__column">
                                    <p class="fs-14 grey-text">Времени потрачено</p>
                                    <div class="statistic__value fw-bold">{{ aisStore.startedCourses[aisStore.selectedCourseId - 1]['course_time'] }}</div>
                                </div>
                                <div class="statistic__column">
                                    <p class="fs-14 grey-text">Хорошо изучено</p>
                                    <div class="statistic__value fw-bold">{{ aisStore.startedCourses[aisStore.selectedCourseId - 1]['good_memorization_count'] }}</div>
                                </div>
                                <div class="statistic__column">
                                    <p class="fs-14 grey-text">Плохо изучено</p>
                                    <div class="statistic__value fw-bold">{{ aisStore.startedCourses[aisStore.selectedCourseId - 1]['bad_memorization_count'] }}</div>
                                </div> -->
                                <div class="statistic__column">
                                    <p class="fs-14 grey-text">Времени потрачено</p>
                                    <div class="statistic__value fw-bold">{{ showCourseStatInfo('course_time') }}</div>
                                </div>
                                <div class="statistic__column">
                                    <p class="fs-14 grey-text">Хорошо изучено</p>
                                    <div class="statistic__value fw-bold">{{ showCourseStatInfo('good_memorization_count') }}</div>
                                </div>
                                <div class="statistic__column">
                                    <p class="fs-14 grey-text">Плохо изучено</p>
                                    <div class="statistic__value fw-bold">{{ showCourseStatInfo('bad_memorization_count') }}</div>
                                </div>
                            </div>
                            <div class="circle-big">
                                <div class="circle-big__text">
                                    {{ progressPercentage }}%
                                    <div class="circle-big__text-progress">прогресс</div>
                                </div>
                                <svg>
                                    <circle class="bg" cx="57" cy="57" r="52"></circle>
                                    <circle :style="progressStyle" class="progress" cx="57" cy="57" r="52"></circle>
                                </svg>
                            </div>
                        </div>
                    </div>
                    <div class="info__buttons">
                        <button class="button info__button" @click="openFavorite">
                            <img class="info__button-img" src="../assets/images/star.png" alt="favorite">
                            <p>Избранные вопросы</p>
                        </button>
                        <button class="button info__button" @click="openMistakes">
                            <img class="info__button-img" src="../assets/images/error.svg" alt="errors">
                            <p>Частые ошибки</p>
                        </button>
                        <button class="button info__button" @click="openHistory">
                            <img class="info__button-img" src="../assets/images/calendar.svg" alt="history">
                            <p>История прохождения</p>
                        </button>
                        <button class="button info__button" @click="courseInfo">
                            <img class="info__button-img" src="../assets/images/info.svg" alt="info">
                            <p>Информация</p>
                        </button>
                    </div>
                </div>
                <div class="selectors">
                    <div class="selector">
                        <div class="selector__header">
                            <div class="selector__text">
                                <p class="selector__title fw-bold">Режим обучения</p>
                                <div class="selector__info">
                                    <div class="selector__data">
                                        <p class="fs-14 main-blue">Вопросы:</p>
                                        <p class="fs-14 main-blue fw-bold">{{ questionCount }} случайных</p>
                                    </div>
                                    <div class="selector__data">
                                        <p class="fs-14 main-blue">Сложность:</p>
                                        <p class="fs-14 main-blue fw-bold">{{ difficultyText1 }}</p>
                                    </div>
                                </div>
                                <p class="selector__subtitle grey-text">
                                    Здесь вы сможете подготовиться к тестированию и улучшить свои знания и навыки. Наш режим обучения предназначен для того, чтобы помочь вам закрепить материал и повысить уверенность в своих силах.
                                </p>
                            </div>
                            <div class="icon">
                                <svg class="selector__svg" width="44" height="38" viewBox="0 0 44 38" fill="none" >
                                    <path d="M40.5625 15.5498V6.91101C40.5625 5.00564 39.0204 3.4555 37.125 3.4555H6.875C4.97956 3.4555 3.4375 5.00564 3.4375 6.91101V24.1885C3.4375 26.0939 4.97956 27.644 6.875 27.644H37.125C39.0204 27.644 40.5625 26.0939 40.5625 24.1885C40.5625 23.2343 41.332 22.4608 42.2812 22.4608C43.2305 22.4608 44 23.2343 44 24.1885C44 27.9993 40.9159 31.0995 37.125 31.0995H23.7188V34.5445H29.7344C30.6836 34.5445 31.4531 35.318 31.4531 36.2722C31.4531 37.2265 30.6836 38 29.7344 38H14.2656C13.3164 38 12.5469 37.2265 12.5469 36.2722C12.5469 35.318 13.3164 34.5445 14.2656 34.5445H20.2812V31.0995H6.875C3.08413 31.0995 0 27.9993 0 24.1885V6.91101C0 3.10028 3.08413 0 6.875 0H37.125C40.9159 0 44 3.10028 44 6.91101V15.5498C44 16.504 43.2305 17.2775 42.2812 17.2775C41.332 17.2775 40.5625 16.504 40.5625 15.5498ZM33.5156 9.41625H23.2891C22.3398 9.41625 21.5703 10.1898 21.5703 11.144C21.5703 12.0982 22.3398 12.8718 23.2891 12.8718H33.5156C34.4649 12.8718 35.2344 12.0982 35.2344 11.144C35.2344 10.1898 34.4649 9.41625 33.5156 9.41625ZM19.4854 6.01093C18.7536 5.4032 17.6703 5.50686 17.0656 6.24245L13.3527 10.7599L11.8876 9.24753C11.2252 8.56377 10.1372 8.54926 9.45716 9.21505C8.77705 9.88075 8.76253 10.9746 9.42485 11.6583L11.2686 13.5616C11.2838 13.5774 11.2992 13.5927 11.315 13.6078C11.8722 14.1408 12.6158 14.4374 13.3808 14.4374C13.4466 14.4374 13.5125 14.4353 13.5785 14.4308C14.4072 14.3752 15.1812 13.9721 15.7043 13.3241L19.7157 8.44344C20.3203 7.70776 20.2171 6.61876 19.4854 6.01093ZM33.5156 20.0419H23.2891C22.3398 20.0419 21.5703 20.8154 21.5703 21.7697C21.5703 22.7239 22.3398 23.4974 23.2891 23.4974H33.5156C34.4649 23.4974 35.2344 22.7239 35.2344 21.7697C35.2344 20.8154 34.4649 20.0419 33.5156 20.0419ZM19.4854 16.6259C18.7536 16.0182 17.6703 16.1218 17.0656 16.8574L13.3518 21.3761L11.8843 19.8697C11.2201 19.1878 10.1319 19.1763 9.45373 19.8441C8.77551 20.5117 8.76416 21.6056 9.42829 22.2874L11.272 24.1801C11.2861 24.1945 11.3004 24.2087 11.315 24.2226C11.8721 24.7557 12.6157 25.0523 13.3808 25.0523C13.4466 25.0523 13.5126 25.0501 13.5785 25.0457C14.4072 24.9901 15.1812 24.5869 15.7043 23.939L19.7157 19.0583C20.3203 18.3227 20.2171 17.2337 19.4854 16.6259Z" fill="#7DB1FF"/>
                                </svg>
                            </div>
                        </div>
                        <div class="selector__action">
                            <div class="selector__buttons">
                                <div class="droppers">
                                    <div class="dropper">
                                        <div class="dropper__title" @click.stop="toggleDropper('questions')">
                                            Вопросы: {{ questionCount }}
                                            <span :class="['dropper__arrow', { 'dropper__arrow--up': dropperStates.questions }]"></span>
                                        </div>
                                        <div v-show="dropperStates.questions" class="dropper__list">
                                            <p class="dropper__item" @click.stop="selectQuestion(10)">10 вопросов</p>
                                            <p class="dropper__item" @click.stop="selectQuestion(20)">20 вопросов</p>
                                            <p class="dropper__item" @click.stop="selectQuestion(30)">30 вопросов</p>
                                            <p class="dropper__item" @click.stop="selectQuestion(40)">40 вопросов</p>
                                        </div>
                                    </div>
                                    <div class="dropper">
                                        <div class="dropper__title" @click.stop="toggleDropper('difficulty1')">
                                            Сложность: {{ difficultyText1 }}
                                            <span :class="['dropper__arrow', { 'dropper__arrow--up': dropperStates.difficulty1 }]"></span>
                                        </div>
                                        <div v-show="dropperStates.difficulty1" class="dropper__list">
                                            <p class="dropper__item" @click.stop="selectDifficulty('difficulty1', 'Легко'), testDifficultyLevel = 'Easy'">Легко</p>
                                            <p class="dropper__item" @click.stop="selectDifficulty('difficulty1', 'Средне'), testDifficultyLevel = 'Medium'">Средне</p>
                                            <p class="dropper__item" @click.stop="selectDifficulty('difficulty1', 'Сложно') , testDifficultyLevel= 'Hard'">Сложно</p>
                                        </div>
                                    </div>
                                </div>
                                <router-link to="/training">
                                    <button class="selector__button" @click="generateCheck">Начать</button>
                                </router-link>
                            </div>
                        </div>
                    </div>
                    <div class="selector">
                        <div class="selector__header">
                            <div class="selector__text">
                                <p class="selector__title fw-bold">Режим тестирования</p>
                                <div class="selector__info">
                                    <div class="selector__data">
                                        <p class="fs-14 main-blue">Билеты:</p>
                                        <p class="fs-14 main-blue fw-bold">{{ aisStore.selectedCourse[0].testing?.['tickets'].length}}</p>
                                    </div>
                                </div>
                                <p class="selector__subtitle grey-text">
                                    Здесь вы сможете проверить свои знания и навыки в условиях, максимально приближенных к реальному экзамену. Наш режим тестирования предназначен для того, чтобы помочь вам оценить свою готовность и выявить области, требующие дополнительного внимания.
                                </p>
                            </div>
                            <div class="icon">
                                <svg class="selector__svg" width="44" height="38" viewBox="0 0 44 38" fill="none" >
                                    <path d="M40.5625 15.5498V6.91101C40.5625 5.00564 39.0204 3.4555 37.125 3.4555H6.875C4.97956 3.4555 3.4375 5.00564 3.4375 6.91101V24.1885C3.4375 26.0939 4.97956 27.644 6.875 27.644H37.125C39.0204 27.644 40.5625 26.0939 40.5625 24.1885C40.5625 23.2343 41.332 22.4608 42.2812 22.4608C43.2305 22.4608 44 23.2343 44 24.1885C44 27.9993 40.9159 31.0995 37.125 31.0995H23.7188V34.5445H29.7344C30.6836 34.5445 31.4531 35.318 31.4531 36.2722C31.4531 37.2265 30.6836 38 29.7344 38H14.2656C13.3164 38 12.5469 37.2265 12.5469 36.2722C12.5469 35.318 13.3164 34.5445 14.2656 34.5445H20.2812V31.0995H6.875C3.08413 31.0995 0 27.9993 0 24.1885V6.91101C0 3.10028 3.08413 0 6.875 0H37.125C40.9159 0 44 3.10028 44 6.91101V15.5498C44 16.504 43.2305 17.2775 42.2812 17.2775C41.332 17.2775 40.5625 16.504 40.5625 15.5498ZM33.5156 9.41625H23.2891C22.3398 9.41625 21.5703 10.1898 21.5703 11.144C21.5703 12.0982 22.3398 12.8718 23.2891 12.8718H33.5156C34.4649 12.8718 35.2344 12.0982 35.2344 11.144C35.2344 10.1898 34.4649 9.41625 33.5156 9.41625ZM19.4854 6.01093C18.7536 5.4032 17.6703 5.50686 17.0656 6.24245L13.3527 10.7599L11.8876 9.24753C11.2252 8.56377 10.1372 8.54926 9.45716 9.21505C8.77705 9.88075 8.76253 10.9746 9.42485 11.6583L11.2686 13.5616C11.2838 13.5774 11.2992 13.5927 11.315 13.6078C11.8722 14.1408 12.6158 14.4374 13.3808 14.4374C13.4466 14.4374 13.5125 14.4353 13.5785 14.4308C14.4072 14.3752 15.1812 13.9721 15.7043 13.3241L19.7157 8.44344C20.3203 7.70776 20.2171 6.61876 19.4854 6.01093ZM33.5156 20.0419H23.2891C22.3398 20.0419 21.5703 20.8154 21.5703 21.7697C21.5703 22.7239 22.3398 23.4974 23.2891 23.4974H33.5156C34.4649 23.4974 35.2344 22.7239 35.2344 21.7697C35.2344 20.8154 34.4649 20.0419 33.5156 20.0419ZM19.4854 16.6259C18.7536 16.0182 17.6703 16.1218 17.0656 16.8574L13.3518 21.3761L11.8843 19.8697C11.2201 19.1878 10.1319 19.1763 9.45373 19.8441C8.77551 20.5117 8.76416 21.6056 9.42829 22.2874L11.272 24.1801C11.2861 24.1945 11.3004 24.2087 11.315 24.2226C11.8721 24.7557 12.6157 25.0523 13.3808 25.0523C13.4466 25.0523 13.5126 25.0501 13.5785 25.0457C14.4072 24.9901 15.1812 24.5869 15.7043 23.939L19.7157 19.0583C20.3203 18.3227 20.2171 17.2337 19.4854 16.6259Z" fill="#7DB1FF"/>
                                </svg>
                            </div>
                        </div>
                        <div class="selector__action">
                            <div class="selector__buttons">
                                <button class="selector__button" @click="goToTickets">Пройти</button>
                            </div>
                        </div>
                    </div>
                    <div class="selector">
                        <div class="selector__header">
                            <div class="selector__text">
                                <p class="selector__title fw-bold">Все вопросы курса</p>
                                <div class="selector__info">
                                    <div class="selector__data">
                                        <p class="fs-14 main-blue">Всего вопросов:</p>
                                        <p class="fs-14 main-blue fw-bold">{{ showQuestionCount() }}</p>
                                    </div>
                                </div>
                                <p class="selector__subtitle grey-text">
                                    Здесь вы найдете все вопросы, которые используются в режимах обучения и тестирования, вместе с правильными ответами и подробными пояснениями. Этот раздел предназначен для того, чтобы помочь вам глубже понять материал и закрепить свои знания.
                                </p>
                            </div>
                            <div class="icon">
                                <svg class="selector__svg" width="44" height="38" viewBox="0 0 44 38" fill="none" >
                                    <path d="M40.5625 15.5498V6.91101C40.5625 5.00564 39.0204 3.4555 37.125 3.4555H6.875C4.97956 3.4555 3.4375 5.00564 3.4375 6.91101V24.1885C3.4375 26.0939 4.97956 27.644 6.875 27.644H37.125C39.0204 27.644 40.5625 26.0939 40.5625 24.1885C40.5625 23.2343 41.332 22.4608 42.2812 22.4608C43.2305 22.4608 44 23.2343 44 24.1885C44 27.9993 40.9159 31.0995 37.125 31.0995H23.7188V34.5445H29.7344C30.6836 34.5445 31.4531 35.318 31.4531 36.2722C31.4531 37.2265 30.6836 38 29.7344 38H14.2656C13.3164 38 12.5469 37.2265 12.5469 36.2722C12.5469 35.318 13.3164 34.5445 14.2656 34.5445H20.2812V31.0995H6.875C3.08413 31.0995 0 27.9993 0 24.1885V6.91101C0 3.10028 3.08413 0 6.875 0H37.125C40.9159 0 44 3.10028 44 6.91101V15.5498C44 16.504 43.2305 17.2775 42.2812 17.2775C41.332 17.2775 40.5625 16.504 40.5625 15.5498ZM33.5156 9.41625H23.2891C22.3398 9.41625 21.5703 10.1898 21.5703 11.144C21.5703 12.0982 22.3398 12.8718 23.2891 12.8718H33.5156C34.4649 12.8718 35.2344 12.0982 35.2344 11.144C35.2344 10.1898 34.4649 9.41625 33.5156 9.41625ZM19.4854 6.01093C18.7536 5.4032 17.6703 5.50686 17.0656 6.24245L13.3527 10.7599L11.8876 9.24753C11.2252 8.56377 10.1372 8.54926 9.45716 9.21505C8.77705 9.88075 8.76253 10.9746 9.42485 11.6583L11.2686 13.5616C11.2838 13.5774 11.2992 13.5927 11.315 13.6078C11.8722 14.1408 12.6158 14.4374 13.3808 14.4374C13.4466 14.4374 13.5125 14.4353 13.5785 14.4308C14.4072 14.3752 15.1812 13.9721 15.7043 13.3241L19.7157 8.44344C20.3203 7.70776 20.2171 6.61876 19.4854 6.01093ZM33.5156 20.0419H23.2891C22.3398 20.0419 21.5703 20.8154 21.5703 21.7697C21.5703 22.7239 22.3398 23.4974 23.2891 23.4974H33.5156C34.4649 23.4974 35.2344 22.7239 35.2344 21.7697C35.2344 20.8154 34.4649 20.0419 33.5156 20.0419ZM19.4854 16.6259C18.7536 16.0182 17.6703 16.1218 17.0656 16.8574L13.3518 21.3761L11.8843 19.8697C11.2201 19.1878 10.1319 19.1763 9.45373 19.8441C8.77551 20.5117 8.76416 21.6056 9.42829 22.2874L11.272 24.1801C11.2861 24.1945 11.3004 24.2087 11.315 24.2226C11.8721 24.7557 12.6157 25.0523 13.3808 25.0523C13.4466 25.0523 13.5126 25.0501 13.5785 25.0457C14.4072 24.9901 15.1812 24.5869 15.7043 23.939L19.7157 19.0583C20.3203 18.3227 20.2171 17.2337 19.4854 16.6259Z" fill="#7DB1FF"/>
                                </svg>
                            </div>
                        </div>
                        <div class="selector__action">
                            <div class="selector__buttons">
                                <button class="selector__button" @click="openCourseQuestions">Смотреть</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <Footer />
    </div>
</template>

<script setup lang="ts">

import Header from './Header.vue'
import Footer from './Footer.vue'

import { computed, onMounted, ref, reactive, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { useStore, GenerateCheck } from "../store"

const router = useRouter()
const aisStore = useStore()

function showCourseStatInfo(name: string) {
    const course = aisStore.startedCourses.find(c => c.course === aisStore.selectedCourseId)
    return course![name]
}

async function goToTickets() {
    const id = aisStore.selectedCourse[0].testing?.['id']
    
    aisStore.testingInfo = []
    await aisStore.getTestingInfo(id)
    router.push('/ticket-selection')
}
function courseInfo(): void {
    aisStore.showCourseInfoButton = false
    router.push('/course-info')
}
function openHistory(): void {
    const whatCourseSelected = aisStore.startedCourses.find(c => c.course === aisStore.selectedCourse[0].id)
    if (whatCourseSelected) {
        aisStore.getCourseHistory(whatCourseSelected.id)
    }
    router.push('/history')
}

// Progress Circle

const progressPercentage = ref(0)

const progressStyle = computed(() => {
    const newStrokeDashoffset = 326.56 - (326.56 * (progressPercentage.value / 100))
    return {
    strokeDashoffset: newStrokeDashoffset,
    };
});

onMounted(() => {
    const course = aisStore.startedCourses.find(c => c.course === aisStore.selectedCourseId)
    const progressFromStore = course!['progress']
    progressPercentage.value = progressFromStore
});

// Progress Circle


// Dropper
const dropperStates = reactive({
    questions: false,
    difficulty1: false,
    difficulty2: false,
});

const questionCount = ref(10)
const difficultyText1 = ref('Легко')
const difficultyText2 = ref('Легко')

const toggleDropper = (dropper: keyof typeof dropperStates) => {
    closeAllDroppers()
    dropperStates[dropper] = true
};

const closeAllDroppers = () => {
    dropperStates.questions = false
    dropperStates.difficulty1 = false
    dropperStates.difficulty2 = false
};

const selectQuestion = (count: number) => {
    questionCount.value = count
    closeAllDroppers()
};

const selectDifficulty = (dropper: 'difficulty1' | 'difficulty2', difficulty: string) => {
    if (dropper === 'difficulty1') {
        difficultyText1.value = difficulty
    } else if (dropper === 'difficulty2') {
        difficultyText2.value = difficulty
    }

    closeAllDroppers()
}
// Dropper end

function goBack(): void {
    router.push('/courses')
}

function openFavorite(): void {
    const course = aisStore.startedCourses.find(c => c.course === aisStore.selectedCourse[0].id)
    aisStore.getCourseQuestions(course?.id)
    router.push('/favorite-questions')
}

function openMistakes(): void {
    const course = aisStore.startedCourses.find(c => c.course === aisStore.selectedCourse[0].id)
    aisStore.getCourseQuestions(course?.id)

    const startedCourse = aisStore.startedCourses.find(c => c.course === aisStore.selectedCourse[0].id)
    if (!startedCourse) throw new Error('Course not found!')
    const check = {
        "user_course_id": startedCourse.id
    }
    aisStore.getMistakes(check)
    router.push('/mistakes')
}


function openCourseQuestions(): void {
    const course = aisStore.startedCourses.find(c => c.course === aisStore.selectedCourse[0].id)
    aisStore.getCourseQuestions(course?.id)
    router.push('/all-questions')
}

function showQuestionCount() {
    return aisStore.selectedCourse[0].question_count
}

// Генерация вопросов

const testDifficultyLevel = ref('Easy')

async function generateCheck() {
    const startedCourse = aisStore.startedCourses.find(c => c.course === aisStore.selectedCourse[0].id)
    if (!startedCourse) throw new Error('Course not found!')
    const check: GenerateCheck = {
        "question_count": questionCount.value,
        "difficulty": testDifficultyLevel.value,
        "user_course_id": startedCourse.id
    }
    await aisStore.smartGenerate(check)

    if (aisStore.questionDetailList) {
        aisStore.questionDetailList = []
    }
    if (aisStore.questionData) {
        for(const q of aisStore.questionData) {
            const result = await aisStore.getQuestionDetail(q.question)
            aisStore.questionDetailList?.push(result)
        }
    }
    aisStore.getLastUserCheckSkills()
    aisStore.questionDataForComplane = aisStore.questionDetailList[0]
    return router.push('/training')
}

// Генерация вопросов end
onMounted(async () => {
    const course = aisStore.startedCourses.find(c => c.course === aisStore.selectedCourse[0].id)
    await aisStore.getCourseById(course?.id)
});

// Page Reload
const handleBeforeUnload = (event: BeforeUnloadEvent) => {
  event.preventDefault()
  event.returnValue = ''
  localStorage.setItem('shouldRedirect', 'true')
}

onMounted(() => {
  window.addEventListener('beforeunload', handleBeforeUnload)
})

onBeforeUnmount(() => {
  window.removeEventListener('beforeunload', handleBeforeUnload)
})
// Page Reload
</script>

<style scoped lang="scss">

@import '../sass/main.scss';

//circle 

.circle-big {
    position: relative;
    width: 114px;
    height: 114px;
    margin: 30px auto 25px auto;
}

.circle-big svg {
    width: 114px;
    height: 114px;
}
.bg {
    fill: none;
    stroke-width: 10px;
    stroke: #ffffff;
}
.progress {
  fill: none;
  stroke-width: 10px;
  stroke: $main-blue;
  stroke-linecap: round;
  stroke-dasharray: 326.56;
  transform: rotate(-90deg);
  transform-origin: 50% 50%;
  animation: big 2s ease-in-out;
}
.circle-big__text {
    position: absolute;
    width: 100%;
    top: 37px;
    font-size: 20px;
    text-align: center;
    line-height: 22px;
}
.circle-big__text {
    color: $main-blue;
}
.circle-big__text-progress {
    font-size: 14px;
}

@keyframes big {
  from {
    stroke-dashoffset: 326.56;
  }
}
//circle end

.container__flex {
    display: flex;
    gap: 20px;
}
.container__bg {
    background-color: $light-blue;
}
.container-name {
    width: 100%;
    padding: 10px 15vw;

    @media (max-width: 1440px) {
        padding: 10px 10vw;
    }
    @media (max-width: 600px) {
        padding: 10px 0;
    }
}
.container-name__title {
    width: 100%;
    padding: 20px 40px;
    border-radius: 0.625rem;

    @media (max-width: 440px) {
        font-size: 16px;
    }
}

.content {
    height: 100%;
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.link-line {
    padding-top: 0.375rem;
    padding-bottom: 0.375rem;
    display: flex;
    align-items: center;
    gap: 2.5rem;
}
.margin-top {
    margin-top: 1.5rem;
}

.selectors {
    display: flex;
    flex-direction: column;
    gap: 20px;
    width: 100%;
}
.selector {
    width: 100%;
    display: flex;
    flex-direction: column;
    border: 1px solid $border;
    border-radius: 0.625rem;
    padding: 1rem;
    gap: 20px;
}
.selector__header {
    display: flex;
    gap: 40px;
    justify-content: space-between;
}
.selector__text {
    display: flex;
    flex-direction: column;
    gap: 0.8rem;
}
.selector__title {
    font-size: 22px;
    color: $main-blue;
}
.selector__info {
    display: flex;
    gap: 20px
}
.selector__data {
    display: flex;
    gap: 6px;
}
.selector__action {
    display: flex;
    flex-direction: column;
    align-items: end;
    justify-content: space-between;
}
.selector__buttons {
    display: flex;
    gap: 20px;
    flex-wrap: wrap;
    justify-content: end;
}
.droppers {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    justify-content: end;
}
.selector__button {
    height: 40px;
    cursor: pointer;
    width: 200px;
    background-color: $main-blue;
    border-radius: 0.5rem;
    color: white;
}

.info {
    display: flex;
    flex-direction: column;
    gap: 20px;
    border-radius: 0.625rem;
    background-color: $light-blue;
    padding: 20px 40px;
    height: 100%;
}
.progress-bar {
    width: 100%;
}
.progress-bar__content {
    display: flex;
    gap: 10px;
    align-items: center;
    margin-top: 10px;

    @media (max-width: 440px) {
        flex-wrap: wrap;
        justify-content: center;
    }
}

.statistic {
    display: flex;
    flex-direction: column;
    gap: 10px;
}
.statistic__column {
    display: flex;
    flex-direction: column;
    gap: 6px;
}
.statistic__value {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 120px;
    padding: 10px 0;
    background-color: #d7dfef;
    border-radius: 6px;
}

.info__buttons {
    display: flex;
    flex-direction: column;
    gap: 20px;
}
.info__button {
    width: 300px;
    align-items: center;
    display: flex;
    gap: 1.25rem;
    background-color: white;
    padding: 0 20px;
}
.info__button-img {
    width: 2.2rem;
    height: 2.2rem;
}

.dropper {
    cursor: pointer;
    position: relative;
}
.dropper__title {
    display: flex;
    justify-content: center;
    align-items: center;
    border: 1px solid $border;
    border-radius: 0.5rem;
    height: 40px;
    width: 200px;

    &:hover {
        background-color: $border;
    }
}
.dropper__list {
    z-index: 10;
    border-radius: 0.5rem;
    width: 100%;
    position: absolute;
    top: 44px;
    left: 0;
    background-color: white;
    box-shadow: 0px 0px 30px $border;
}
.dropper__item {
    width: 100%;
    padding: 10px 1rem;
    text-align: center;
    &:hover {
        background-color: $border;
    }
}
.dropper__arrow {
    display: inline-block;
    margin-left: 10px;
    width: 0;
    height: 0;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid black;
    transition: transform 0.3s;
}
.dropper__arrow--up {
    transform: rotate(180deg);
}

@media (max-width: 360px) {
    .selector__info {
        flex-wrap: wrap;
    }
}
@media (max-width: 600px) {
    .container {
        padding: 0 4vw;
    }
    .info {
        padding: 20px 20px;
        flex-wrap: wrap;
    }
    .info__button {
        width: 100%;
        text-align: start
    }
    .selector__buttons {
        flex-wrap: wrap;
    }
}
@media (max-width: 1024px) { 
    .info {
        width: 100%;
    }
    .info__button {
        width: 100%;
    }
    .container__flex {
        flex-wrap: wrap;
    }
    .manage {
        flex-wrap: wrap;
    }
    .selector {
        flex-wrap: wrap;
    }
    .selector__action {
        width: 100%;
        gap: 20px;
    }
    .selector__svg {
        display: none;
    }
}

</style>