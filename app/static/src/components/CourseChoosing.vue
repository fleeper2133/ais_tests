<template>
    <div class="content">
        <div>
            <Header />
            <div class="content__gap">
                <div class="container container__graph">
                    <div class="graph">
                        <div class="graph__title fs-18">Ударный режим</div>
                        <div class="graph__info">
                            <div class="graph__info-item">
                                <p class="fs-14 grey-text">Ваш ударный режим:</p>
                                <p class="fw-bold fs-14">3 дня</p>
                            </div>
                            <div class="graph__info-item">
                                <p class="fs-14 grey-text">Вы выполнили:</p>
                                <p class="fw-bold fs-14">5 заданий</p>
                            </div>
                        </div>
                        <div class="graph__days">
                            <div class="graph__day" v-for="(day, index) in days" :key="index">
                                <div class="graph__day-icon" :class="{ 'graph__day-icon--filed': aisStore.weekActivityData[day] }">
                                    <svg width="20px" height="20px" viewBox="0 0 24 24" fill="none">
                                        <path d="M4 12.6111L8.92308 17.5L20 6.5" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                    </svg>
                                </div>
                                <p class="fs-14">{{ translatedDays[index] }}</p>
                            </div>
                        </div>
                    </div>
                    <div class="last-course">
                        <p>Последний курс:</p>
                        <p class="fs-18">{{ truncatedCourseName }}</p>
                        <div class="info-text">
                            <div class="info-text__stats">
                                <p class="main-blue">Вопросов:</p>
                                <p class="main-blue fw-bold">{{ showQuestions }}</p>
                            </div>
                            <div class="info-text__stats">
                                <p class="main-blue">Прогресс:</p>
                                <p class="main-blue fw-bold">{{ showLastCourseProgress }}%</p>
                            </div>
                        </div>
                        <div class="progress">
                            <div class="progress__inner"></div>
                        </div>
                        <button class="button last-course__button" @click="goToCourse">Продолжить</button>
                    </div>
                </div>
                <div class="container container__bg">
                    <div class="tabs">
                        <div class="tabs__item" v-for="(status, statusIndex) in aisStore.courseStatuses" @click="showCourseStatus = status.id">
                            <p
                                class=" fs-18"
                                :class="{'fw-bold' : showCourseStatus === status.id}"
                            >
                                {{ status.name }}
                            </p>
                            <div v-if="showCourseStatus === status.id" class="tabs__selected"></div>
                        </div>
                    </div>
                </div>
                <div class="container container__courses">
                    <div 
                        class="search" 
                        :style="`border: ${condition};`" 
                        @click.stop="makeFocus"
                    >
                        <input class="search__input" type="text" ref="searchInput" placeholder="Введите название курса.." v-model="inputText">
                        <svg v-if="inputText.length === 0" class="svg-icon magnifier" viewBox="0 0 24 24" fill="none">
                            <path d="M15.7955 15.8111L21 21M18 10.5C18 14.6421 14.6421 18 10.5 18C6.35786 18 3 14.6421 3 10.5C3 6.35786 6.35786 3 10.5 3C14.6421 3 18 6.35786 18 10.5Z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                        <svg v-else class="svg-icon clear" viewBox="0 0 1024 1024" @click="clearSearch()">
                            <path fill="#000000" d="M195.2 195.2a64 64 0 0 1 90.496 0L512 421.504 738.304 195.2a64 64 0 0 1 90.496 90.496L602.496 512 828.8 738.304a64 64 0 0 1-90.496 90.496L512 602.496 285.696 828.8a64 64 0 0 1-90.496-90.496L421.504 512 195.2 285.696a64 64 0 0 1 0-90.496z"/>
                        </svg>
                    </div>
                    <div v-if="paginatedItems.length > 0" class="courses">
                        <div v-for="(course, index) in selectedTasks" :key="course.id" class="course">
                            <div class="course__icon">
                                <svg width="78" height="76" viewBox="0 0 78 76" fill="none">
                                    <path d="M0 37.6746C0 27.7028 4.10892 18.1395 11.4228 11.0884C18.7368 4.03726 28.6566 0.0759888 39 0.0759888C49.3434 0.0759888 59.2632 4.03726 66.5772 11.0884C73.8911 18.1395 78 27.7028 78 37.6746C78 47.6463 73.8911 57.2097 66.5772 64.2608C59.2632 71.3119 49.3434 75.2731 39 75.2731C28.6566 75.2731 18.7368 71.3119 11.4228 64.2608C4.10892 57.2097 0 47.6463 0 37.6746ZM36.5625 9.14488C36.5625 7.14273 34.6234 5.76478 33.0201 6.96397C31.0023 8.47316 29.0718 10.7677 27.3634 13.8559C27.1675 14.2134 26.9777 14.5739 26.7939 14.9371C25.8526 16.7983 27.2928 18.8753 29.3785 18.8753H33.5625C35.2194 18.8753 36.5625 17.5321 36.5625 15.8753V9.14488ZM17.761 18.8753C19.0598 18.8753 20.2011 18.0355 20.666 16.8228C21.3462 15.0486 22.1453 13.318 23.0588 11.6422V11.6422C23.7585 10.3775 22.4892 8.84254 21.2436 9.57584C18.9137 10.9474 16.7627 12.5822 14.8362 14.4447C13.0761 16.1465 14.4174 18.8753 16.8657 18.8753H17.761ZM14.2061 35.3246C15.8215 35.3246 17.1393 34.0444 17.268 32.4341C17.4086 30.6742 17.619 28.9514 17.8942 27.2746C18.2066 25.3707 16.7805 23.5751 14.8512 23.5751H10.0295C8.88554 23.5751 7.82988 24.2211 7.38572 25.2752C6.45618 27.4814 5.77835 29.7771 5.36329 32.1217C5.05934 33.8387 6.44827 35.3246 8.19199 35.3246H14.2061ZM25.974 23.5751C24.5962 23.5751 23.3872 24.512 23.1098 25.8616C22.6775 27.9651 22.365 30.0895 22.1736 32.2255C22.0221 33.9162 23.3894 35.3246 25.0868 35.3246H33.5625C35.2194 35.3246 36.5625 33.9815 36.5625 32.3246V26.5751C36.5625 24.9182 35.2194 23.5751 33.5625 23.5751H25.974ZM44.4375 23.5751C42.7806 23.5751 41.4375 24.9182 41.4375 26.5751V32.3246C41.4375 33.9815 42.7806 35.3246 44.4375 35.3246H52.9095C54.6065 35.3246 55.9736 33.917 55.8229 32.2267C55.6324 30.0908 55.3208 27.9663 54.8894 25.8628C54.6125 24.5127 53.4032 23.5751 52.025 23.5751H44.4375ZM25.0905 40.0245C23.3935 40.0245 22.0264 41.4321 22.1771 43.1224C22.3676 45.2584 22.6792 47.3828 23.1106 49.4863C23.3875 50.8364 24.5968 51.774 25.975 51.774H33.5625C35.2194 51.774 36.5625 50.4309 36.5625 48.774V43.0245C36.5625 41.3676 35.2194 40.0245 33.5625 40.0245H25.0905ZM44.4375 40.0245C42.7806 40.0245 41.4375 41.3676 41.4375 43.0245V48.774C41.4375 50.4309 42.7806 51.774 44.4375 51.774H52.0366C53.4095 51.774 54.6158 50.8439 54.8928 49.4992C55.311 47.4691 55.6259 45.3393 55.8228 43.1317C55.9739 41.4378 54.6055 40.0245 52.9049 40.0245H44.4375ZM29.3987 56.4738C27.3074 56.4738 25.8575 58.5649 26.8016 60.4309C26.9845 60.7924 27.1718 61.1465 27.3634 61.4932C29.0699 64.578 30.9999 66.8689 33.0155 68.378C34.6199 69.5793 36.5625 68.2013 36.5625 66.197V59.4738C36.5625 57.817 35.2194 56.4738 33.5625 56.4738H29.3987ZM21.2416 65.7776C22.4899 66.5114 23.7598 64.9739 23.0588 63.7069V63.7069C22.1453 62.0311 21.3462 60.3005 20.666 58.5263C20.2011 57.3136 19.0598 56.4738 17.761 56.4738H16.8565C14.41 56.4738 13.0681 59.1994 14.8257 60.9013C16.7534 62.7679 18.9075 64.4053 21.2416 65.7776ZM14.862 51.774C16.7879 51.774 18.2119 49.9847 17.8981 48.0845C17.6153 46.3725 17.4044 44.65 17.2658 42.9214C17.1364 41.3085 15.8177 40.0245 14.1997 40.0245H8.18735C6.44534 40.0245 5.05659 41.5077 5.35806 43.2234C5.7767 45.606 6.46232 47.9003 7.38436 50.0789C7.82942 51.1304 8.88363 51.774 10.0255 51.774H14.862ZM54.9413 63.7069C54.2402 64.9739 55.5101 66.5114 56.7584 65.7776C59.0925 64.4053 61.2466 62.7679 63.1743 60.9013C64.9319 59.1994 63.59 56.4738 61.1435 56.4738H60.239C58.9402 56.4738 57.7989 57.3136 57.334 58.5263C56.6538 60.3005 55.8547 62.0311 54.9413 63.7069V63.7069ZM44.4375 56.4738C42.7806 56.4738 41.4375 57.817 41.4375 59.4738V66.2042C41.4375 68.2064 43.3766 69.5843 44.9799 68.3851C46.9977 66.8759 48.9282 64.5815 50.6366 61.4932C50.8289 61.1461 51.0168 60.7913 51.2003 60.4288C52.1446 58.5638 50.6944 56.4738 48.6039 56.4738H44.4375ZM60.1019 48.0845C59.7881 49.9846 61.2121 51.774 63.138 51.774H67.9745C69.1164 51.774 70.1706 51.1304 70.6156 50.0789C71.5377 47.9003 72.2233 45.606 72.6419 43.2234C72.9434 41.5077 71.5547 40.0245 69.8127 40.0245H63.8003C62.1823 40.0245 60.8635 41.3085 60.7342 42.9214C60.5956 44.65 60.3847 46.3725 60.1019 48.0845ZM69.808 35.3246C71.5517 35.3246 72.9407 33.8387 72.6367 32.1217C72.2217 29.7771 71.5438 27.4814 70.6143 25.2752C70.1701 24.2211 69.1145 23.5751 67.9705 23.5751H63.1488C61.2195 23.5751 59.7934 25.3707 60.1058 27.2746C60.381 28.9514 60.5914 30.6742 60.732 32.4341C60.8607 34.0444 62.1785 35.3246 63.7939 35.3246H69.808ZM54.9413 11.6422C55.8266 13.2457 56.6277 14.9813 57.3347 16.8322C57.7965 18.0413 58.9355 18.8753 60.2298 18.8753H61.1435C63.59 18.8753 64.9319 16.1497 63.1743 14.4478C61.2466 12.5813 59.0927 10.9439 56.7588 9.57174C55.522 8.84463 54.2458 10.3874 54.9413 11.6422V11.6422ZM48.6215 18.8753C50.7072 18.8753 52.1474 16.7983 51.2061 14.9371C51.0224 14.5739 50.8325 14.2134 50.6366 13.8559C48.9293 10.7696 47.0001 8.47794 44.9837 6.96889C43.3795 5.76826 41.4375 7.14661 41.4375 9.15042V15.8753C41.4375 17.5321 42.7806 18.8753 44.4375 18.8753H48.6215Z" fill="white"/>
                                </svg>
                            </div>
                            <div class="course__content">
                                <div class="course__header">
                                    <div class="course__text">
                                        <p class="fs-18 fw-bold course__title">{{course.name}}</p>
                                        <p class="course__subtitle fs-14">{{course.description}}</p>
                                        <p class="fs-14 grey-text">Версия: {{course.version}}</p>
                                    </div>
                                </div>
                                <div class="course__info">
                                    <div class="info-text">
                                        <div class="info-text__stats">
                                            <p class="main-blue fs-14">Вопросов:</p>
                                            <p class="main-blue fw-bold">{{ course.question_count }}</p>
                                        </div>
                                        <div v-if="aisStore.startedCourses.find(c => c.course === course.id)" class="info-text__stats">
                                            <p class="main-blue fs-14">Прогресс:</p>
                                            <p class="main-blue fw-bold">{{ showProgress(course.id) + '%' }}</p>
                                        </div>
                                    </div>
                                    <button 
                                        :style="{ backgroundColor: whatStatus(course.id) }" 
                                        class="button course__button" @click="goToCourseInfo(course.id)"
                                    >
                                        {{whatTextShow(course.id)}}
                                    </button>
                                </div>
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
import { computed, onMounted, ref, watch, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { useStore, Schedule } from "../store"

import Header from './Header.vue'
import Footer from './Footer.vue'
import Pagination from './Pagination.vue'

const router = useRouter()
const aisStore = useStore()

const days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
const translatedDays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']

function goToCourseInfo(id: number): void {
    const course = aisStore.allCourses.filter(c => c.id === id)
    aisStore.selectedCourse = course
    aisStore.selectedCourseId = aisStore.selectedCourse[0].id
    const whatCourseSelected = aisStore.startedCourses.find(c => c.course === aisStore.selectedCourse[0].id)

    aisStore.showCourseInfoButton = true

    if (whatCourseSelected) {
        router.push('/course')
    } else {
        router.push('/course-info')
    }
}

// Last course
const showLastCourseInfo = computed(() => {
    if (aisStore.allCourses.length === 0) {
        return null
    }
    const course = aisStore.allCourses.find(c => c.id === aisStore.lastCourse['course']);
    return course || null
})
const truncatedCourseName = computed(() => {
    const course = showLastCourseInfo.value
    if (!course || !course.name) {
        return ''
    }
    const courseName = course.name
    if (courseName.length > 50) {
        return courseName.slice(0, 50) + '...'
    }
    return courseName
})
const showQuestions = computed(() => {
    const course = showLastCourseInfo.value
    if (!course || !course.question_count) {
        return 0
    }
    const courseName = course.question_count
    return courseName
})
const showLastCourseProgress = computed(() => {
    const course = showLastCourseInfo.value
    if (!course || !course.id) {
        return ''
    }
    const courseId = course.id
    return showProgress(courseId)
})

function goToCourse() {
    const course = aisStore.startedCourses.filter(c => c.course === aisStore.lastCourse['course'])
    const course2 = aisStore.allCourses.filter(c => c.id === course[0].course)
    goToCourseInfo(course2[0].id)
}
// Last course end

// Search
const inputText = ref('')
function clearSearch() {
    if(this.inputText !== undefined ) {
        return this.inputText = ''
    }
}
const filterSearch = computed(() => {
    if (!inputText.value) {
        return aisStore.allCourses;
    }

    return aisStore.allCourses.filter((question) => {
        return question.name.toLowerCase().includes(inputText.value.toLowerCase());
    });
});
const searchInput = ref<HTMLInputElement | null>(null);
function makeFocus(): void {
    if (searchInput.value) {
        searchInput.value.focus();
    }
}
const condition = computed(() => {
    if (filterSearch.value.length === 0) {
        return '1px solid #ff1d4e'
    }
})
// Search end

// Pagination

const currentPage = ref(1);
const itemsPerPage = 15;
const totalItems = computed(() => filterSearch.value.length);

const paginatedItems = computed(() => 
    filterSearch.value.slice(
        (currentPage.value - 1) * itemsPerPage,
        currentPage.value * itemsPerPage
    )
);

// Pagination end


function showProgress(id: number) {
    const course = aisStore.startedCourses.find(c => c.course === id)
    if (course) {
        return course.progress
    }
}
function whatTextShow(id: number) {
    const course = aisStore.startedCourses.find(c => c.course === id)
    if (course) {
        return 'Продолжить'
    } else {
        return 'Выбрать'
    }
}
const whatStatus = (id: number) => {
    const course = aisStore.startedCourses.find(c => c.course === id);

    if (course && course.status === 'New') {
        return '#0075ff';
    }

    return '#338DF4';
};

// Status

const showCourseStatus = ref('All')
const courses = computed(() => {
  return {
    'All': paginatedItems.value,
    'New': paginatedItems.value.filter(c2 => aisStore.startedCourses.find(c => c.course === c2.id)) // Убрать пагинацию (если меньше 15)
  }
})

const selectedTasks = computed(() => {
  return courses.value[showCourseStatus.value]
})

// Status end



watch(inputText, () => {
  currentPage.value = 1;
});
onMounted(async () => {
    aisStore.getCurrentUser()
    aisStore.getLastCourse()
    await aisStore.getCourses()
    await aisStore.getUserCourses()
});
</script>

<style lang="scss" scoped>

@import '../sass/main.scss';

.container {
  padding: 0 20vw;
}
.content {
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.content__gap {
    display: flex;
    flex-direction: column;
    gap: 30px;
}

.container__bg {
    border-bottom: 1px solid $light-blue;
}
.container__graph {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 20px;
}
.container__courses {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.tabs {
    margin-top: 16px;
    height: 100%;
    display: flex;
    gap: 3rem;
}
.tabs__item {
    display: flex;
    flex-direction: column;
    gap: 10px;
    cursor: pointer;
    transition: .2s;
    height: 100%;

    // &:hover {
    //     transition: .2s;
    //     color: #7DB1FF;
    // }
}
.tabs__text {
    &:hover {
        color: #0075ff;
    }
}
.tabs__text-unselected {
    color: $main-grey;
}
.tabs__selected {
    border-bottom: 2px solid #0075ff;
}

// graph

.graph {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    padding: 20px;
    background-color: #E0F1FF;
    border-radius: 10px;
}
.graph__info {
    display: flex;
    gap: 20px;
    flex-wrap: wrap;
}
.graph__info-item {
    display: flex;
    gap: 6px;
}
.graph__days {
    display: flex;
    gap: 20px;
    flex-wrap: wrap;
}
.graph__day {
    display: flex;
    flex-direction: column;
    gap: 4px;
    align-items: center;
}
.graph__day-icon {
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: white;
    width: 40px;
    height: 40px;
    border-radius: 6px;
}
.graph__day-icon--filed {
    background-color: $main-blue;
}
.graph__day-icon--selected {
    border: 2px solid $main-blue;
}

.last-course {
    display: flex;
    flex-direction: column;
    gap: 10px;
    padding: 20px;
    background-color: #E0F1FF;
    border-radius: 10px;
}
.last-course__button {
    background-color: $main-blue;
    color: white;
}
.progress {
    height: 6px;
    width: 100%;
    background-color: white;
    border-radius: 20px;
}
.progress__inner {
    width: 20%;
    height: 100%;
    background-color: $main-blue;
    border-radius: 20px;
} 

// courses
.courses {
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
}
.course {
    position: relative;
    height: 100%;
    width: 100%;
    display: flex;
    border: 1px solid $border;
    border-radius: 0.625rem;
    padding: 0.625rem;
    gap: 1.875rem;
    align-items: center;
}
.course__icon {
    display: flex;
    width: 200px;
    height: 100%;
    justify-content: center;
    align-items: center;
    background-color: #7DB1FF;
    border-radius: 4px;
}

.course__content {
    display: flex;
    flex-direction: column;
    gap: 10px;
    width: 100%;
}
.course__button {
    max-width: 300px;
    height: 3rem;
    color: white;
}
.course__header {
    display: flex;
    justify-content: space-between;
    gap: 1.875rem;
}
.course__text {
    display: flex;
    flex-direction: column;
    gap: 14px;
    max-width: 90%;
}
.course__subtitle {
    color: $main-grey;
}
.course__info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 10px;
}
.info-text {
    display: flex;
    gap: 1.8rem;
    flex-wrap: wrap;
}
.info-text__stats {
    display: flex;
    align-items: end;
    gap: 0.5rem;
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

.pagination {
    margin-top: 20px;
}

.search {
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


@media (max-width: 360px) {
    .info-text {
        gap: 10px;
    }
}
@media (max-width: 600px) {
    * {
        transition: .2s;
    }
    .container {
        padding: 0 4vw;
    }
}
@media (max-width: 1024px) {
    .tabs {
        flex-wrap: wrap;
    }

    .graph {
        width: 100%;
    }

    .last-course {
        width: 100%;    
    }
    .last-course__button {
        max-width: 300px;
    }

    .course {
        flex-direction: column;
        height: auto;
    }
    .course__icon {
        padding: 20px 0;
        width: 100%;
    }
}


// copied
.fw-bold {
  font-weight: bold;
}
.fw-medium {
  font-weight: medium;
}
.main-blue {
  color: $main-blue !important;
}
.grey-text {
  color: $main-grey;
}

.fs-14 {
  font-size: 14px;
}
.fs-18 {
  font-size: 18px;
}
.fs-20 {
  font-size: 20px;
}
.fs-24 {
  font-size: 24px;
}
// copied
</style>