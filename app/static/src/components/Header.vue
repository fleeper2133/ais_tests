<template>
    <div class="header">
        <img src="../assets/images/logo.png" alt="logo">
        <router-link to="/">
            <div class="header__icon">
                <svg class="header__png" width="24px" height="24px" viewBox="0 0 24 24" fill="none">
                    <path d="M5 21C5 17.134 8.13401 14 12 14C15.866 14 19 17.134 19 21M16 7C16 9.20914 14.2091 11 12 11C9.79086 11 8 9.20914 8 7C8 4.79086 9.79086 3 12 3C14.2091 3 16 4.79086 16 7Z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </div>
            <span>{{ email }}</span>
        </router-link>
    </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref} from "vue";
import { jwtDecode } from "jwt-decode";

const email = computed(() => {
    const accessToken = localStorage.getItem('accessToken')
    if(accessToken){
      const payload = jwtDecode(accessToken);
      return payload.email;
    }
})

</script>

<style lang="scss" scoped>

@import '../sass/main.scss';

.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.25rem 10vw;
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
