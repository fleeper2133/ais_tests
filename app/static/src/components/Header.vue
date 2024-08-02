<template>
    <div class="header">
        <img class="logo" src="../assets/images/logo.png" alt="logo">
        <div class="header__content">
            <div class="header__email">
                <p class="fw-bold">Здравствуйте</p>
                <p class="fs-14 grey-text">{{ email }}</p>
            </div>
            <div class="header__icon">
                <svg class="header__png" width="24px" height="24px" viewBox="0 0 24 24" fill="none">
                    <path d="M5 21C5 17.134 8.13401 14 12 14C15.866 14 19 17.134 19 21M16 7C16 9.20914 14.2091 11 12 11C9.79086 11 8 9.20914 8 7C8 4.79086 9.79086 3 12 3C14.2091 3 16 4.79086 16 7Z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </div>
            <div class="exit" @mouseover="showText = true" @mouseleave="showText = false" @click="exit">
                <svg class="exit-button" width="30px" height="30px" viewBox="0 0 16 16" fill="none">
                    <g>
                    <path d="M1 8a6 6 0 018.514-5.45.75.75 0 01-.629 1.363 4.5 4.5 0 100 8.175.75.75 0 11.63 1.361A6 6 0 011 8z"/>
                    <path d="M11.245 4.695a.75.75 0 00-.05 1.06l1.36 1.495H6.75a.75.75 0 000 1.5h5.805l-1.36 1.495a.75.75 0 001.11 1.01l2.5-2.75a.748.748 0 00-.002-1.012l-2.498-2.748a.75.75 0 00-1.06-.05z"/>
                    </g>
                </svg>
                <transition name="fade">
                    <div class="exit-text" v-if="showText">Выйти</div>
                </transition>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref} from "vue";
import { jwtDecode } from "jwt-decode";
import { useStore } from "../store"
import { useRouter } from 'vue-router'

const router = useRouter()
const aisStore = useStore()

const showText = ref(false)

const email = computed(() => {
    const accessToken = localStorage.getItem('accessToken')
    if(accessToken){
      const payload = jwtDecode(accessToken);
      return payload.email;
    }
})

function exit() {
    aisStore.currentUser = {}
    router.push('/')
}

</script>

<style lang="scss" scoped>

@import '../sass/main.scss';

.logo {
  cursor: pointer;
}

.exit {
    cursor: pointer;
    display: flex;
    gap: 6px;
    align-items: center;
    // background-color: #e3e8f0;
    border-radius: 10px;
    padding: 6px 10px;
    transition: .2s;
}
.exit-button {
    fill: #7DB1FF;
    transition: .2s;
}
.exit-text {
    color: #7DB1FF;
    transition: .2s;
}

.fade-enter-active, .fade-leave-active {
    transition: opacity 0.3s;
}
.fade-enter, .fade-leave-to {
    opacity: 0;
}

.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.25rem 20vw;
}
.header__content {
    display: flex;
    gap: 20px;
    align-items: center;
}
.header__email {
    display: flex;
    flex-direction: column;
    gap: 4px;
    align-items: end;
}
.header__icon {
    display: flex;
    justify-content: center;
    align-items: center;

    width: 3.125rem;
    height: 3.125rem;
    border-radius: 100%;
    background-color: #E0ECFF;
    border: 2px solid #aaccff;
}
.header__png {
    stroke: #7DB1FF;
}

@media (max-width: 600px) {
    .header {
      padding: 1.25rem 4vw;
    }
}
</style>
