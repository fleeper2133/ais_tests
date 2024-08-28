<template>
    <div class="content">
        <div class="container container-space">
            <div class="general general--margin">
                <div class="general__info">
                    <div class="logo">
                        <img src="../assets/images/logo.png" alt="logo">
                        <p class="logo__text fs-14">Автоматизированная информационная система по подготовке к экзамену по профессиональной квалификации</p>
                    </div>
                    <div class="general__info-text">
                        <h1 class="title">Система подготовки специалистов к сдаче экзамена</h1>
                        <div class="paragraphs">
                            <h2 class="fw-medium">• По промышленной безопасности</h2>
                            <h2 class="fw-medium">• По промышленной безопасности</h2>
                            <h2 class="fw-medium">• По промышленной безопасности</h2>
                        </div>
                    </div>
                    <img class="auth-img" src="../assets/images/auth-img.png" alt="auth-img">
                </div>
                <div class="login-panel" @submit.prevent>
                    <div class="greeting">
                        <p class="fs-20 fw-bold">Добро пожаловать в </p>
                        <img src="../assets/images/logo.png" alt="logo">
                    </div>
                    <form class="form" @submit.prevent="login">
                        <div class="form__input">
                            <p class="fw-bold">Логин</p>
                            <input class="input" v-model="email" type="login" placeholder="Введите электронную почту..">
                        </div>
                        <div class="form__input">
                            <p class="fw-bold">Пароль</p>
                            <input class="input" v-model="password" type="password" placeholder="Введите пароль..">
                        </div>
                        <div class="buttons">
                            <button class="button button__enter" type="submit">Войти</button>
                            <router-link to="/courses">
                                <button class="button button__demo">Запустить демо</button>
                            </router-link>
                        </div>
                    </form>
                </div>
            </div>
            <div class="app-links">
                <a class="app-link">
                    <svg width="56" height="56" viewBox="0 0 50 50" fill="none">
                        <path d="M25 50C38.8071 50 50 38.8071 50 25C50 11.1929 38.8071 0 25 0C11.1929 0 0 11.1929 0 25C0 38.8071 11.1929 50 25 50Z" fill="url(#paint0_linear_82_28)"/>
                        <path d="M29.3694 11.8822C29.9098 10.9391 29.5867 9.73441 28.648 9.19157C27.7092 8.64874 26.5101 8.97327 25.9698 9.91641L25.0275 11.5615L24.085 9.91641C23.5446 8.97327 22.3455 8.64874 21.4067 9.19157C20.468 9.73441 20.145 10.9391 20.6853 11.8822L22.7644 15.5115L16.188 26.9909H10.89C9.8068 26.9909 8.92871 27.8731 8.92871 28.9613C8.92871 30.0495 9.8068 30.9316 10.89 30.9316H29.3437C29.5055 30.5045 29.6759 29.7716 29.4946 29.0981C29.2223 28.0856 28.2144 26.9909 26.5255 26.9909H20.7139L29.3694 11.8822Z" fill="white"/>
                        <path d="M17.2083 33.1105C16.8736 32.7371 16.124 32.1405 15.4665 31.9443C14.4642 31.6448 13.7042 31.8327 13.3208 31.9962L11.8599 34.5464C11.3196 35.4894 11.6426 36.6941 12.5814 37.2369C13.5202 37.7798 14.7192 37.4553 15.2595 36.5121L17.2083 33.1105Z" fill="white"/>
                        <path d="M36.1242 30.9316H39.1103C40.1935 30.9316 41.0715 30.0495 41.0715 28.9613C41.0715 27.873 40.1935 26.9909 39.1103 26.9909H33.8667L27.9599 16.6805C27.5212 17.0995 26.6799 18.1696 26.5528 19.383C26.3894 20.9429 26.6344 22.2564 27.3699 23.5427C29.8426 27.8671 32.3192 32.1896 34.7955 36.5121C35.3358 37.4554 36.5348 37.7798 37.4737 37.237C38.4124 36.6941 38.7355 35.4895 38.1951 34.5464L36.1242 30.9316Z" fill="white"/>
                        <defs>
                        <linearGradient id="paint0_linear_82_28" x1="25" y1="0" x2="25" y2="50" gradientUnits="userSpaceOnUse">
                        <stop stop-color="#2AC9FA"/>
                        <stop offset="1" stop-color="#1F65EB"/>
                        </linearGradient>
                        </defs>
                    </svg>
                    <div class="app-link__text">
                        <p>Скоро в</p>
                        <p class="fw-bold">App store</p>
                    </div>
                    <img class="store-qr" src="../assets/images/app-store.png" alt="app-store">
                </a>
                <a class="app-link">
                    <svg width="56" height="56" viewBox="0 0 50 50" fill="none">
                        <path d="M25 50C38.8063 50 50 38.8063 50 25C50 11.1917 38.8063 0 25 0C11.1938 0 0 11.1917 0 25C0 38.8063 11.1938 50 25 50Z" fill="white"/>
                        <path d="M35.048 30.0459L41.6105 26.4063C42.3522 25.9959 43.1293 24.948 41.6105 24.1084L35.0439 20.4792L30.3418 25.2772L35.048 30.0459Z" fill="#FFE300"/>
                        <path d="M30.3414 25.2771L15.3081 40.625C15.6477 40.6667 16.056 40.5771 16.5248 40.3167L35.0456 30.0459L30.3414 25.2792V25.2771Z" fill="#FF4E54"/>
                        <path d="M30.3438 25.2771L35.0438 20.4792L16.5251 10.2459C16.1549 10.0277 15.7178 9.95219 15.2959 10.0334L30.3438 25.2771Z" fill="#00F085"/>
                        <path d="M30.3436 25.2772L15.2957 10.0334C14.6748 10.1751 14.1665 10.7209 14.1665 11.8147V38.7939C14.1665 39.8251 14.5665 40.5501 15.3082 40.623L30.3436 25.2772Z" fill="#00E0FF"/>
                    </svg>
                    <div class="app-link__text">
                        <p>Скоро в</p>
                        <p class="fw-bold">Goggle Play</p>
                    </div>
                    <img class="store-qr" src="../assets/images/play-market.png" alt="play-market">
                </a>
            </div>
        </div>
        <Footer />
    </div>
