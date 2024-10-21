<script setup>
import { reactive } from "vue";
</script>

<template>
<div id="trebovaniya" class="container">
    <h3 class="mb-5"style="margin-top: 5rem;">Требования к претендентам на удостоверение эксперта по промышленной безопасности включают:</h3>
    <div class="row">
        <div class="col-md-6">
            <div class="req-title">
                <a href="">Российское гражданство.</a>
            </div>
            <div class="req-title-sec">
                <div style="margin-bottom: 1rem;">
                    <a href="">Стаж работы в соответствующей сфере:</a>
                </div>
                <div>
                    <a href="">для первой категории — более 10 лет;<br>
                    для второй категории — более 7 лет;<br>
                    для третьей категории — более 5 лет.</a>
                    
                </div>
            </div>
        </div>
        <div class="col-md-6">
            <div class="req-title">
                <a href="">Наличие высшего образования или учёной степени.</a>
            </div>
            <div class="req-title-sec">
                <div style="margin-bottom: 1rem;">
                    <a href="">Участие в экспертизах промышленной безопасностиОПО:</a>
                </div>
                <div>
                    <a href="">для первой категории — 15 экспертиз;<br>
                    для второй категории — 10 экспертиз;<br>
                    для третьей категории — участие не обязательно.</a>
                    
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<style scoped lang="scss">
.req-title {
    border-radius: 0.25rem;
padding: 1rem;
background: rgb(8, 106, 217);
margin-bottom: 2rem;
a {
    display: flex;
    justify-content: center;
    text-decoration: none;
    color: rgb(255, 255, 255);
    font-size: 1rem;
    font-weight: 600;
}
}
.req-title-sec {
    border-radius: 0.25rem;
padding: 1rem;
background: rgb(8, 106, 217);
margin-bottom: 2rem;
a {
    text-decoration: none;
    color: rgb(255, 255, 255);
    font-size: 1rem;
    font-weight: 600;
}
}
</style>