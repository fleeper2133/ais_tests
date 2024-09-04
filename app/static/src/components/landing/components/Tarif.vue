<script setup>
import { reactive } from "vue";
</script>

<template>
<div class="container">
    <h3 style="margin-top:5rem;">Тариф</h3>
    <div class="row">
        <div class="col-md-6" style="position: relative;">
            <div class="bgc-tarif" >
                <p class="tarif__name">Базовый тариф: все необходимые материалы для обучения </p>
                <div style="    margin-bottom: 2rem;">
                    <a class="tarif__price"htef="">97 500 ₽ / в месяц</a>
                </div>
                <p class="tarif__text">Профессиональная программа повышения квалификации</p>
            </div>
            <div class="tarif__img">
                <img  style="position: absolute;top: 7rem; right: -2rem;" src="../../../assets/images/landing/sales.svg" alt="" />
            </div>
        </div>
        <div class="col-md-6">
            <div style="margin-top: 2rem;">
                <p>Компания «АИС ПЭК» поможет в подготовке и сопровождении процесса аттестации, аккредитации. Проведем независимую оценку дел и оснащенности организации, поможем составить пакет документов и обучим  в дистанционном формате.</p>
            </div>
        </div>
    </div>
</div>
</template>

<style scoped lang="scss">
.bgc-tarif {
    margin-top: 2rem;
    border-radius: 10px;
padding: 1rem;
background: rgb(125, 177, 255);
}
.tarif__name {
    color: rgb(255, 255, 255);
    font-size: 1.2rem;
    font-weight: 600;
    margin-bottom: 2rem;
}
.tarif__text {
    color: rgb(255, 255, 255);
    font-size: 1.2rem;
    font-weight: 600;
    margin-bottom: 0;
}
.tarif__price {
    color: rgb(255, 255, 255);
    font-size: 2rem;
    font-weight: 600;
    text-decoration: none;

}
.tarif__img {
    img {
        @media screen and (max-width: 430px) {
        display: none;
        }

    }
}
</style>