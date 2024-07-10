<template>
    <div class="content">
        <div>
            <Header />
            <div class="container">
                <router-link to="/course">
                    <button class="button-back">
                        <svg class="button-bac__arrow" width="30px" height="30px" viewBox="0 0 24 24" fill="none">
                            <path d="M14.2893 5.70708C13.8988 5.31655 13.2657 5.31655 12.8751 5.70708L7.98768 10.5993C7.20729 11.3805 7.2076 12.6463 7.98837 13.427L12.8787 18.3174C13.2693 18.7079 13.9024 18.7079 14.293 18.3174C14.6835 17.9269 14.6835 17.2937 14.293 16.9032L10.1073 12.7175C9.71678 12.327 9.71678 11.6939 10.1073 11.3033L14.2893 7.12129C14.6799 6.73077 14.6799 6.0976 14.2893 5.70708Z"/>
                        </svg>
                        <p class="button-back__text fw-bold">Вернуться обратно</p>
                    </button>
                </router-link>
                <div class="tickets tickets--margin">
                    <p class="fw-bold fs-20">Выберите билет</p>
                    <div class="tickets__list">
                        <div v-for="ticket in allTickets" class="ticket">
                            <p class="fw-bold fs-18">{{ticket.name}}</p>
                            <div class="ticket__progress" :style="`background-color: ${chooseBackgroundColor(ticket.status)};`">
                                {{ticket.status}}
                            </div>
                        </div>
                    </div>
                    <div class="button-position">
                        <button disabled class="button tickets__button">Начать</button>
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

import { ref } from 'vue';


const allTickets = [
    {name: 'Билет 1', status: 'Сдан'},
    {name: 'Билет 2', status: 'Не пройден',},
    {name: 'Билет 3', status: 'Не пройден'},
    {name: 'Билет 4', status: 'Не сдан'},
    {name: 'Билет 5', status: 'Сдан'},
    {name: 'Билет 6', status: 'Не пройден'},
]
function chooseBackgroundColor(status) {
    if (status === 'Не пройден') {
        return 'rgb(238, 252, 255)'
    }
    if (status === 'Сдан') {
        return 'rgb(202, 255, 209)'
    }
    if (status === 'Не сдан') {
        return 'rgb(255, 202, 204)'
    }
}

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
  padding: 0 10vw;
  width: 100%;
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
.ticket__progress {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 2.5rem;
    width: 10rem;
    border-radius: 0.375rem;
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