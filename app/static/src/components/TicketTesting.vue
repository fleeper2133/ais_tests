<template>
    <div class="content">
        <div>
            <Header />
            <div class="container container__bg link-line">
                <button class="button-back" @click="back">
                    <svg class="button-back__arrow" width="30px" height="30px" viewBox="0 0 24 24" fill="none">
                        <path d="M14.2893 5.70708C13.8988 5.31655 13.2657 5.31655 12.8751 5.70708L7.98768 10.5993C7.20729 11.3805 7.2076 12.6463 7.98837 13.427L12.8787 18.3174C13.2693 18.7079 13.9024 18.7079 14.293 18.3174C14.6835 17.9269 14.6835 17.2937 14.293 16.9032L10.1073 12.7175C9.71678 12.327 9.71678 11.6939 10.1073 11.3033L14.2893 7.12129C14.6799 6.73077 14.6799 6.0976 14.2893 5.70708Z"/>
                    </svg>
                    <p class="button-back__text fw-bold">Выйти</p>
                </button>
                <p class="fw-bold">Режим тестирования</p>
            </div>
            <div>
                <div class="container ticket-list">
                    <div v-if="isTestDone" class="fw-bold fs-18">
                        Итог:
                    </div>
                    <div class="tickets">
                        <div 
                            @click="selectQuestion(key)"
                            class="ticket"
                            :style="{ 
                                backgroundColor: whatBgColor(value, value['answer_items']),
                                border: whatBorder(value, value['answer_items']),
                                transform: key === currentQuestionIndex ? 'scale(1.15)' : 'scale(1)',
                            }"
                            v-for="(value, key) in allQuestions"
                            :key="key"
                        >
                            <p class="fw-bold" :style="{ color: whatFontColor(value['answer_items']) }">{{ key + 1 }}</p>
                        </div>
                    </div>
                    <div v-if="!isTestDone" class="timer">
                        <svg width="30px" height="30px" viewBox="0 0 24.00 24.00" fill="none" stroke="#ffffff" transform="matrix(1, 0, 0, 1, 0, 0)rotate(0)">
                            <g id="SVGRepo_bgCarrier" stroke-width="0"/>
                            <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round" stroke="#CCCCCC" stroke-width="0.288"/>
                            <g id="SVGRepo_iconCarrier"> <path d="M4.51555 7C3.55827 8.4301 3 10.1499 3 12C3 16.9706 7.02944 21 12 21C16.9706 21 21 16.9706 21 12C21 7.02944 16.9706 3 12 3V6M12 12L8 8" stroke="#ffffff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/> </g>
                        </svg>
                        <div class="timer__content">
                            <p class="timer__text">Времени осталось:</p>
                            <p class="timer__text">{{ timer }}</p>
                        </div>
                    </div>
                    <!-- <div v-if="!isTestDone" class="favorites">
                        <p>Добавить вопрос в избранное</p>
                        <svg  class="star" viewBox="-0.5 0 25 25" :class="question.selected ? 'star--filled' : 'none'" @click.stop="favoriteQuestion($event, currentQuestion.id)">
                            <path d="M12.71 3.45001L15.17 7.94C15.2272 8.04557 15.307 8.1371 15.4039 8.20801C15.5007 8.27892 15.6121 8.3274 15.73 8.34998L20.73 9.29999C20.8726 9.327 21.0053 9.39183 21.1142 9.48767C21.2232 9.58352 21.3044 9.70688 21.3494 9.84485C21.3943 9.98282 21.4014 10.1303 21.3698 10.272C21.3383 10.4136 21.2693 10.5442 21.17 10.65L17.66 14.38C17.5784 14.4676 17.5172 14.5723 17.4809 14.6864C17.4446 14.8005 17.4341 14.9213 17.45 15.04L18.09 20.12C18.1098 20.2633 18.0903 20.4094 18.0337 20.5425C17.9771 20.6757 17.8854 20.791 17.7684 20.8762C17.6514 20.9613 17.5135 21.0132 17.3694 21.0262C17.2253 21.0392 17.0804 21.0129 16.95 20.95L12.32 18.77C12.2114 18.7155 12.0915 18.6871 11.97 18.6871C11.8485 18.6871 11.7286 18.7155 11.62 18.77L6.99 20.95C6.85904 21.0119 6.71392 21.0375 6.56971 21.0242C6.4255 21.0109 6.28751 20.9591 6.17008 20.8744C6.05265 20.7896 5.96006 20.6749 5.90201 20.5422C5.84396 20.4096 5.82256 20.2638 5.84 20.12L6.49 15.04C6.50596 14.9213 6.49542 14.8005 6.45911 14.6864C6.4228 14.5723 6.36162 14.4676 6.28 14.38L2.76999 10.65C2.67072 10.5442 2.60172 10.4136 2.57017 10.272C2.53861 10.1303 2.54568 9.98282 2.59064 9.84485C2.63561 9.70688 2.71683 9.58352 2.82578 9.48767C2.93473 9.39183 3.06742 9.327 3.21 9.29999L8.21 8.34998C8.32789 8.3274 8.43929 8.27892 8.53614 8.20801C8.63299 8.1371 8.71286 8.04557 8.76999 7.94L11.28 3.45001C11.349 3.32033 11.4521 3.21187 11.578 3.13623C11.704 3.0606 11.8481 3.02063 11.995 3.02063C12.1419 3.02063 12.2861 3.0606 12.412 3.13623C12.538 3.21187 12.641 3.32033 12.71 3.45001V3.45001Z" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                    </div> -->
                    <!-- доделать нажатие на звезду, переделать с yellow, под class -->
                    <!-- разобраться с question.selected, его тут нет -->
                </div>
                <div class="container__bg">
                    <div class="container answers">
                        <div v-if="currentQuestionIndex !== null && !isTestDone">
                            <div class="title">
                                <p class="grey-text">Вопрос <span class="grey-text">{{ currentQuestionIndex + 1 }}</span></p>
                                <h1 class="fs-18" >{{ currentQuestion['question_text'] }}</h1>
                            </div>
                            <div class="answers">
                                <div
                                    v-for="(answer, answerIndex) in currentQuestion.varients"
                                    class="answer"
                                    :class="{
                                        'selected': selectedField(answer.answer_number),
                                        'selected-answer': allQuestions[currentQuestionIndex].answer_items?.includes(answer.answer_number)
                                    }"
                                    :key="answerIndex"
                                    @click="selectAnswer(answer.answer_number, allQuestions[currentQuestionIndex]['answer_items'])"
                                >
                                    {{ answer.answer_text }}
                                </div>
                            </div>
                        </div>
                        
                        <div v-if="isTestDone" class="statistic">
                            <div class="statistic__status">
                                <p class="fs-20 fw-bold">Результат:</p>
                                <span class="fs-20 fw-bold statistic__status-item">{{ resultStatus }}</span>
                            </div>
                            <!-- Для отображения статуса, разобраться с обновление (баг на переключение вопросов) -->
                            <div 
                                v-for="(question, index) in allQuestions"
                                class="statistic__answer"
                                @click="selectQuestion(index)"
                            >
                                <div 
                                    class="statistic__answer-header" 
                                    :style="{ backgroundColor: question['status'] === 'Wrong' ? '#fff2f2' : '#d4e8ff', 
                                    border: question['status'] === 'Wrong' ? '2px solid #ff6969' : '2px solid #338DF4' }"
                                >
                                    <p class="fw-bold fs-14">Вопрос {{ index + 1 }}</p>
                                    <p>{{ question['question_text'] }}</p>
                                </div>
                                <div v-if="currentQuestionIndex === index" class="statistic__answer-body">
                                    <div class="statistic__showed-answers">
                                        <div class="statistic__showed-answer">
                                            <p class="fw-bold">Ваш ответ:</p>
                                            <span class="statistic__showed-item">{{ yourAnswer(question['answer_items'], question['varients']) }}</span>
                                        </div>
                                        <div class="statistic__showed-answer">
                                            <p class="fw-bold">Верный ответ:</p>
                                            <span class="statistic__showed-item">{{ correctAnswer(question['varients']) }}</span>
                                        </div>
                                    </div>
                                    <div class="statistic__normative">
                                        <p class="fw-bold fs-18">{{ question['normative_documents'].text }}<span class="fw-bold fs-18 statistic__normative-point">{{ question['normative_point'] }}</span></p>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="buttons-panel">
                            <button v-if="!isTestDone" class="button-back button-skip" @click="previousQuestion">
                                <svg class="button-back__arrow" width="30px" height="30px" viewBox="0 0 24 24" fill="none">
                                    <path d="M14.2893 5.70708C13.8988 5.31655 13.2657 5.31655 12.8751 5.70708L7.98768 10.5993C7.20729 11.3805 7.2076 12.6463 7.98837 13.427L12.8787 18.3174C13.2693 18.7079 13.9024 18.7079 14.293 18.3174C14.6835 17.9269 14.6835 17.2937 14.293 16.9032L10.1073 12.7175C9.71678 12.327 9.71678 11.6939 10.1073 11.3033L14.2893 7.12129C14.6799 6.73077 14.6799 6.0976 14.2893 5.70708Z"/>
                                </svg>
                                <p class="button-skip__text fw-bold">Назад</p>
                            </button>

                            <button v-if="!allQuestions[currentQuestionIndex]['answer_items'] && !isTestDone" :disabled="selectedAnswer.length === 0" class="button answers__button" :class="{ disabled: selectedAnswer.length === 0 }" @click="send()">Ответить</button>
                            <button v-if="isTestDone" @click="back" class="button answers__button end__button">Выйти</button>
                            
                            <button v-if="!isTestDone" class="button-back button-skip" @click="nextQuestion">
                                <p class="button-skip__text fw-bold">Дальше</p>
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
import { computed, onMounted, ref, watch, onUnmounted, onBeforeMount } from 'vue'
import { useRouter } from 'vue-router'
import { useStore, GenerateCheckResponse } from "../store"

