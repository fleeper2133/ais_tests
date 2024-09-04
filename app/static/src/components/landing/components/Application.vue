<script setup>
import { reactive } from "vue";
</script>

<template>
<div class="container" style="margin-bottom: 10rem;">
    <div class="d-flex justify-content-center">
        <h3 style="margin-top: 5rem; margin-bottom: 2rem;">Форма заявки</h3>
    </div>
    <div class="row ll">
        <div class="col-md-6">
            <div class="app__img">
                <img class="" src="../../../assets/images/landing/serCal.svg" alt="" />
            </div>
        </div>
        <div class="col-md-6 ">
            <div class="app__bgc">
                <div class="app__sert" style="width: 100%;">
                    <input class="app__sert__inp" type="text" placeholder="Введите ФИО">
                    <input class="app__sert__inp" type="text" placeholder="Введите номер телефона">
                    <textarea class="app__sert__inp" name="" id="" rows="1" cols="20" placeholder="Комментарий"></textarea>
                </div>
                <div class="app__button"style="width: 100%;">
                <a href="">Записаться на подготовку</a>
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<style scoped lang="scss">
.app__img {
    @media screen and (max-width: 768px) {
        img {
            width: 100%;
        }
    }
    @media screen and (max-width: 430px) {
        margin-bottom: 2rem;
        img {
            width: 100%;
        }
    }
}
.app__bgc {
    border-radius: 5px;
padding: 3rem 1rem 3rem 1rem;
background: rgb(224, 236, 255);
}
.app__button {
    display: flex;
    justify-content: center;
    margin-top: 1rem;
    a {
        width: 50%;
        border-radius: 10px;
        padding: 0.5rem;
        background: rgb(115, 54, 254);
        display: flex;
        justify-content: center;
        text-decoration: none;
        color: rgb(255, 255, 255);
        font-size: 1rem;
        font-weight: 500;
        @media screen and (max-width: 1025px) {
            width: 100%;
    }
    }
    a:hover {
      color: rgb(37, 42, 193);
    }
}
.app__sert {
    &__inp {
        box-sizing: border-box;
        width: 100%;
        border: 2px solid rgb(224, 236, 255);
        border-radius: 10px;
        background: rgb(255, 255, 255);
        padding: 0.5rem;
        margin-bottom: 1rem;
    }
}
</style>