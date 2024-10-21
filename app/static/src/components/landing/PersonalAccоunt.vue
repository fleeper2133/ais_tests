<script setup>
import { reactive } from "vue";
import Header from './components/Header.vue';
import Footer from './components/Footer.vue';


</script>

<template>
  <Header />

  
  <div class="container">
    <div class="row">
        <div class="col-lg-2 col-md-3">
            <div class="lk_bid">
                <a href="/application">Подать заявку</a>
            </div>
        </div>
    </div>
    <div class="row" style="padding: 0 1rem 0 1rem">
        <div class="col-md-2 d-none d-md-block">
            <p >ФИО</p>
        </div>
        <div class="col-md-3 d-none d-md-block">
            <p>Выбранные курсы</p>
        </div>
        <div class="col-md-3 d-none d-md-block">
            <p>Период обучения</p>
        </div>
        <div class="col-md-2 d-none d-md-block">
            <p>Пулл вопросов</p>
        </div>
        <div class="col-md-2 p-0 d-none d-md-block">
            <p>Статус оплаты</p>
        </div>
    </div>
    <div class="lk__bgc">
        <div class="row">
        <div class="col-md-2 d-flex">
            <p>Иванов Иван Иавнович <span style="color: rgb(8, 106, 217);">#567</span></p>
        </div>
        <div class="col-md-3 lk__cours">
            <p>A.1 Основы промышленной безопасности</p>
        </div>
        <div class="col-md-2 lk__data">
            <p>c 12.12.24 до 12.01.24</p>
        </div>
        <div class="col-md-3">
            <div class="dropdown">
  <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false">
    1232 вопросов
  </button>
  <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
    <li><a class="dropdown-item" href="#">регистрация ОПО в госреестре;</a></li>
    <hr style="margin: 0.5rem 0 0.5rem 0;">
    <li><a class="dropdown-item" href="#">обязанности эксплуатирующих организаций, их ответственность;</a></li>
    <hr style="margin: 0.5rem 0 0.5rem 0;">
    <li><a class="dropdown-item" href="#">система управления промышленной безопасностью и производственный контроль;</a></li>
  </ul>
</div>
        </div>
        <div class="col-md-2">
            <div class="lk__status">
                <p>Оплачен</p>
            </div>
        </div>
        </div>
    </div>
    <div class="lk__bgc">
        <div class="row">
        <div class="col-md-2 d-flex">
            <p>Иванов Иван Иавнович <span style="color: rgb(8, 106, 217);">#567</span></p>
        </div>
        <div class="col-md-3 lk__cours">
            <p>A.1 Основы промышленной безопасности</p>
        </div>
        <div class="col-md-2 lk__data">
            <p>c 12.12.24 до 12.01.24</p>
        </div>
        <div class="col-md-3">
            <div class="dropdown">
  <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false">
    1232 вопросов
  </button>
  <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
    <li><a class="dropdown-item" href="#">регистрация ОПО в госреестре;</a></li>
    <hr style="margin: 0.5rem 0 0.5rem 0;">
    <li><a class="dropdown-item" href="#">обязанности эксплуатирующих организаций, их ответственность;</a></li>
    <hr style="margin: 0.5rem 0 0.5rem 0;">
    <li><a class="dropdown-item" href="#">система управления промышленной безопасностью и производственный контроль;</a></li>
  </ul>
</div>
        </div>
        <div class="col-md-2">
            <div class="lk__status__non">
                <p>Не оплачен</p>
            </div>
        </div>
        </div>
    </div>
  </div>
  
  <Footer />
</template>

<style scoped lang="scss">
@import '../../sass/styles.scss';
.lk__cours {
    @media screen and (max-width: 430px) {
    margin-top: 1rem;
    }
}
.lk__data {
    @media screen and (max-width: 430px) {
    margin-bottom: 1rem;
    margin-top: 1rem;
    }
}
.btn-secondary {
    padding: 0;
    background-color: #fff;
    border: 0;
    color: black;
    padding-top: 0;
    @media screen and (max-width: 430px) {
    margin-bottom: 1rem;
    }
}
.btn:hover {
    color: rgb(0, 0, 0);
    background-color: rgb(255, 255, 255);
    border-color: none;
}
.dropdown-menu {
    box-sizing: border-box;
    border: 2px solid rgb(125, 177, 255);
    border-radius: 10px;
    box-shadow: 0px 0px 5.3px 0px rgba(0, 0, 0, 0.25);
    background: rgb(255, 255, 255);
    a {
        color: rgb(0, 0, 0);
        font-size: 0.8rem;
        font-weight: 400;
    }
    
}
.lk__status__non {
    border-radius: 5px;
    padding: 0.5rem;
    background: rgba(234, 173, 173, 1);
    width: 70%;
    margin-bottom: 2rem;
    @media screen and (max-width: 768px) {
      width: 100%;
    }
    p {
        display: flex;
        justify-content: center;
        margin: 0;
    }
}
.lk__status {
    border-radius: 5px;
    padding: 0.5rem;
    background: rgb(173, 234, 190);
    width: 70%;
    margin-bottom: 2rem;
    @media screen and (max-width: 768px) {
      width: 100%;
    }
    p {
        display: flex;
        justify-content: center;
        margin: 0;
    }
}
.lk__bgc {
    box-sizing: border-box;
    border: 3px solid rgb(125, 177, 255);
    border-radius: 5px;
    background: rgb(255, 255, 255);
    padding: 1rem;
    margin-bottom: 2rem;
    p {
        margin: 0;
    }
}

.lk_bid {
    border-radius: 10px;
    padding: 0.5rem;
    box-shadow: 0px 0px 5.3px 0px rgba(99, 99, 99, 0.25);
    background: rgb(255, 255, 255);
    margin-bottom: 2rem;
    a {
        display: flex;
        justify-content: center;
        color: rgb(8, 106, 217);
        font-size: 1rem;
        font-weight: 500;
        text-decoration: none;
    }
    :hover {
        color: rgb(54, 57, 60) ;
    }
}
</style>