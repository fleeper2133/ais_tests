<template>
    <div v-if="aisStore.isQuestionComplanePopupVisible" class="complaint-popup">
        <div class="complaint-content">
            <h2>Жалоба</h2>
            <input v-model="complaneText" type="text" name="" id="">
            <button @click="sendQuestionComplane">send</button>
            <button @click="aisStore.isQuestionComplanePopupVisible = false">Закрыть</button>
        </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useStore } from "../store"

const aisStore = useStore()

const complaneText = ref('')
// function sendQuestionComplane() {
//     if (currentQuestion.value) {
//         const toSend = {
//             "message": complaneText.value,
//             "user": aisStore.currentUser['id'],
//             "question": currentQuestion.value['id']
//         }  
//         aisStore.issueСomplain(toSend) 
//     }
// }

function sendQuestionComplane() {
        const toSend = {
            "message": complaneText.value,
            "user": aisStore.currentUser['id'],
            "question": 1
        }  
        aisStore.issueСomplain(toSend) 
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
}

.complaint-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
}
</style>