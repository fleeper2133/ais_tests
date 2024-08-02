<template>
    <div class="content">
        <div>
            <Header />
            <div class="container">
                <button class="button-back" @click="goBack">
                    <svg class="button-back__arrow" width="30px" height="30px" viewBox="0 0 24 24" fill="none">
                        <path d="M14.2893 5.70708C13.8988 5.31655 13.2657 5.31655 12.8751 5.70708L7.98768 10.5993C7.20729 11.3805 7.2076 12.6463 7.98837 13.427L12.8787 18.3174C13.2693 18.7079 13.9024 18.7079 14.293 18.3174C14.6835 17.9269 14.6835 17.2937 14.293 16.9032L10.1073 12.7175C9.71678 12.327 9.71678 11.6939 10.1073 11.3033L14.2893 7.12129C14.6799 6.73077 14.6799 6.0976 14.2893 5.70708Z"/>
                    </svg>
                    <p class="button-back__text fw-bold">Назад</p>
                </button>
                <div class="content__items">
                    <div 
                        class="search" 
                        @click.stop="makeFocus"
                        :style="`border: ${condition}`"
                    >
                        <input class="search__input" type="text" ref="searchInput" placeholder="Введите текст вопроса" v-model="inputText">
                        <svg v-if="inputText.length === 0" class="svg-icon magnifier" viewBox="0 0 24 24" fill="none">
                            <path d="M15.7955 15.8111L21 21M18 10.5C18 14.6421 14.6421 18 10.5 18C6.35786 18 3 14.6421 3 10.5C3 6.35786 6.35786 3 10.5 3C14.6421 3 18 6.35786 18 10.5Z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                        <svg v-else class="svg-icon clear" viewBox="0 0 1024 1024" @click="clearSearch()">
                            <path fill="#000000" d="M195.2 195.2a64 64 0 0 1 90.496 0L512 421.504 738.304 195.2a64 64 0 0 1 90.496 90.496L602.496 512 828.8 738.304a64 64 0 0 1-90.496 90.496L512 602.496 285.696 828.8a64 64 0 0 1-90.496-90.496L421.504 512 195.2 285.696a64 64 0 0 1 0-90.496z"/>
                        </svg>
                    </div>
                    <div class="questions" v-if="filterSearch.length > 0">
                        <div 
                            class="question" 
                            :style="`border: ${selectedQuestion === index ? '1px solid #338DF4' : '1px solid rgb(193, 199, 224)'}`" 
                            v-for="(question, index) in paginatedItems"
                            @click="selectedQuestion = selectedQuestion === index ? null : index"
                        >
                            <div class="question__main">
                                <div class="question__title fs-18 fw-bold">{{ question.question_text }}</div>
                                <svg  class="star" viewBox="-0.5 0 25 25" :class="question.selected ? 'star--filled' : 'none'" @click.stop="selectQuestion($event, question.id)">
                                    <path d="M12.71 3.45001L15.17 7.94C15.2272 8.04557 15.307 8.1371 15.4039 8.20801C15.5007 8.27892 15.6121 8.3274 15.73 8.34998L20.73 9.29999C20.8726 9.327 21.0053 9.39183 21.1142 9.48767C21.2232 9.58352 21.3044 9.70688 21.3494 9.84485C21.3943 9.98282 21.4014 10.1303 21.3698 10.272C21.3383 10.4136 21.2693 10.5442 21.17 10.65L17.66 14.38C17.5784 14.4676 17.5172 14.5723 17.4809 14.6864C17.4446 14.8005 17.4341 14.9213 17.45 15.04L18.09 20.12C18.1098 20.2633 18.0903 20.4094 18.0337 20.5425C17.9771 20.6757 17.8854 20.791 17.7684 20.8762C17.6514 20.9613 17.5135 21.0132 17.3694 21.0262C17.2253 21.0392 17.0804 21.0129 16.95 20.95L12.32 18.77C12.2114 18.7155 12.0915 18.6871 11.97 18.6871C11.8485 18.6871 11.7286 18.7155 11.62 18.77L6.99 20.95C6.85904 21.0119 6.71392 21.0375 6.56971 21.0242C6.4255 21.0109 6.28751 20.9591 6.17008 20.8744C6.05265 20.7896 5.96006 20.6749 5.90201 20.5422C5.84396 20.4096 5.82256 20.2638 5.84 20.12L6.49 15.04C6.50596 14.9213 6.49542 14.8005 6.45911 14.6864C6.4228 14.5723 6.36162 14.4676 6.28 14.38L2.76999 10.65C2.67072 10.5442 2.60172 10.4136 2.57017 10.272C2.53861 10.1303 2.54568 9.98282 2.59064 9.84485C2.63561 9.70688 2.71683 9.58352 2.82578 9.48767C2.93473 9.39183 3.06742 9.327 3.21 9.29999L8.21 8.34998C8.32789 8.3274 8.43929 8.27892 8.53614 8.20801C8.63299 8.1371 8.71286 8.04557 8.76999 7.94L11.28 3.45001C11.349 3.32033 11.4521 3.21187 11.578 3.13623C11.704 3.0606 11.8481 3.02063 11.995 3.02063C12.1419 3.02063 12.2861 3.0606 12.412 3.13623C12.538 3.21187 12.641 3.32033 12.71 3.45001V3.45001Z" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                                </svg>
                            </div>
                            <div v-if="selectedQuestion === index" class="question__desc grey-text">
                                <div class="line"></div>
                                <ul>
                                    <li v-for="varient in question.varients">
                                        <span :style="varient.correct ? 'color: green' : 'color: red'">{{ varient.answer_text }}</span>
                                    </li>
                                </ul>
                                
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
                    <div class="nothing-found"v-else>
                        По вашему запросу, ничего не найдено..
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