import Header from './Header.vue'
import Footer from './Footer.vue'

const router = useRouter()
const aisStore = useStore()

type AnswerIndex = number;

const isTestDone = ref(false)
const currentQuestionIndex = ref(0)
const selectedAnswer = ref<AnswerIndex[]>([])
const varientsLength = ref(0)
const allQuestions = ref([])

function back() {
    // aisStore.testingDetail = {}
    // const result = aisStore.getTestingDetail(aisStore.selectedTestId)
    // aisStore.testingDetail = result
    router.push('/ticket-selection')
}

function yourAnswer(myAnswer, variants) {
    const correctVariant = variants.find(v => myAnswer.includes(v.answer_number))
    return correctVariant ? correctVariant.answer_text : 'Нет ответа'
}
function correctAnswer(variants) {
    const correctVariant = variants.find(variant => variant.correct === true)
    return correctVariant ? correctVariant.answer_text : 'Нет верного ответа'
}

// Timer
const timer = ref('30:00')
const totalSeconds = ref(30 * 60)
let interval

const startTimer = () => {
    interval = setInterval(() => {
        if (totalSeconds.value > 0) {
            totalSeconds.value--
            updateTimer()
        } else {
            clearInterval(interval)
        }
    }, 1000)
}

const stopTimer = () => {
    clearInterval(interval)
}

