<template>
    <div class="content">
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
            <div class="container">
                <div class="tickets tickets--margin">
                    <p class="fw-bold fs-20">Выберите билет</p>
                    <div class="tickets__list">
                        <div v-for="(ticket, index) in ticketsInfo" class="ticket" :class="{ selected : index === selectedTicket }" @click="select(index, ticket)">
                            <p class="fw-bold fs-18" :style="`color: ${index === selectedTicket ? '#ffffff' : '#333333'};`">Билет {{ index + 1 }}</p>
                            <div 
                                class="ticket__progress"
                                :style="{ backgroundColor: chooseBackgroundColor(ticket.status)}"
                            >
                                {{ showStatus(ticket.status) }}
                            </div>
                        </div>
                    </div>
                    <div class="creator">
                        <div class="creator__text">
                            <h1 class="white fs-18 fw-bold">Генерация нового билета</h1>
                            <div class="creator__data">
                                <div class="selector__data">
                                    <p class="white fs-14">Вопросов в курсе:</p>
                                    <p class="yellow fs-14 fw-bold">444</p>
                                </div>
                                <div class="selector__data">
                                    <p class="white fs-14">Вопросов в билете:</p>
                                    <p class="yellow fs-14 fw-bold">3</p> 
                                </div>
                            </div>
                        </div>
                        <button class="button" @click="generateCheck">Сгенерировать билет</button>
                    </div>
                    <div class="button-position" :class="{ disabled : selectedTicket === null }">
                        <button :disabled="selectedTicket === null" class="button tickets__button" @click="startTesting">Начать</button>
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

import { computed, onMounted, ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from "../store"

const router = useRouter()
const aisStore = useStore()

function goBack(): void {
    router.push('/course')
}

const ticketsInfo = computed(() => {
    return aisStore.testingInfo['tickets']
})

function chooseBackgroundColor(status) {
    if (status === 'Not started') {
        return '#d8efff'
    }
    if (status === 'Done') {
        return '#87ffc1'
    }
    if (status === 'Failed') {
        return '#ffd4d4'
    }
}

const selectedTicket = ref(null)    
function select(index, ticket) {
    selectedTicket.value = index
    aisStore.selectedTestId = ticket.id
}

async function startTesting() {

    aisStore.testingDetail = {}
    const result = await aisStore.getTestingDetail(aisStore.selectedTestId)
    aisStore.testingDetail = result

    router.push('/testing')
}

function showStatus(id) {
    if (id === "Not started") return "Не начат"
    if (id === "Done") return "Пройден"
    if (id === "Failed") return "Провален"
}

// Generate Random Ticket

async function generateCheck() {
    const startedCourse = aisStore.startedCourses.find(c => c.course === aisStore.selectedCourse[0].id)
    if (!startedCourse) throw new Error('Course not found!')
    const data = {
        "user_course_id": startedCourse?.id,
    }
    await aisStore.generateRandomTicket(data)

    const id = aisStore.selectedCourse[0].testing?.id
    
    aisStore.getTestingInfo(id)

    // При генерации билета, сделать обновление и его отображение
}
// Generate Random Ticket end

</script>

<style scoped lang="scss">

@import '../sass/main.scss';

.content {
    height: 100%;
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.container {
  padding: 0 20vw;
  width: 100%;
}
.container__bg {
    background-color: $light-blue;
}

.link-line {
    padding-top: 0.375rem;
    padding-bottom: 0.375rem;
    display: flex;
    align-items: center;
    gap: 2.5rem;
}

.tickets {
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
}
.tickets--margin {
    margin-top: 2.5rem;
}
.tickets__list {
    display: flex;
    flex-direction: column;
    gap: 0.625rem;
}
.ticket {
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.625rem 1.875rem;
    border: 1px solid $border;
    border-radius: 0.625rem;

    flex-wrap: wrap;
    gap: 0.625rem;

    &:hover {
        box-shadow: 0px 0px 20px $border;
    }
}

.selected {
    background-color: $main-blue;
}
.disabled {
    opacity: 0.4;
}

.ticket__progress {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 2.5rem;
    border-radius: 0.375rem;
    width: 140px;
    padding: 10px 10px;
}
.tickets__button {
    color: white;
    width: 18.75rem;
    background-color: $main-blue;
}
.button-position {
    width: 100%;
    display: flex;
    justify-content: end;
}

.creator {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #436175;
    padding: 1.4rem;
    border-radius: 0.5rem;
    gap: 1rem;
    flex-wrap: wrap;
}
.creator__text {
    display: flex;
    flex-direction: column;
    gap: 10px;
}
.creator__data {
    display: flex;
    gap: 10px;
}
.white {
    color: white;
}
.yellow {
   color: #ffca00;
}
.selector__data {
    display: flex;
    gap: 6px;
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
    width: 300px;

    &:hover {
        background-color: $border;
    }
}
.dropper__list {
    border-radius: 0.5rem;
    width: 300px;
    position: absolute;
    top: 44px;
    left: 0;
    background-color: white;
    box-shadow: 0px 0px 30px $border;
    z-index: 10;
}
.dropper__item {
    width: 100%;
    padding: 10px 1rem;
    text-align: center;
    &:hover {
        background-color: $border;
    }
}

.button {
    max-width: 300px;
}

@media (max-width: 430px) {
    .tickets__button {
        width: 100%;
    }
}
@media (max-width: 600px) {
    .container {
        padding: 0 4vw;
    }
}
</style>