<script setup>
import {reactive} from 'vue';

import { useRouter } from 'vue-router';
const router = useRouter()
</script>

<template>
  <div class="header__bgc">
    <div class="container">
      <div class="row">
        <div class="col-md-3">
          <div class="head__img">
            <a href="/">
              <img class="" src="../../../assets/images/landing/logoAis.svg" alt="" />
            </a>
          </div>
        </div>
        <div class="col-md-7 d-none d-lg-block menu__main">
          <div class="header__menu">
            <ul class="d-flex p-0 mb-0" style="list-style-type: none;margin-top: 2rem;">
                <li><a href="/main">Главная</a></li>
                <li><a href="">Этапы</a></li>
                <li><a href="#">Отзывы</a></li>
                <li><a href="#">Требования</a></li>
                <li><a href="">Информация</a></li>
            </ul>
          </div>
        </div>
        <div class="col-md-2 d-flex justify-content-end d-none d-lg-block" style="align-items: center;">
          <div class="d-flex justify-content-between">
            <div class="d-flex" style="align-items: end;">
              <a href="/notification">
                <img class="" src="../../../assets/images/landing/nott.svg" alt="" />
              </a>
            </div>
            <div class="" style="margin-top: 1rem;">
              <div class="app__button"style="width: 100%;">
                  <a href="/account">Войти</a>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-9 d-flex justify-content-end">
          <div class="d-lg-none">
                <li class="nav-item dropdown" style="  list-style-type: none;">
                  <a class="nav-link" href="#"
                      role="button" data-bs-toggle="dropdown" aria-expanded="false">
                      <svg xmlns="http://www.w3.org/2000/svg" width="47" height="47" fill="currentColor" class="bi bi-list" viewBox="0 0 16 16">
                        <path fill-rule="evenodd" d="M2.5 12a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5"/>
                      </svg>
                  </a>
                  <ul class="dropdown-menu burger" aria-labelledby="it-menu-case-dropdown">
                    <li><a href="#">Главная</a></li>
                    <li><a href="">Этапы</a></li>
                    <li><a href="#">Отзывы</a></li>
                    <li><a href="#">Требования</a></li>
                    <li><a href="#">Информация</a></li>
                    <li><a href="">Войти</a></li>
                  </ul>
                </li>
            </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">

.burger {
  padding: 1rem 1rem 0 1rem;
  li {
    margin-bottom: 1rem;

  }
  a {
    margin-right: 1rem;
    color: rgb(11, 11, 11);
    font-size: 1rem;
    text-decoration: none;
    font-weight: 600;
  }
}
.head__img {
  @media screen and (max-width: 430px) {
    margin-bottom: 1rem;
    }
  img {
    width: 100%;
    @media screen and (max-width: 430px) {
      width: 50%;
    }
  }
}
.app__button {
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
.header__menu {
  a {
    margin-right: 1rem;
    color: rgb(11, 11, 11);
    font-size: 1rem;
    text-decoration: none;
    font-weight: 600;
  }

}
.header__bgc {
  background: rgb(250, 248, 253);
  padding-bottom: 1rem;
  padding-top: 1rem;
  margin-bottom: 5rem;
}
// .header_tel {
//   a {
//     color: rgb(115, 54, 254);
//     font-size: 1rem;
//     font-weight: 500;
//     text-decoration: none;
//   }
// }
</style>

  <!-- <div class="bgc-header">
    <div class="container g-0">
      <div class="row g-0 ll">
        <div class="col-md-3 ">
          <a class="header__logo"href="">
            <img class="" src="../../../assets/images/landing/logoAis.svg" alt="" />
          </a>
        </div>
        <div class="col-md-6 d-none d-lg-block" style="display: flex; align-items: center;">
          <div class="navMenu">
            <ul class="d-flex justify-content-between" style="list-style-type: none;">
              <li><a href="">Главная</a></li>
              <li><a href="">Этапы</a></li>
              <li><a href="">Отзывы</a></li>
              <li><a href="">Требования</a></li>
              <li><a href="">Информация</a></li>
          </ul>
          </div>
        </div>
        <div class="col-md-3">
          <div class="d-flex">
            <div>
              <div class="header__info">
                <a href="">8920*****9087</a>
              </div>
              <div class="header__info">
                <a href="">info@aispek.com</a>
              </div>
          </div>
          <a class="callBack__header"href="">Перезвоните мне</a>
        </div>
        </div>
        <div class="d-lg-none meb-menu__nov col-md-3 d-flex justify-content-end">
                <li class="nav-item dropdown" style="  list-style-type: none;">
                  <a class="nav-link" href="#" id="it-menu-case-dropdown"
                      role="button" data-bs-toggle="dropdown" aria-expanded="false">
                      <svg xmlns="http://www.w3.org/2000/svg" width="47" height="47" fill="currentColor" class="bi bi-list" viewBox="0 0 16 16">
                        <path fill-rule="evenodd" d="M2.5 12a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5"/>
                      </svg>
                  </a>
                  <ul class="dropdown-menu" aria-labelledby="it-menu-case-dropdown">
                      <li><a class="dropdown-item" href=""></a></li>
                      <li><a class="dropdown-item" href="">Войти</a></li>
                      <li><a class="dropdown-item" href="" data-bs-toggle="modal" data-bs-target="#exampleModal">Каталог</a></li>
                      <li><a class="dropdown-item" href="#">О магазине</a></li>
                      <li><a class="dropdown-item" href="#">Распродажа</a></li>
                      <li><a class="dropdown-item" href="">Контакты</a></li>
                      <li><a class="dropdown-item" href="">
                      </a></li>
                  </ul>
                </li>
          </div>
      </div>
    </div>
  </div> -->