</template>

<script setup lang="ts">
import Footer from './Footer.vue';
import { Login, Registration, useStore } from "../store";
import { computed, ref, onMounted } from "vue";


const aisStore = useStore()

const email = ref('');
const password = ref('');

function login() {
    const data: Login = {
        "email": email.value,
        "password": password.value,
    }
    // debugger;
    aisStore.login(data);
}

</script>

<style lang="scss" scoped>
@import '../sass/main.scss';

.content {
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.logo__text {
    color: $main-blue;
    max-width: 420px;
}

.general {
    display: flex;
    justify-content: center;
    height: 100%;
    gap: 7rem;
}
.general--margin {
    margin-top: 2vh;
}
.general__info {
    display: flex;
    flex-direction: column;
    gap: 50px;
}
.general__info-text {
    display: flex;
    flex-direction: column;
    gap: 20px;
}
.title {
    font-size: 24px;
    max-width: 420px;
}
.paragraphs {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

// login
.login-panel {
    display: flex;
    flex-direction: column;
    gap: 30px;
    justify-content: center;
}
.greeting {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
}

.auth-img {
    width: 18.75rem;
    height: 18.75rem;
}

.form {
    width: 20rem;
    display: flex;
    flex-direction: column;
    gap: 20px;
}
.form__input {
    display: flex;
    flex-direction: column;
    gap: 10px;
}
.buttons {
    display: flex;
    flex-direction: column;
    gap: 0.625rem;
}
.button__enter {
    color: white;
    background-color: #9668FF;
}
.button__demo {
    color: white;
    background-color: #338DF4;
}

.app-links {
    flex-wrap: wrap;
    justify-content: center;
    display: flex;
    gap: 1.25rem;
}
.app-link {
    width: 300px;
    cursor: pointer;
    background-color: #ebf3ff;
    padding: 1rem;
    justify-content: center;
    display: flex;
    align-items: center;
    gap: 1.25rem;
}
.app-link__text {
    display: flex;
    flex-direction: column;
    gap: 4px;
}
.store-qr {
    width: 3.5rem;
    height: 3.5rem;
}

.input {
    width: 100%;
    height: 3.75rem;
    border: 1px solid $border;
    border-radius: 0.25rem;
    padding-left: 1.25rem;
}

@media (max-width: 1024px) {
    .general {
        flex-wrap: wrap;
        gap: 4rem;
        height: auto;
    }
    .general__info {
        align-items: center;
    }
    .title {
        text-align: center;
    }
    .general__info-text {
        align-items: center;
    }
    .logo {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 6px;
        
        &__text {
            text-align: center
        }
    }
    .auth-img {
        display: none;
    }
    .app-links {
        margin-top: 40px;
    }
}
</style>