<template>
  <div v-if="aisStore.isQuestionComplanePopupVisible" class="complaint-popup">
    <div class="complaint-content">
      <div class="complaint-content__header">
        <h1 class="fw-bold fs-20">Жалоба на вопрос</h1>
        <svg class="complaint-content__exit-icon" @click="aisStore.isQuestionComplanePopupVisible = false, showError = false" width="30px" height="30px" viewBox="0 0 24 24" fill="none">
        <circle cx="12" cy="12" r="10" stroke="#1C274C" stroke-width="1.5"/>
        <path d="M14.5 9.50002L9.5 14.5M9.49998 9.5L14.5 14.5" stroke="#1C274C" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
      </div>
      <div class="question-text">
        <p class="question-text__id grey-text">ID вопроса: {{ aisStore.questionDataForComplane['id'] }}</p>
        <p class="question-text__desc">{{ aisStore.questionDataForComplane['question_text'] }}</p>
      </div>
      <div class="complaint-content__textarea">
        <span class="color-grey fw-bold fs-14">Текст вашей жалобы</span>
        <p v-if="showError" class="complaint-content__textarea-error fw-bold">Введите текст!</p>
        <textarea class="textarea" :style="`background-color: ${showError ? '#e4c1c5' : '#dee3e7'}`" v-model="complaneText" maxlength="1000"></textarea>
      </div>
      <button class="button" @click="sendQuestionComplane(aisStore.questionDataForComplane['id'])">Отправить</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useStore } from "../store"

const aisStore = useStore()

const showError = ref(false)
const complaneText = ref('')
function sendQuestionComplane(id) {

  if (complaneText.value.length > 0) {
    const toSend = {
      "message": complaneText.value,
      "user": aisStore.currentUser['id'],
      "question": id
    }
    aisStore.issueСomplain(toSend)
    aisStore.isQuestionComplanePopupVisible = false
    complaneText.value = ''
  } else showError.value = true
}

</script>

<style lang="scss" scoped>
@import '../sass/main.scss';

.complaint-popup {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;

  @media (max-width: 1440px) {
    padding: 0 10vw;
  }
  @media (max-width: 600px) {
    padding: 0 2vw;
  }
}

.complaint-content {
  width: 1000px;
  background: white;
  padding: 40px;
  border-radius: 8px;
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.complaint-content__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.complaint-content__exit-icon {
  cursor: pointer;

  &:hover {
    scale: 1.2;
  }
}
.question-text {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.question-text__id {
  text-align: start;
  font-weight: bold;
  font-size: 14px;
}
.question-text__desc {
  text-align: start;
}
.complaint-content__textarea {
  display: flex;
  flex-direction: column;
  align-items: start;
  gap: 10px;
}
.complaint-content__textarea-error {
  color: #ff4a71;
  font-size: 14px;
}
.textarea {
  width: 100%;
  height: 200px;
  padding: 20px;
  resize: none;
}
</style>