<script setup>
import { reactive } from "vue";
</script>

<template>
<div id="advantages" class="container">
    <h3 style="margin-bottom: 2rem;">
        Наши преимущества
    </h3>
    <div class="bgc-advent">
        <div class="row">
            <div class="col-md-6">
                <div>
                    <div style="margin-bottom: 1rem;"class="">
                        <a class="advent__title"href="">Передовые технологии дистанционного обучения</a>
                    </div>
                    <div style="margin-bottom: 2rem;"  class="">
                        <a class="advent__text" href="">
                            Пройти обучение или аттестацию можно с помощью нашего Портала, без отрыва от производств
                        </a>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div>
                    <div style="margin-bottom: 1rem;"class="">
                        <a class="advent__title"href="">Наличие необходимых Лицензий</a>
                    </div>
                    <div style="margin-bottom: 2rem;"class="">
                        <a class="advent__text" href="">
                            Мы имеем Лицензию на образовательную деятельность и проведение Экспертизы ПБ
                        </a>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div>
                    <div style="margin-bottom: 1rem;"class="">
                        <a class="advent__title"href="">Гарантия</a>
                    </div>
                    <div style="margin-bottom: 2rem;"  class="">
                        <a class="advent__text" href="">
                            Гарантированное получение необходимых разрешений в предельно сжатые сроки.
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<style scoped lang="scss">
.advent__title {
    text-decoration: none;
    color: rgb(255, 255, 255);
    font-size: 1.2rem;
    font-weight: 600;
}
.advent__title__thr{
    height: 50px;
    @media screen and (max-width: 769px) {
    height: 30px;
    }
}
.advent__text {
    color: rgb(224, 236, 255);
    font-size: 1rem;
    font-weight: 400;
    text-decoration: none;

}
.bgc-advent {
    border-radius: 0.25rem;
    padding: 2rem 1rem 0 1rem;
    background: rgb(115, 54, 254);
}
</style>