import { computed, onMounted, ref, watch } from 'vue'
import { useStore } from "../store"
import { useRouter } from 'vue-router'

const router = useRouter();
const aisStore = useStore()

const inputText = ref('')
function clearSearch() {
    if(this.inputText !== undefined ) {
        this.inputText = ''
    }
}
const filterSearch = computed(() => {
    if (!inputText.value) {
        return aisStore.courseQuestions;
    }

    return aisStore.courseQuestions.filter((question) => {
        return question.question_text.toLowerCase().includes(inputText.value.toLowerCase());
    });
});

const selectedQuestion = ref<number | null>(0)

const searchInput = ref<HTMLInputElement | null>(null);
function makeFocus() {
    if (searchInput.value) {
        searchInput.value.focus()
    }
}

function selectQuestion(event, id){

    event.target.classList.add('star--scaled');
    setTimeout(() => {
        event.target.classList.remove('star--scaled');
    }, 300);

    if(event.currentTarget.getAttribute('fill') == 'none')
    event.currentTarget.setAttribute('fill', 'yellow')
    else
    event.currentTarget.setAttribute('fill', 'none')
    aisStore.markQuestionSelected(id)
}

function goBack(): void {
    router.push('/course')
}

const condition = computed(() => {
    if (filterSearch.value.length === 0) {
        return '1px solid #ff1d4e'
    }
})

// Pagination

const currentPage = ref(1);
const itemsPerPage = 15;
const totalItems = computed(() => filterSearch.value.length)

const paginatedItems = computed(() =>
    filterSearch.value.slice(
        (currentPage.value - 1) * itemsPerPage,
        currentPage.value * itemsPerPage
    )
);

// Pagination end


watch(inputText, () => {
  currentPage.value = 1;
});
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
.content__items {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 20px;
}
.container {
  padding: 0 20vw;
  width: 100%;
}

.search {
    margin-top: 40px;
    cursor: text;
    display: flex;
    align-items: center;
    gap: 20px;
    padding: 16px 30px;
    border-radius: 0.375rem;
    background-color: #e3e6ef;
    border: 1px solid white;

    &:focus-within {
        border: 1px solid $main-grey;
    }
    &:focus-within {
        background-color: white;
    }
}
.search__input {
    width: 100%;
    height: 30px;
    background: none;
}
.magnifier {
    right: 25px;
    width: 25px;
    stroke: $main-grey;
}
.clear {
    cursor: pointer;
    right: 20px;
    width: 20px;
}

.questions {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 20px;
    height: 100%;
}
.question {
    cursor: pointer;
    padding: 20px 40px;
    border-radius: 0.625rem;
    display: flex;
    flex-direction: column;
    gap: 20px;
}
.question__main {
    display: flex;
    justify-content: space-between;
}
.question__title {
    padding-right: 2.5rem;
}
.question__desc {
    padding-right: 3.75rem;
}

.line {
    width: 100%;
    height: 1px;
    background-color: $border;
    margin-bottom: 20px;
}


@media (max-width: 600px) {
    .container {
        padding: 0 4vw;
    }
    .question__title {
        padding-right: 1.5rem;
    }
    .question__desc {
        padding-right: 1rem;
    }
}
</style>