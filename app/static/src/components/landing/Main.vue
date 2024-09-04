<script setup>
import Header from './components/Header.vue';
import Footer from './components/Footer.vue';
import Stages from './components/Stages.vue';
import Skill from './components/Skill.vue';
import Advant from './components/Advant.vue';
import Tarif from './components/Tarif.vue';
import Certificate from './components/Certificate.vue';
import Application from './components/Application.vue';



import Request from './components/Request.vue';

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
          <img class="" style="width: 100%;" src="../../assets/images/landing/aisR.svg" alt="" />
        </div>
      </div>
    </div>
    <Stages/>
    <Request/>
    <Skill/>
    <Advant/>
    <Tarif/>
    <Certificate/>
    <Application/>

    <Footer/>
</template>

<style scoped lang="scss">
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
