<template>
    <div class="content">
        <div>
            <Header />
            <div class="container">
                <div class="card">
                    <div class="card__text" v-for="(course, index) in currentCourse">
                        <div class="card__content">
                        <button class="button-back" @click="goBack">
                            <svg class="button-back__arrow" width="30px" height="30px" viewBox="0 0 24 24" fill="none">
                                <path d="M14.2893 5.70708C13.8988 5.31655 13.2657 5.31655 12.8751 5.70708L7.98768 10.5993C7.20729 11.3805 7.2076 12.6463 7.98837 13.427L12.8787 18.3174C13.2693 18.7079 13.9024 18.7079 14.293 18.3174C14.6835 17.9269 14.6835 17.2937 14.293 16.9032L10.1073 12.7175C9.71678 12.327 9.71678 11.6939 10.1073 11.3033L14.2893 7.12129C14.6799 6.73077 14.6799 6.0976 14.2893 5.70708Z"/>
                            </svg>
                            <p class="button-back__text fw-bold">Назад</p>
                        </button>
                        <h1 class="fs-20">{{course.name}}</h1>
                        <h1 class="grey-text fw-medium">{{course.description}}</h1>
                        <div class="card__desc">
                            <p class="fw-bold">Включает в себя :</p>
                            <p class="grey-text fw-medium main-blue">{{ course.question_count }} вопросов</p>
                        </div>
                        <!-- <div class="card__desc">
                            <p class="fw-bold">Примерное время прохождения :</p>
                            <p class="grey-text fw-medium main-blue">2 недели</p>
                        </div> -->
                        <div class="card__list">
                            <p class="fw-bold">Содержание курса:</p>
                            <div class="card__list">
                                <p v-for="c in course['titles']" class="grey-text">· {{ c }}</p>
                            </div>
                        </div>
                        </div>
                    </div>
                    <div v-if="aisStore.showCourseInfoButton" class="button-position">
                        <button class="button" @click="startCourse">Начать</button>
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

import { computed} from 'vue'
import { useRouter } from 'vue-router'
import { useStore, UserCourse } from "../store"

const router = useRouter();
const aisStore = useStore()

function goBack() {
    if (!aisStore.showCourseInfoButton) {
        return router.push('/course')
    } else {
        return router.push('/courses')
    }
}
function startCourse(id) {

    if (aisStore.showCourseInfoButton) {
        const c: UserCourse = {
            "course": aisStore.selectedCourse[0].id
        }
        aisStore.startCourse(aisStore.selectedCourse[0].id, c)
        aisStore.getUserCourses()
    }

    return router.push('/course')
}

const currentCourse = computed(() => {
    return aisStore.selectedCourse
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

.card {
    width: 100%;
    flex-direction: column;
    display: flex;
    border: 1px solid $border;
    border-radius: 0.625rem;
    padding: 1rem;
    gap: 1.25rem;
}
.card__content {
    display: flex;
    flex-direction: column;
    gap: 0.875rem;
    max-width: 1000px;
}
.card__desc {
    display: flex;
    gap: 0.625rem;
    flex-wrap: wrap;
}
.card__list {
    display: flex;
    flex-direction: column;
    gap: 10px;
}
.card__text {
    display: flex;
    justify-content: space-between;
}

.star {
    cursor: pointer;
    stroke: $yellow;
    transition: .2s;

    &:hover {
        opacity: 0.8;
        fill: $yellow;
        transition: .2s;
    }
}
.star--filled {
    fill: $yellow;
}

.button {
    max-width: 300px;
    padding: 0 80px;
    background-color: $main-blue;
    height: 3rem;
    color: white;
}
.button-position {
    margin: 0 auto;
}

@media (max-width: 600px) {
    * {
        transition: .2s;
    }
    .container {
        padding: 0 4vw;
    }
}

</style>