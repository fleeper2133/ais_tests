<script setup>
import { reactive } from "vue";
import Header from './Header.vue';
import Footer from './Footer.vue';
import Stages from './Stages.vue';
import Skill from './Skill.vue';
import Advant from './Advant.vue';
import Tarif from './Tarif.vue';
import Certificate from './Certificate.vue';
import Application from './Application.vue';
import Request from './Request.vue';

</script>
<template>
    <Header />
    
    <div class="container">
      <div class="row" style="margin-bottom: 5rem;">
        <div class="col-md-7 ">
          <h3 class="main_title">Система подготовки специалистов к сдаче экзамена</h3>
          <div class="main_title__text">
            <p>Для обеспечения теоретической подготовки эксперта в области промышленной безопасности Учебный центр «АИС ПЭК» проводит:</p>
          </div>
          <div class="main_page__point">
            <p>Подготовку специалистов по разработанной индивидуальной программе</p>
          </div>
          <div class="main_page__point">
            <p>Практические занятия по решению ситуационных задач с учетом описания проблемной ситуации и обоснования принятия оптимальных решений и способов их реализации.</p>
          </div>
        </div>
        <div class="col-md-5 main__img">
          <img class="" style="width: 100%;" src="../img/aisR.svg" alt="" />
        </div>
      </div>
    </div>
    <Stages/>
    <Request/>
    <Skill/>
    <!-- <Swiper/> -->
    <Advant/>
    <Tarif/>
    <Certificate/>
    <Application/>

    <Footer/>
</template>

<style scoped lang="scss">
@import "../../sass/landing.scss";
.main_title {
  color: rgb(0, 0, 0);
  font-weight: 500;
  margin-bottom: 2rem;
  &__text {
    p {
      color: rgb(0, 0, 0);
      font-size: 1.2rem;
      font-weight: 400;
      margin-bottom: 2rem;
    }
  }
}
.main_page__point{
  border-radius: 10px;
padding: 0.5rem;
background: rgb(115, 54, 254);
margin-bottom: 1.5rem;
  p {
  color: rgb(255, 255, 255);
  font-size: 1rem;
  font-weight: 500;
  }
}
.main__img {
  display: flex;
  justify-content: flex-end;
}
</style>