const getElapsedTime = () => {
    const elapsedSeconds = (30 * 60) - totalSeconds.value
    const hours = Math.floor(elapsedSeconds / 3600)
    const minutes = Math.floor((elapsedSeconds % 3600) / 60)
    const seconds = elapsedSeconds % 60

    return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`
}

const updateTimer = () => {
    const minutes = Math.floor((totalSeconds.value % 3600) / 60)
    const seconds = totalSeconds.value % 60

    timer.value = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`
}

// timer for question
const QuestionTimerValue = ref(0);
let QuestionIntervalId = null;

function startQuestionTimer() {

    if (QuestionIntervalId !== null) {
        clearInterval(QuestionIntervalId);
    }

    QuestionTimerValue.value = 0;

    QuestionIntervalId = setInterval(() => {
        QuestionTimerValue.value++;
    }, 1000);
}
// timer for question END

onMounted(() => {
    startTimer()
    startQuestionTimer()
})
onUnmounted(() => {
    clearInterval(interval)
})
watch(timer, (newValue) => {
    if (newValue === '00:00') {
        endTesting()
    }
})
// Timer END

function getVarientsLength() {
    const variants = allQuestions.value[currentQuestionIndex.value].varients
    varientsLength.value = variants?.length
}
let currentQuestion = computed(() => {
        getVarientsLength()
        return allQuestions.value[currentQuestionIndex.value]
})

