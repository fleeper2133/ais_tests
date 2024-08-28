<template>
  <router-view></router-view>
  <QuestionComplanePopup />
</template>

<script setup lang="ts">
import QuestionComplanePopup from './QuestionComplanePopup.vue';


import { onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

onMounted(() => {
  if (localStorage.getItem('shouldRedirect') === 'true') {
    localStorage.removeItem('shouldRedirect');
    router.push('/courses');
  }
});
</script>

<style lang="scss">
@import '../sass/main.scss';

</style>
