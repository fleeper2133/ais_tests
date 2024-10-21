<script setup>
import { reactive } from "vue";
</script>

<template>
<div id="skill" class="container">
    <h3 style="margin-top: 5rem;margin-bottom: 2rem;">Эксперт по промышленной безопасности: квалификация и полномочия</h3>
    <p class="skill__text">Эксперт по ПБ является специалистом, который оценивает опасные производственные объекты (ОПО) в своей области:</p>
    <div class="row">
        <div class="col-md-6">
            <p class="skill_list">нефтегазовой промышленности;</p>
            <p class="skill_list">горнодобывающей промышленности;</p>
            <p class="skill_list">химической промышленности;</p>
            <p class="skill_list">теплоснабжении, др.</p>
        </div>
        <div class="col-md-6">
            <p class="skill_list">транспортировке опасных грузов;</p>
            <p class="skill_list">трубопроводном транспорте;</p>
            <p class="skill_list">газоснабжении;</p>
        </div>
    </div>
    <p class="skill__text-sec" style="margin-top: 2rem;">Также квалификация аттестованного профессионала определяет перечень разрешенных для него работ. Одни эксперты работают над проектной документацией, другие – на консервации и ликвидации ОПО, третьи – на выдаче деклараций ПБ.</p>
</div>
</template>

<style scoped lang="scss">
.skill__text {
    color: rgb(8, 106, 217);
    font-size: 1rem;
    font-weight: 400;
    margin-bottom: 2rem;
}
.skill_list {
    color: rgb(0, 0, 0);
    font-size: 1.2rem;
    font-weight: 500;
}
.skill__text-sec {
    color: rgb(8, 106, 217);
    font-size: 1rem;
    font-weight: 400;
    margin-bottom: 5rem;
}

</style>