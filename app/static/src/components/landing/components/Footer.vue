<script setup>
import { reactive } from "vue";
</script>

<template>
<div class="bgc-footer__first" style="margin-top: 10rem;">
  <div class="container">
    <div class="row">
      <div class="col-md-8">
        <div class="foot__menu">
          <ul class="d-flex flex-column flex-sm-row  p-0 mb-0" style="list-style-type: none;">
              <li><a href="/">Главная</a></li>
              <li><a href="">Этапы</a></li>
              <li><a href="">Отзывы</a></li>
              <li><a href="">Требования</a></li>
              <li><a href="">Информация</a></li>
          </ul>
        </div>
      </div>
      <div class="col-md-4">
        <div class="foot__menu__contact">
          <ul class="d-flex flex-column p-0 mb-0" style="list-style-type: none;">
                <li><a href="">Контакты</a></li>
            </ul>
        </div>
      </div>
    </div>
  </div>
</div>
<div class="bgc__foot__sec">
  <div class="container">
    <div class="row">
      <div class="col-md-8">
        <div class="fooet__slogan" style=" margin-top: 2rem; margin-bottom: 2rem;">
          <a href="">Компания Знаю ПБ предлагает услуги сопровождения бизнеса при подтверждении уровня квалификации персонала, прохождения проверок СРО, контролирующих органов, подготовку и сдачу документации. С нами вы сможете получить лицензию ФСБ и пройти любые виды сертификации, аттестации</a>
        </div>
      </div>
      <div class="col-md-4">
        <div class="d-flex justify-content-between foot__info">
          <div class="foot__post">
            <div>
              <p class="mb-0">Почта</p>
            </div>
            <div>
              <a href="">info@aispek.com</a>
            </div>
          </div>

          <div class="foot__tel">
            <div>
              <p class="mb-0">Телефон</p>
            </div>
            <div>
              <a href="">8920*****9087</a>
            </div>
          </div>

        </div>
        <div class="foot__add">
          <div>
              <p class="mb-0">Адрес</p>
            </div>
            <div>
              <a href="">г. Москва, м Павелецкая, Дербеневская набережная дом 7 корпус 23, офис 10</a>
            </div>
        </div>
      </div>
    </div>
    <div class="row foot__main">
      <div class="col-md-6">
        <div class="foot_rights">
          <a href="">Все права защищены, ссылка на сайт обязательна.</a>
        </div>
      </div>
      <div class="col-md-6 d-flex justify-content-between">
        <div class="foot__policy">
          <a href="">Политика конфиденциальности</a>
        </div>
        <div class=" foot__year">
          <a href="">2024 @ ООО </a>
        </div>
      </div>
      <!-- <div class="col-md-4">
      </div>
      <div class="col-md-2">
      </div> -->
    </div>
  </div>
</div>

</template>

<style scoped lang="scss">
.foot__main {
  @media screen and (max-width: 430px) {
        flex-direction: column;
        }
}
.foot__year {
  a {
    color: rgb(87, 87, 87);
    font-size: 0.7rem;
    text-decoration: none;
    font-weight: 400;
  }
}
.foot__policy {
  a {
    color: rgb(87, 87, 87);
    font-size: 0.7rem;
    font-weight: 400;
  }
}
.foot_rights {
  a {
    color: rgb(87, 87, 87);
    font-size: 0.7rem;
    text-decoration: none;
    font-weight: 400;
  }
}
.foot__info {
  @media screen and (max-width: 768px) {
       flex-direction: column;
        }
}
.foot__add {
  margin-bottom: 3rem;
  @media screen and (max-width: 430px) {
       margin-bottom: 1rem;
        }
  p {
    color: rgb(87, 87, 87);
    font-size: 1rem;
    font-weight: 400;
    margin-bottom: 1rem;
  }
  a {
    color: rgb(115, 54, 254);
    font-size: 1rem;
    font-weight: 500;
    text-decoration: none;
  }
}
.foot__tel {
  margin-top: 2rem;
  margin-bottom: 3rem;
  @media screen and (max-width: 430px) {
       margin-bottom: 1rem;
       margin-top: 0;
        }
  p {
    color: rgb(87, 87, 87);
    font-size: 1rem;
    font-weight: 400;
    margin-bottom: 1rem;
  }
  a {
    color: rgb(115, 54, 254);
    font-size: 1rem;
    font-weight: 500;
    text-decoration: none;
  }
}
.foot__post {
  margin-top: 2rem;
  margin-bottom: 3rem;
  @media screen and (max-width: 430px) {
       margin-bottom: 1rem;
       margin-top: 0;
    }
    @media screen and (width: 768px) {
       margin-bottom: 1rem;
       margin-top: 2rem;
    }
  p {
    color: rgb(87, 87, 87);
    font-size: 1rem;
    font-weight: 400;
    margin-bottom: 1rem;
  }
  a {
    color: rgb(115, 54, 254);
    font-size: 1rem;
    font-weight: 500;
    text-decoration: none;
  }
}
.fooet__slogan {
  width: 60%;
  @media screen and (max-width: 430px) {
       width: 100%;
        }
  a {
    color: rgb(0, 0, 0);
    font-size: 1rem;
    font-weight: 400;
    text-decoration: none;
  }
}
.bgc__foot__sec {
  background: rgb(250, 248, 253);
  padding-bottom: 1rem;
}
.foot__menu__contact {
  a {
    margin-right: 1rem;
    color: rgb(11, 11, 11);
    font-size: 1rem;
    text-decoration: none;
    font-weight: 600;
  }
}
.bgc-footer__first {
  background: linear-gradient(152.65deg, rgb(242, 234, 255) 0.235%,rgb(125, 177, 255) 239.941%);
  padding: 1rem 0 1rem 0;
}
.foot__menu {
  a {
    margin-right: 1rem;
    color: rgb(11, 11, 11);
    font-size: 1rem;
    text-decoration: none;
    font-weight: 600;
  }
  @media screen and (max-width: 450px) {
    display: flex;
        flex-direction: column;
        }
}
</style>