async function selectAnswer(number, condition) {
    if (condition) {
        return
    }

    const index = selectedAnswer.value.indexOf(number);
    if (index !== -1) {
        selectedAnswer.value.splice(index, 1)
    } else if (selectedAnswer.value.length === varientsLength.value) {
        return
    } else {
        selectedAnswer.value.push(number)
    }
}

function selectedField(number) {
    return selectedAnswer.value.indexOf(number) !== -1;
}

function selectQuestion(index) {
    startQuestionTimer()
    currentQuestionIndex.value = index
    selectedAnswer.value = []
    varientsLength.value = 0
}
function previousQuestion() {
    startQuestionTimer()
    if (currentQuestionIndex.value > 0) {
        currentQuestionIndex.value--
        selectedAnswer.value = []
        varientsLength.value = 0
    } else {
        currentQuestionIndex.value = allQuestions.value.length - 1
        selectedAnswer.value = []
        varientsLength.value = 0
    }
}
function nextQuestion() {
    startQuestionTimer()
    if (currentQuestionIndex.value < allQuestions.value.length - 1) {
        currentQuestionIndex.value++
        selectedAnswer.value = []
        varientsLength.value = 0
    } else {
        currentQuestionIndex.value = 0
        selectedAnswer.value = []
        varientsLength.value = 0
    }
}

function send() {

    allQuestions.value[currentQuestionIndex.value].answer_items = [...selectedAnswer.value];
    allQuestions.value[currentQuestionIndex.value].answer_time = QuestionTimerValue.value;

    const rightVarientsArray = currentQuestion.value?.varients.filter(v => v.correct === true)
    const answerNumbers = rightVarientsArray.map(v => v.answer_number)
    allQuestions.value[currentQuestionIndex.value].correct_answer_items = [...answerNumbers]

    selectedAnswer.value = []

    startQuestionTimer()
    
    setTimeout(() => {
        currentQuestionIndex.value++
    }, 200);
    
}

// Запоминание

function whatBgColor(value, answer) {

    if (answer) {
        if (value['status'] === 'Wrong') {
            return '#ff6969'
        }   
        return '#0098ff'
    }
    return 'transparent'
}
function whatBorder(value, answer) {
    if (value['status'] === 'Wrong') {
        return '#ff6969'
    }
    if (answer) return 'none'
}
function whatFontColor(value) {
    if (value) return '#ffffff'
}
// Запоминание end

const endTestingInfo = ref<Object>({})
const resultStatus = computed(() => {
    if (endTestingInfo.value['status'] === 'Failed') return 'Не сдан'
    if (endTestingInfo.value['status'] === 'Done') return 'Сдан'
})
async function endTesting() {
    isTestDone.value = true
    stopTimer()
    
    for(const q of allQuestions.value) {
        const toSend = {
            "answer_items": q['answer_items'],
            "answer_time": q['answer_time']
        }

        const response = await aisStore.createTicketAnswer(q['question_ticket_id'], toSend)
        // if (response) {
        //     q['status'] = response['status']
        // }
    }
    
    const sendingInfo = {
        // "time_ticket": getElapsedTime()
        "time_ticket": 10
        // Передать в секундах
    }
    endTestingInfo.value = await aisStore.makeEndTicket(aisStore.testingDetail['id'], sendingInfo)

    currentQuestionIndex.value = 0
}


const checkAllQuestionsAnswered = () => {
    if (allQuestions.value.every(question => question['answer_items'])) {
        isTestDone.value = true
        endTesting()
    }
}
watch(allQuestions, (newQuestions) => {
    checkAllQuestionsAnswered()
}, { deep: true })
onBeforeMount(async () => {
    allQuestions.value = aisStore.testingDetail['questions']
})

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

