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
                    <div class="fs-18 fw-bold">Частые ошибки</div>
                </div>
            </div>
            <div class="container">
                <div class="history-list">

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
import { useRouter } from 'vue-router';

const router = useRouter();

function goBack() {
    router.push('/course')
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
</style>