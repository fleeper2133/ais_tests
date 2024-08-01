<template>
    <div class="content">
        <div>
            <Header />
            <div class="container container__bg link-line">
                <router-link to="/course">
                    <button class="button-back">
                        <svg class="button-back__arrow" width="30px" height="30px" viewBox="0 0 24 24" fill="none">
                            <path d="M14.2893 5.70708C13.8988 5.31655 13.2657 5.31655 12.8751 5.70708L7.98768 10.5993C7.20729 11.3805 7.2076 12.6463 7.98837 13.427L12.8787 18.3174C13.2693 18.7079 13.9024 18.7079 14.293 18.3174C14.6835 17.9269 14.6835 17.2937 14.293 16.9032L10.1073 12.7175C9.71678 12.327 9.71678 11.6939 10.1073 11.3033L14.2893 7.12129C14.6799 6.73077 14.6799 6.0976 14.2893 5.70708Z"/>
                        </svg>
                        <p class="button-back__text fw-bold">Назад</p>
                    </button>
                </router-link>
                <p class="fw-bold">Проверить себя</p>
            </div>
            <div>
                <div class="container ticket-list">
                    <div class="tickets">
                        <div 
                            @click="selectQuestion(value['number_in_check'] - 1)"
                            class="ticket" 
                            :style="{ backgroundColor: whatBgColor(value.status), border: whatBorder(value.status)}"
                            v-for="(value, key) in aisStore.questionData"
                            :key="key"
                        >
                            <p class="fw-bold">{{ value.number_in_check }}</p>
                        </div>
                    </div>
                    <div class="favorites">
                        <p>Добавить вопрос в избранное</p>
                        <svg class="star" viewBox="-0.5 0 25 25" fill="none">
                            <path d="M12.71 3.45001L15.17 7.94C15.2272 8.04557 15.307 8.1371 15.4039 8.20801C15.5007 8.27892 15.6121 8.3274 15.73 8.34998L20.73 9.29999C20.8726 9.327 21.0053 9.39183 21.1142 9.48767C21.2232 9.58352 21.3044 9.70688 21.3494 9.84485C21.3943 9.98282 21.4014 10.1303 21.3698 10.272C21.3383 10.4136 21.2693 10.5442 21.17 10.65L17.66 14.38C17.5784 14.4676 17.5172 14.5723 17.4809 14.6864C17.4446 14.8005 17.4341 14.9213 17.45 15.04L18.09 20.12C18.1098 20.2633 18.0903 20.4094 18.0337 20.5425C17.9771 20.6757 17.8854 20.791 17.7684 20.8762C17.6514 20.9613 17.5135 21.0132 17.3694 21.0262C17.2253 21.0392 17.0804 21.0129 16.95 20.95L12.32 18.77C12.2114 18.7155 12.0915 18.6871 11.97 18.6871C11.8485 18.6871 11.7286 18.7155 11.62 18.77L6.99 20.95C6.85904 21.0119 6.71392 21.0375 6.56971 21.0242C6.4255 21.0109 6.28751 20.9591 6.17008 20.8744C6.05265 20.7896 5.96006 20.6749 5.90201 20.5422C5.84396 20.4096 5.82256 20.2638 5.84 20.12L6.49 15.04C6.50596 14.9213 6.49542 14.8005 6.45911 14.6864C6.4228 14.5723 6.36162 14.4676 6.28 14.38L2.76999 10.65C2.67072 10.5442 2.60172 10.4136 2.57017 10.272C2.53861 10.1303 2.54568 9.98282 2.59064 9.84485C2.63561 9.70688 2.71683 9.58352 2.82578 9.48767C2.93473 9.39183 3.06742 9.327 3.21 9.29999L8.21 8.34998C8.32789 8.3274 8.43929 8.27892 8.53614 8.20801C8.63299 8.1371 8.71286 8.04557 8.76999 7.94L11.28 3.45001C11.349 3.32033 11.4521 3.21187 11.578 3.13623C11.704 3.0606 11.8481 3.02063 11.995 3.02063C12.1419 3.02063 12.2861 3.0606 12.412 3.13623C12.538 3.21187 12.641 3.32033 12.71 3.45001V3.45001Z" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                    </div>
                </div>
                <div class="container__bg">
                    <div class="container answers">
                        <div v-if="currentQuestionIndex !== null">
                            <div class="title">
                                <p class="grey-text">Вопрос <span class="grey-text">{{ currentQuestionIndex + 1 }}</span></p>
                                <h1 class="fs-18" >{{ currentQuestion.question_text }}</h1>
                            </div>
                            <div class="answers">
                                <div
                                    v-for="(answer, answerIndex) in currentQuestion.varients"
                                    class="answer"
                                    :class="[selectedField(answer.answer_number) ? 'selected' : null, (aisStore.questionData[currentQuestionIndex]?.answer_items || []).includes(answer.answer_number) ? 'selected' : null]"
                                    :key="answerIndex"
                                    @click="selectAnswer(answer.answer_number)"
                                >
                                    {{ answer.answer_text }}
                                </div>
                            </div>
                        </div>
                        <div class="buttons-panel">
                            <button class="button-back" @click="previousQuestion">
                                <svg class="button-back__arrow" width="30px" height="30px" viewBox="0 0 24 24" fill="none">
                                    <path d="M14.2893 5.70708C13.8988 5.31655 13.2657 5.31655 12.8751 5.70708L7.98768 10.5993C7.20729 11.3805 7.2076 12.6463 7.98837 13.427L12.8787 18.3174C13.2693 18.7079 13.9024 18.7079 14.293 18.3174C14.6835 17.9269 14.6835 17.2937 14.293 16.9032L10.1073 12.7175C9.71678 12.327 9.71678 11.6939 10.1073 11.3033L14.2893 7.12129C14.6799 6.73077 14.6799 6.0976 14.2893 5.70708Z"/>
                                </svg>
                                <p class="button-back__text fw-bold">Предыдущий вопрос</p>
                            </button>
                            <button v-if="aisStore.questionData[currentQuestionIndex].status === 'Not Answered'" :disabled="selectedAnswer.length === 0" class="button answers__button" :class="{ disabled: selectedAnswer.length === 0 }" @click="send()">Ответить</button>
                            <button class="button-back" @click="nextQuestion">
                                <p class="button-back__text fw-bold">Следующий вопрос</p>
                                <svg class="button-back__arrow buttons-panel__svg" width="30px" height="30px" viewBox="0 0 24 24" fill="none">
                                    <path d="M14.2893 5.70708C13.8988 5.31655 13.2657 5.31655 12.8751 5.70708L7.98768 10.5993C7.20729 11.3805 7.2076 12.6463 7.98837 13.427L12.8787 18.3174C13.2693 18.7079 13.9024 18.7079 14.293 18.3174C14.6835 17.9269 14.6835 17.2937 14.293 16.9032L10.1073 12.7175C9.71678 12.327 9.71678 11.6939 10.1073 11.3033L14.2893 7.12129C14.6799 6.73077 14.6799 6.0976 14.2893 5.70708Z"/>
                                </svg>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <Footer />
    </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useStore, GenerateCheckResponse } from "../store"

