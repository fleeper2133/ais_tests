<script setup>
import { reactive } from "vue";
</script>

<template>
<div class="container">
    <h3 style="margin-top: 5rem; margin-bottom: 2rem;">По окончанию обучения выдается  сертификат</h3>
    <div class="sert__about">
        <p style="margin-bottom: 2rem;">Лица, которые успешно прошли все этапы экзамена, в течение 7 дней получают сертификат. Одновременно данные о новом уполномоченном специалисте заносятся в единый реестр на сайте gosnadzor.ru.
            В дальнейшем в этом реестре будут отражены данные об экспертизах, проведенных аттестованным профессионалом.</p>
    </div>
    <div class="row">
        <div class="col-md-4">
            <div class="sert_max">
                <img class="" style="width: 100%;" src="../../img/examp.svg" alt="" />
            </div>
        </div>
        <div class="col-md-8 sert_min">
             <div style="display: flex;">
                <p style="align-items: start;">Образец сертификата</p>
            </div>
            <div class="">
                <div class="d-flex sert__photo">
                    <img class="me-4" src="../../img/examp.svg" alt="" />
                    <img class="me-4" src="../../img/examp.svg" alt="" />
                </div>
            </div>
        </div>
        <div class="sert__time" style="margin-top: 2rem;">
            <p class="mb-0">Сертификат легитимно на протяжении 5 лет после выдачи. По окончании срока его действия потребуется прохождение переаттестации.</p>
        </div>
    </div>
</div>

</template>


<style scoped lang="scss">
.sert__photo {
    img {
        width: 150px;
        @media screen and (max-width: 768px) {
        width: 100px;
        }
    }
}
.sert_min {
    p {
        color: rgb(8, 106, 217);
        font-size: 1rem;
        font-weight: 500;
    }
}
.sert__about {
    p {
        color: rgb(0, 0, 0);
        font-size: 1rem;
        font-weight: 500;
    }
}
.sert__time {
    p {
        color: rgb(8, 106, 217);
        font-size: 1rem;
        font-weight: 400;
    }
}
// .sert_min {
//     align-items: end;
//     @media screen and (max-width: 320px) {
//         flex-direction: column;
//         align-items: start;
//         }
//     img {
//         width: 200px;
//         @media screen and (max-width: 1025px) {
//         width: 100px;
//         }
//         @media screen and (max-width: 320px) {
//         margin-bottom: 1rem;
//         }

//     }
// }
.sert_max {
    @media screen and (max-width: 430px) {
        margin-bottom: 2rem;
        }
}
</style>