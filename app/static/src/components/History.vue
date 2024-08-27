<template>
    <div class="content">
        <div>
            <Header />
            <div class="container container__bg">
                <div class="manage margin-top link-line">
                    <button class="button-back" @click="goBack">
                        <svg class="button-back__arrow" width="30px" height="30px" viewBox="0 0 24 24" fill="none">
                            <path d="M14.2893 5.70708C13.8988 5.31655 13.2657 5.31655 12.8751 5.70708L7.98768 10.5993C7.20729 11.3805 7.2076 12.6463 7.98837 13.427L12.8787 18.3174C13.2693 18.7079 13.9024 18.7079 14.293 18.3174C14.6835 17.9269 14.6835 17.2937 14.293 16.9032L10.1073 12.7175C9.71678 12.327 9.71678 11.6939 10.1073 11.3033L14.2893 7.12129C14.6799 6.73077 14.6799 6.0976 14.2893 5.70708Z"/>
                        </svg>
                        <p class="button-back__text fw-bold">Назад</p>
                    </button>
                </div>
            </div>
            <div class="container container__header">
                <div class="fs-18 fw-bold">История прохождения</div>
            </div>
            <div class="container">
                <div class="history-list">
                    <div class="history">
                        <div 
                            v-for="(course, index) in paginatedItems" 
                            class="history__content"
                        >
                            <div class="history__item">
                                <div class="history__items">
                                    <div class="history__item-header">
                                        <p class="fw-bold fs-18">{{ typeText(course.type) }}</p>
                                        <div 
                                            class="history__item-status fs-14 fw-bold" 
                                            :style="{ backgroundColor: chooseBackgroundColor(course.status)}"
                                        >{{ statusText(course.status) }}</div>
                                    </div>
                                    <div class="history__item-body">
                                        <div class="history__item-info">
                                            <div class="selector__data">
                                                <p class="fs-14 main-blue">Начато:</p>
                                                <p class="fs-14 main-blue fw-bold">{{ createTime(course.created_at) }}</p>
                                            </div>
                                            <!-- Добавить сложность для Обучения (showDifText) -->
                                            <div class="selector__data">
                                                <p class="fs-14 main-blue">Вопросов:</p>
                                                <p class="fs-14 main-blue fw-bold">{{ course.question_count }}</p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <button
                                        v-if="course.status === 'In Progress'"
                                        class="button history__button"
                                        @click="openTestPage(course)"
                                    >
                                    Продолжить
                                    </button>
                            </div>
                        </div>
                        
                        <Pagination
                            v-if="totalItems > 15"
                            class="pagination"
                            :current-page="currentPage"
                            :items-per-page="itemsPerPage"
                            :total-items="totalItems"
                            @update:currentPage="currentPage = $event"
                        />
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
import Pagination from './Pagination.vue'

import { computed, onMounted, ref, reactive } from 'vue'
import { useStore } from "../store"
import { useRouter } from 'vue-router'

const router = useRouter()
const aisStore = useStore()

function goBack() {
    router.push('/course')
}

// Pagination

const currentPage = ref(1)
const itemsPerPage = 15;
const totalItems = computed(() => aisStore.courseHistory.length)

const paginatedItems = computed(() =>
    aisStore.courseHistory.slice(
        (currentPage.value - 1) * itemsPerPage,
        currentPage.value * itemsPerPage
    )
);

// Pagination end

async function openTestPage(value) {

    if (value.type === 'check_skill' && value.status === 'In Progress') {

        if (aisStore.questionDetailList) {
            aisStore.questionDetailList = []
        }
        if (aisStore.questionData) {
            aisStore.questionData = []
        }

        await aisStore.getUserCkeckSkillsQuestions()
        const data = aisStore.allQuestionsData.filter(q => q.user_check_skills === value.id)
        aisStore.questionData = data

        for(const q of aisStore.questionData) {
            const result = await aisStore.getQuestionDetail(q.question)
            aisStore.questionDetailList?.push(result)
        }

        aisStore.lastCheckSkills = {}
        aisStore.lastCheckSkills = value

        console.log('value', value.id)

        return router.push('/training')
    }
    
}

function typeText(value) {
    if (value === 'check_skill') {
        return 'Режим обучения'
    }
    if (value === 'ticket') {
        return 'Тестирование'
    }
}
function statusText(value) {
    if (value === 'In Progress') {
        return 'В процессе'
    }
    if (value === 'Completed') {
        return 'Завершен'
    }
    if (value === 'Not started') {
        return 'Не окончен'
    }
    if (value === 'Failed') {
        return 'Провален'
    }
    if (value === 'Done') {
        return 'Пройден'
    }
}
function chooseBackgroundColor(status) {
    if (status === 'Not started' || status === 'In Progress') {
        return '#d8efff'
    }
    if (status === 'Done' || status === 'Completed') {
        return '#87ffc1'
    }
    if (status === 'Failed') {
        return '#ffd4d4'
    }
}
function showDifText(value) {
    if (value === 'Easy') {
        return 'Легко'
    }
    if (value === 'Medium') {
        return 'Средне'
    }
    if (value === 'Hard') {
        return 'Тяжело'
    }
}

function createTime(value) {
    const date = new Date(value)

    const formattedDate = date.toISOString().split('T')[0]
    const formattedTime = date.toISOString().split('T')[1].substring(0, 5)

    return `${formattedDate} в ${formattedTime}`
}

</script>

<style scoped lang="scss">

@import '../sass/main.scss';

.container {
  padding: 0 20vw;
  width: 100%;
}
.container__bg {
    background-color: $light-blue;
}
.content {
    height: 100%;
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.container__header {
    padding-top: 20px;
    padding-bottom: 20px;
}

.link-line {
    padding-top: 0.375rem;
    padding-bottom: 0.375rem;
    display: flex;
    align-items: center;
    gap: 2.5rem;
}
.history-list {
    display: flex;
    flex-direction: column;
}

.history {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 20px;
    width: 100%;
}
.history__content {
    display: flex;
    flex-direction: column;
    gap: 10px;
    width: 100%;
}
.history__item {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    width: 100%;
    padding: 20px;
    border: 1px solid $main-grey;
    border-radius: 0.375rem;
    transition: .2s;
    gap: 16px;
    align-items: center;
}
.history__items {
    display: flex;
    flex-direction: column;
    gap: 10px;
}
.history__item-header {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
}
.history__item-status {
    padding: 8px 14px;
    border-radius: 0.375rem;
    color: #4c5771;
}
.history__item-body {
    display: flex;
    justify-content: space-between;
    gap: 10px;
    align-items: center;
    flex-wrap: wrap;
}
.history__item-info {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}
.history__button {
    max-width: 200px;
    height: 40px;
    transition: .2s;
}
.selector__data {
    display: flex;
    gap: 6px;
}

@media (max-width: 600px) {
    .container {
        padding-left: 4vw;
        padding-right: 4vw;
    }
    .question__title {
        padding-right: 1.5rem;
    }
    .question__desc {
        padding-right: 1rem;
    }
}
</style>