import Header from './Header.vue';
import Footer from './Footer.vue';

const router = useRouter()
const aisStore = useStore()

type AnswerIndex = number;

const currentQuestionIndex = ref(0)
const selectedAnswer = ref<AnswerIndex[]>([])
const varientsLength = ref(0)
const selectedQuestionId = ref<number>(0)
// const answeredList = ref([])

async function getVarientsLength() {
    if (aisStore.questionDetailList) {
        varientsLength.value = await aisStore.questionDetailList[currentQuestionIndex.value].varients.length
    }
}

const currentQuestion = computed(() => {

    if (aisStore.questionDetailList) {
        getVarientsLength()
        return aisStore.questionDetailList[currentQuestionIndex.value]
    }
})

function selectAnswer(number) {
    const index = selectedAnswer.value.indexOf(number);
    if (index !== -1) {
        selectedAnswer.value.splice(index, 1);
    } else if (selectedAnswer.value.length === varientsLength.value) {
        return
    } else {
        selectedAnswer.value.push(number);
    }
}

function selectedField(number) {
    return selectedAnswer.value.indexOf(number) !== -1
}

function selectQuestion(index) {
    currentQuestionIndex.value = index
    selectedAnswer.value = []
    varientsLength.value = 0
}
function previousQuestion() {
    if (currentQuestionIndex.value > 0) {
        currentQuestionIndex.value--
        selectedAnswer.value = []
        varientsLength.value = 0
    }
}
function nextQuestion() {
    if (currentQuestionIndex.value < aisStore.questionDetailList.length - 1) {
        currentQuestionIndex.value++
        selectedAnswer.value = []
        varientsLength.value = 0
    }
}

