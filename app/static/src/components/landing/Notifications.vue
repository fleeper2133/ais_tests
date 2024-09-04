<script setup>
import { reactive } from "vue";
import Header from './components/Header.vue';
import Footer from './components/Footer.vue';
</script>

<template>
  <Header />
  <div class="container">
    <div class="bgc-notif">
      <div class="d-flex">
        <div class="notif__title">
          <p>Оплата прошла успешно</p>
        </div>
        <div class="" style="margin-left: 0.5rem;">
          <img class=""style="width: 20px;" src="../../assets/images/landing/coool.svg" alt="" />
        </div>
      </div>
      <div class="notif__text">
        <p>Вам доступен курс обучения по <span>“A.1 Основы промышленной безопасности”</span></p>
      </div>
      <div class="d-flex justify-content-between notif__end">
        <div class="notif__text__next">
          <p>Для прохождения нажмите на кнопку справа</p>
        </div>
        <div class="notif__text__butt">
          <a href="">Начать обучение</a>
        </div>
      </div>
    </div>
    
    <div class="bgc-notif">
      <div class="d-flex">
        <div class="notif__title__error">
          <p>Оплата не прошла</p>
        </div>
        <div class="" style="margin-left: 0.5rem;">
          <img class=""style="width: 20px;" src="../../assets/images/landing/error.svg" alt="" />
        </div>
      </div>
      <div class="notif__text">
        <p style="font-weight: 600;">“A.1 Основы промышленной безопасности”</p>
      </div>
      <div class="d-flex justify-content-between notif__end">
        <div class="notif__text__next">
          <p>Для повторной оплаты нажмите на кнопку справа</p>
        </div>
        <div class="notif__text__butt__erorr">
          <a href="">Оплатить повторно</a>
        </div>
      </div>
    </div>
  </div>
  <Footer />
</template>

<style scoped lang="scss">
@import '../../sass/styles.scss';

.notif__end {
  @media screen and (max-width: 430px) {
     flex-direction: column;
    }
}
.notif__text__butt__erorr {
  border-radius: 10px;
  padding: 0.5rem 1rem 0.5rem 1rem;
  background: rgb(255, 78, 84);
  a {
    color: rgb(255, 255, 255);
    font-size: 1rem;
    font-weight: 400;
    text-decoration: none;
    @media screen and (max-width: 430px) {
     display: flex;
     justify-content: center;
    }
  }
  a:hover {
      color: rgb(197, 197, 197);
    }
}
.notif__text__butt {
  border-radius: 10px;
  padding: 0.5rem 1rem 0.5rem 1rem;
  background: rgb(115, 54, 254);
  a {
    color: rgb(255, 255, 255);
    font-size: 1rem;
    font-weight: 400;
    text-decoration: none;
    @media screen and (max-width: 430px) {
     display: flex;
     justify-content: center;
    }
  }
  a:hover {
      color: rgb(37, 42, 193);
    }
}
.notif__text {
  p {
    color: rgb(0, 0, 0);
    font-size: 1rem;
    font-weight: 400;
  }
  span {
    color: rgb(0, 0, 0);
    font-size: 1rem;
    font-weight: 600;
  }
}
.notif__title {
  p {
    color: rgb(0, 0, 0);
    font-size: 1.2rem;
    font-weight: 600;
  }

}
.notif__title__error {
  p {
    color: rgb(0, 0, 0);
    font-size: 1.2rem;
    font-weight: 600;
  }

}
.notif__text__next {
    p {
      color: rgb(8, 106, 217);
      font-size: 1rem;
      font-weight: 400;

    }
  }
.bgc-notif {
  box-sizing: border-box;
  border: 3px solid rgb(125, 177, 255);
  border-radius: 5px;
  padding: 1rem;
  background: rgb(255, 255, 255);
  margin-bottom: 2rem;
}
</style>