.timer {
    display: flex;
    align-items: center;
    gap: 10px;
    background-color: #0098ff;
    padding: 10px 20px;
    max-width: 300px;
    border-radius: 0.25rem;
}
.timer__content {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
}
.timer__text {
    color: white;
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
.end__button {
    margin-top: 20px;
    background-color: #0fa5eb;
}

.rate-container {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 10px;
}
.rate {
    display: flex;
    width: 100%;
    border-radius: 0.25rem;
    background-color: #f0faff;
}
.rate__item {
    cursor: pointer;
    padding: 10px 0;
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 5px;
    align-items: center;
    justify-content: center;
    transition: .2s;

    &:hover {
        background-color: #c0cfd6;
        transition: .2s;
    }
    &:hover .rate__smile {
        scale: 1.1;
        transition: .2s;
    }
}
.rate__smile {
    width: 26px;
    height: 26px;
    transition: .2s;
}

.button-skip {
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #d3eaff;
    border-radius: 0.25rem;
    padding: 10px 0;
    width: 240px;
    height: 3.75rem;

    &:hover {
        background-color: #abd7ff;
    }
}
.button-skip__text {
    color: $main-blue;
    text-align: start;
    transition: .2s;
}
.buttons-panel {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
}
.buttons-panel__svg {
    transform: rotate(180deg)
}

.question-status {
    width: 100%;
    margin-bottom: 30px;
    display: flex;
    flex-direction: column;
    gap: 20px;
}
.question-status__text {
    width: 100%;
    text-align: center;
}
.question-status__text-wrong {
    color: #9b1e1e;
}
.question-status__text-right {
    color: #269b37;
}
.question-status__description {
    display: flex;
    flex-direction: column;
    gap: 10px
}
.question-status__description-text {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.selected {
    background-color: #bbdbff;
    border: 2px solid $main-blue;
}
.selected-answer {
    background-color: #89bffb;
    border: 2px solid $main-blue;
}
.selected-right {
    background-color: #d4ffd0;
    border: 2px solid #2ac71b;
}
.selected-wrong {
    background-color: #ffe9e9;
    border: 2px solid #ff4a4a;
}
.correct-answer {
    background-color: #d4ffd0;
    border: 2px solid #2ac71b;
}
.disabled {
    opacity: 0.4;
}


// stats

.stats {
    margin-top: 10vh;
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 60px;
}
.stats__content {
    display: flex;
    flex-direction: column;
    width: 300px;
    gap: 10px;
}
.stats__answers {
    display: flex;
    justify-content: space-between;
}
.stats__content-button {
    margin-top: 20px;
}
.svg {
    width: 100%;
    height: 120px;
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
}
.svg__front {
    position: absolute;
    z-index: 3;
}
.svg__back {
    position: absolute;
    z-index: 2;
    opacity: 0.05;
}

// stats end

.statistic {
    padding-top: 10px;
    display: flex;
    flex-direction: column;
    gap: 20px;
}
.statistic__status {
    width: 100%;
    justify-content: center;
    display: flex;
    gap: 10px;
}
.statistic__status-item{
    color: #ff4e5d;
}
.statistic__answer {
    background-color: #eff8ff;
    border-radius: 0.5rem;
}
.statistic__answer-header {
    cursor: pointer;
    display: flex;
    flex-direction: column;
    padding: 30px;
    border-radius: 0.5rem;
    gap: 10px;
}
.statistic__answer-body {
    display: flex;
    flex-direction: column;
    padding: 30px;
    gap: 20px;
}
.statistic__showed-answers {
    display: flex;
    gap: 10px;
}
.statistic__showed-answer {
    display: flex;
    flex-direction: column;
    gap: 10px;
}
.statistic__showed-item {
    border: 2px solid rgb(193, 199, 224);
    border-radius: 0.5rem;
    padding: 14px;
    max-width: 500px;
    background-color: white;
    height: 100%;
}
.statistic__normative {
    display: flex;
    gap: 10px;
}
.statistic__normative-point {
    margin-left: 10px;
    color: #237aa3;
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
    .button-skip {
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