async function send() {
    if (aisStore.questionData) {
        const way = aisStore.questionData.find(q => q.number_in_check === currentQuestionIndex.value + 1)
        selectedQuestionId.value = way.id

        if (selectedAnswer) {
            const toSend: GenerateCheckResponse = {
                "answer_items": selectedAnswer.value
            }
            await aisStore.createAnswer(selectedQuestionId.value, toSend)


            // Логика завершения курса. Нужна будет кнопка 'завершить тестирование'. Чтобы человек мог посмотреть свои ошибки (не выкидывать просто так)

            // if (answeredList.value.length === aisStore.questionDetailList.length - 1) {
            //     if (aisStore.userCheckSkills) aisStore.endTraining(aisStore.userCheckSkills)
            //     здесь лучше сделать пробежку по aisStore.questionWorkStats[id].status, и если все статусы объектов не равны стандарту, завершать курс
            //     router.push('/course')
            // } else {
            //     // Сюда добавлять ответ с wrang/right, чтобы потом легче отслеживать
            //     // answeredList.value.push(aisStore.trainingAnswer) - // для определения длинный массива
            //     console.log(aisStore.trainingAnswer['id'])
            // }
        }
    }
    

    if (aisStore.questionData) {
        const index = aisStore.questionData.findIndex(q => q.id === aisStore.trainingAnswer['id']);
        if (index !== -1) {
            aisStore.questionData.splice(index, 1, aisStore.trainingAnswer)
            console.log("aisStore.questionData[index]['answer_items']", aisStore.questionData[index], aisStore.trainingAnswer)
            aisStore.questionData[index]['answer_items'] = [...selectedAnswer.value]
        }
    }

    currentQuestionIndex.value++
    selectedAnswer.value = []
}


// Запоминание

function whatBgColor(status) {
    if (status === 'Wrong') {
        return '#ffb2c1';
    }
    if (status === 'Right') {
        return '#acffac';
    }
    return 'transparent';
}

function whatBorder(status) {
    if (status === 'Wrong' || status === 'Right') {
        return 'none';
    }
}


// Запоминание end


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

.ticket-list {
    display: flex;
    flex-direction: column;
    gap: 0.625rem;
    padding-top: 1.875rem;
    padding-bottom: 1.875rem;
}
.tickets {
    display: flex;
    gap: 0.625rem;
    flex-wrap: wrap;
}

.ticket {
    cursor: pointer;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 2.5rem;
    height: 2.5rem;
    border-radius: 0.25rem;
    border: 2px solid $second-blue;

    &:hover {
        transform: scale(1.1);
        box-shadow: 0px 0px 10px $border;
    }
}

.favorites {
    display: flex;
    gap: 0.625rem;
    align-items: center;
    justify-content: end;
}

.answers {
    display: flex;
    flex-direction: column;
    gap: 1.875rem;
    padding-top: 1.875rem;
    padding-bottom: 1.875rem;
}
.title {
    display: flex;
    flex-direction: column;
    gap: 10px;
    padding-left: 1.875rem;
    padding-right: 1.875rem;
}
.answers {
    display: flex;
    flex-direction: column;
    gap: 10px;
}
.answer {
    cursor: pointer;
    padding: 1.875rem 1.875rem;
    border-radius: 1rem;
    border: 2px solid $border;
    background-color: white;

    &:hover {
        box-shadow: 0px 0px 30px $border;
    }
}
.answers__button {
    width: 300px;
    margin: 0 auto;
}

.buttons-panel {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
}
.buttons-panel__svg {
    transform: rotate(180deg)
}

.selected {
    background-color: #bbdbff;
    border: 2px solid $main-blue;
}
.disabled {
    opacity: 0.4;
}


@media (max-width: 600px) {
    .container {
        padding: 0 4vw;
    }
    .ticket-list {
        padding-top: 1.875rem;
        padding-bottom: 1.875rem;
    }
    .link-line {
        padding-top: 0.375rem;
        padding-bottom: 0.375rem;
    }
    .answers {
        padding-top: 1.875rem;
        padding-bottom: 1.875rem;
    }
    .answers__button {
        width: 100%;
    }
}

@media (max-width: 1024px) {
    .buttons-panel {
        gap: 20px;
        align-items: center;
        justify-content: center
    }
}
</style>