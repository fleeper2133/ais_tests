<script setup>
import { reactive } from "vue";
</script>


<template>
<div class="container">
    <h3 class="d-flex justify-content-center mb-5">Этапы прохождения курса</h3>
   <div class="row">
    <div class="col-md-6">
        <div class="stages__step">
            <div class="mb-2" >
                <a class="stages__step__title" href="">Режим тестирования</a>
            </div>
            <div>
                <a class="stages__step__text" href="">Здесь вы сможете проверить свои знания и навыки в условиях, максимально приближенных к реальному экзамену. Наш режим тестирования предназначен для того, чтобы помочь вам оценить свою готовность и выявить области, требующие дополнительного внимания.</a>
            </div>
        </div>
    </div>
    <div class="col-md-6">
        <div class="stages__step">
            <div class="mb-2">
                <a class="stages__step__title" href="">Все вопросы курса</a>
            </div>
            <div>
                <a class="stages__step__text" href="">Здесь вы найдете все вопросы, которые используются в режимах обучения и тестирования, вместе с правильными ответами и подробными пояснениями. Этот раздел предназначен для того, чтобы помочь вам глубже понять материал и закрепить свои знания.</a>
            </div>
        </div>
    </div>
   </div>
   <div class="row">
    <div class="col-md-6">
        <div class="stages__step">
            <div class="mb-2" >
                <a class="stages__step__title" href="">Режим обучения</a>
            </div>
            <div>
                <a class="stages__step__text" href="">Здесь вы сможете подготовиться к тестированию и улучшить свои знания и навыки. Наш режим обучения предназначен для того, чтобы помочь вам закрепить материал и повысить уверенность в своих силах.</a>
            </div>
        </div>
    </div>
    <div class="col-md-6">
        <!-- <div class="main-for"style="">
            <a class="stages__step__program" href="">Программа разработана на основании нормативно-правовых актов, нормативных и
                 методических документов, используемых при составлении вопросов тестирования в Ростехнадзоре.</a>
        </div> -->
        <div class="stages__button">
            <a href="">Записаться на подготовку</a>
        </div>
    </div>
   </div>
</div>
</template>

<style scoped lang="scss">
.main-for {
    margin-bottom: 1rem;
    @media screen and (min-width: 1025px) {
    margin-bottom: 2.1rem;
    }
}
.stages__step {
    height: 150px;
    border-radius: 10px;
    padding: 1rem;
    background: rgb(125, 177, 255);
    margin-bottom: 2rem;
    @media screen and (max-width: 768px) {
    height: 200px;
    margin-bottom: 1rem;
    }
    &__title {
        text-decoration: none;
        color: rgb(255, 255, 255);
        font-size: 1.2rem;
        font-weight: 500;
    }
    &__text {
        text-decoration: none;
        color: rgb(255, 255, 255);
        font-size: 1rem;
        font-weight: 400;

    }
    &__program {
        text-decoration: none;
        color: rgb(0, 0, 0);
        font-size: 1rem;
        font-weight: 500;
    }
}
.stages__button {
    a {
        border-radius: 10px;
        padding: 0.5rem;
        background: rgb(115, 54, 254);
        display: flex;
        justify-content: center;
        text-decoration: none;
        color: rgb(255, 255, 255);
        font-size: 1rem;
        font-weight: 500;
    }
    a:hover {
      color: rgb(37, 42, 193);
    }
}

</style>