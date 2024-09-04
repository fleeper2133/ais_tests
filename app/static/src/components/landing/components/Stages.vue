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
                <a class="stages__step__title" href="">Пройти тестрирование</a>
            </div>
            <div>
                <a class="stages__step__text" href="">Пройдите тест чтобы получить точную оценку своихзнаний.</a>
            </div>
        </div>
    </div>
    <div class="col-md-6">
        <div class="stages__step">
            <div class="mb-2">
                <a class="stages__step__title" href="">Все вопросы курса</a>
            </div>
            <div>
                <a class="stages__step__text" href="">Этот блок поможет оценить знания, узнать новое, определить слабые места и предоставить обратную связь для улучшения учебного процесса.</a>
            </div>
        </div>
    </div>
   </div>
   <div class="row">
    <div class="col-md-6">
        <div class="stages__step">
            <div class="mb-2" >
                <a class="stages__step__title" href="">Проверить себя</a>
            </div>
            <div>
                <a class="stages__step__text" href="">Чтобы проверить себя и свои навыки, пройдите этот тест.
                    Он состоит из нескольких вопросов, которые помогут
                    определить ваш уровень подготовки.</a>
            </div>
        </div>
    </div>
    <div class="col-md-6">
        <div class="main-for"style="">
            <a class="stages__step__program" href="">Программа разработана на основании нормативно-правовых актов, нормативных и
                 методических документов, используемых при составлении вопросов тестирования в Ростехнадзоре.</a>
        </div>
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