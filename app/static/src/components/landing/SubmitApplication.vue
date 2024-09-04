<script setup>
import { reactive } from "vue";
import Header from './components/Header.vue';
import Footer from './components/Footer.vue';

import { ref } from 'vue';


const users = ['A.1 Основы промышленной безопасности', 'A.2 Основы промышленной безопасности', 'A.3 Основы промышленной безопасности'];
const selectedUser = ref('');

// const showBlock = ref(false);

function showBlock() {
    const card = document.getElementById('card');
    card.style.display = 'block';

    const cardSec = document.getElementById('cardSec');
    cardSec.style.display = 'none';


}

function showBlockSec() {
    const cardSec = document.getElementById('cardSec');
    cardSec.style.display = 'block';

    const card = document.getElementById('card');
    card.style.display = 'none';

} 
</script>

<template>
<Header />
<div class="container">
    <div class="d-flex justify-content-center">
        <h3 style="margin-bottom: 2rem;">Подать заявку</h3>
    </div>
    <div class="d-flex justify-content-center">
        <div class="prop__name">
            <p class="">Введите почту:</p>
            <input  type="text" name="" id="">
        </div>
    </div>
    <div class="d-flex justify-content-center">
        <div class="prop__name">
            <p class="">Введите номер телефона:</p>
            <input  type="text" name="" id="">
        </div>
    </div>
    <div class="d-flex justify-content-center">
        <div class="prop__name">
            <p class="">Введите ФИО:</p>
            <input  type="text" name="" id="">
        </div>
    </div>
    <div class="d-flex justify-content-center">
        <div class="prop__name">
            <p class="">Выберите направление курса:</p>
            <!-- <div class="dropdown" >
                <button class="btn btn-prop dropdown-toggle"type="button" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false">
                </button>
                <ul class="dropdown-menu" style="" aria-labelledby="dropdownMenuButton1">
                    <li><a class="dropdown-item" href="#">A.1 Основы промышленной безопасности</a></li>
                    <p style="padding: 0 1rem 0 1rem ; color:  rgb(8, 106, 217);">Период обучения с 12.02.24 по 12.03.24</p>
                    <hr>
                    <li><a class="dropdown-item" href="#">A.1 Основы промышленной безопасности</a></li>
                    <p style="padding: 0 1rem 0 1rem ; color:  rgb(8, 106, 217);">Период обучения с 12.02.24 по 12.03.24</p>
                </ul>
            </div> -->
            <div>
                <select class="drop__us" id="user-select" v-model="selectedUser">
                <option v-for="user in users" :value="user">{{ user }}</option>
                </select>
            </div>
        </div>
    </div>
</div>
<div class="bgc__prop">
    <div class="container">
        <div class="d-flex justify-content-center">
            <h3 style="margin-bottom: 2rem;">Детали оплаты</h3>
        </div>
        <div class="d-flex justify-content-center">
            <p>Назначение платежа: <span style="font-weight: 600; font-size: 1rem;">A.1 Основы промышленной безопасности</span></p>
        </div>
        <div class="d-flex justify-content-center">
            <p>Стоимость курса: <span style="font-weight: 600; font-size: 1rem;">20 000₽</span></p>
        </div>
    </div>
</div>
<div class="container">
    <div class="d-flex justify-content-center">
        <h3 style="margin-bottom: 2rem;">Пополнение баланса</h3>
    </div>
    <div class="prop__pay d-flex justify-content-center">
        <div>
            <p class="" style="margin-bottom: 0.5rem;">Способо оплаты</p>
            <div class="d-flex">
                <div class="non-cash">
                    <button @click="showBlockSec">Безналичная оплата</button>
                </div>
                <div class="bank-card">
                    <button @click="showBlock">Банковская карта</button>
                </div>
            </div>
            <div class="" style="margin-top: 1rem;">
                <p style="margin-bottom: 0.5rem;">Сумма для пополнения</p>
                <input class="prop_sum"type="text">
                <div class="prop__total" style="margin-top:1rem;margin-bottom: 2rem;">
                    <a href="">Итого:</a>
                </div>
            </div>
            <!-- <button  class="app__button"style="width: 100%;">
                Перейти к оплате
            </button> -->
        </div>
    </div>
    <div id="card" style="display: none;">
        <div class=" d-flex justify-content-center">
            <div class="bgc-pay" style="z-index: 1;">
                <p style="margin-bottom: 0.5rem;">Номер карты</p>
                <input class="prop__inf__num"style="" type="text">

                <p style="margin-bottom: 0.5rem; margin-top: 1rem;">Срок действия</p>
                <input style="width: 100px;" type="text" placeholder="__/ __">
                <input class="prop__cvv" style="width: 100px;" type="text" placeholder="CVV">

                <p style="margin-bottom: 0.5rem; margin-top: 1rem;">Держатель карты</p>
                <input class="prop__inf" type="text">
                <div class="d-flex justify-content-center">
                    <div class="propp__button"style="width: 70%;">
                    <a href="">Оплатить</a>
                    </div>
                </div>
            </div>
            <div class="prop__img__right">
                <img class="ll" style="margin-left: -1rem; z-index: 0; width: 90%; margin-top: 1rem;" src="../../assets/images/landing/prop.svg" alt="" />
            </div>
        </div>
    </div>
    <div id="cardSec" style="display: none;">
        <div class="d-flex justify-content-center" >
            <div class="bgc-non__cash">
                <div class="d-flex justify-content-center prop__num-res">
                    <p>Счет на оплату:
                    <span>№2#######</span>
                    </p>
                </div>
                <div class="bgc-for__text">
                    <p>Дата:
                        <span>от 22.03.24</span>
                    </p>
                </div>
                <div class="bgc-for__text">
                    <p>Поставщик:
                        <span>ООО “Аис Пэк”</span>
                    </p>
                </div>
                <div class="bgc-for__text">
                    <p>Получатель:
                        <span>Иванов Иван Иванович</span>
                    </p>
                </div>
                <div class="bgc-for__text">
                    <p>Назначение платежа:
                        <span> A.1 Основы промышленной безопасности</span>
                    </p>
                </div>
                <div class="d-flex justify-content-between">
                    <div class="prop__result">
                        <a href="">Итого:
                            <span>30 000₽</span>
                        </a>
                    </div>
                    <div >
                        <button class="prop__res">Оплатить</button>
                    </div>
                </div>
                <div class="prop__link">
                    <p>Перейдя по ссылке, вы сможете распечатать образец платежного поручения или оплатить счет онлайн любым удобным для вас способом.</p>
                </div>
            </div>
        </div>
    </div>
</div>



<Footer />
</template>

<style scoped lang="scss">
@import '../../sass/styles.scss';

.drop__us {
        box-sizing: border-box;
        border: 2px solid rgb(125, 177, 255);
        border-radius: 5px;
        background: rgba(255, 255, 255, 0.71);
        width: 600px;
        padding-left: 0.5rem;
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-right: 0.5rem;
        color: rgb(0, 0, 0);
        font-size: 1rem;
        margin-bottom: 0.5rem;
        font-weight: 500;
        @media screen and (max-width: 430px) {
        width: 100%;
        }
}
.drop__us:hover {
    border: 2px solid rgb(125, 177, 255);
}
.prop__num-res {
    p {
        color: rgb(0, 0, 0);
        text-decoration: none;
        font-size: 1.2rem;
        font-weight: 400;
    }
    span {
        color: rgb(0, 0, 0);
        text-decoration: none;
        font-size: 1.2rem;
        font-weight: 600;
    }
}
.prop__link {
    margin-top: 1rem;
    p {
        color: rgb(129, 129, 129);
        font-size: 1rem;
        font-weight: 500;
    }
}
.prop__res {
    border-radius: 10px;
    padding: 0.5rem 2rem 0.5rem 2rem;
    background: rgb(115, 54, 254);
    color: white;
    border: 0;
    margin-top: 1rem;
}
.prop__res:hover {
      color: rgb(37, 42, 193);
    }
.prop__result {
    display: flex;
    align-items: center;
    margin-top: 1rem;
    a {
        color: rgb(0, 0, 0);
        text-decoration: none;
        font-size: 1.2rem;
        font-weight: 400;
    }
    span {
        color: rgb(0, 0, 0);
        text-decoration: none;
        font-size: 1.2rem;
        font-weight: 600;
    }
}
.bgc-for__text {
    border-radius: 5px;
    padding: 0.5rem;
    background: rgb(255, 255, 255);
    margin-bottom: 1rem;
    p {
        color: rgb(0, 0, 0);
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0;
    }
    span {
        color: rgb(0, 0, 0);
        font-size: 1rem;
        font-weight: 400;
        margin-bottom: 0;
    }
}
.bgc-non__cash {
    border-radius: 10px;
    padding: 1rem;
    width: 600px;
    background: rgb(224, 236, 255);
}
.bgc-non__cash:active {
    background: rgb(21, 96, 217);
}
.bank-card {
    button {
            border-radius: 10px;
            box-shadow: 0px 0px 5.3px 0px rgba(0, 0, 0, 0.25);
            background: rgb(255, 255, 255);
            padding: 1rem;
            color: rgb(0, 0, 0);
            font-size: 1rem;
            text-decoration: none;
            font-weight: 500;
            border: 0;
    }
    button:hover {
        background: rgb(115, 54, 254);
        color: white;
    }
}
.non-cash {
    button {
        border-radius: 10px;
        box-shadow: 0px 0px 5.3px 0px rgba(0, 0, 0, 0.25);
        background: rgb(255, 255, 255);
        padding: 1rem;
        margin-right: 1rem;
        color: rgb(0, 0, 0);
        font-size: 1rem;
        text-decoration: none;
        font-weight: 500;
        border: 0;
        }
        button:hover {
                background: rgb(115, 54, 254);
                color: white;
            }
}
.prop__cvv {
    margin-left: 5rem;
    @media screen and (max-width: 430px) {
        margin-left: 1rem;
        }
}
.prop__inf {
        width: 600px;
        @media screen and (max-width: 430px) {
        width: 100%;
        }
}
.prop__inf__num {
    width: 280px;
        @media screen and (max-width: 430px) {
        width: 100%;
        }
}
.prop__img__right {
    @media screen and (max-width: 768px) {
    display: none;
    }
}
.propp__button {
    margin-top: 5rem;
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
.bgc-pay {
    border-radius: 10px;
    padding: 1rem;
    box-shadow: 6px 0px 5.8px 0px rgba(142, 142, 142, 0.25);
    background: linear-gradient(214.70deg, rgb(173, 215, 234) 27.564%,rgb(125, 177, 255) 98.616%);
    p {
        color: rgb(99, 99, 99);
        font-size: 1rem;
        font-weight: 400;
    }
    input {
        border-radius: 5px;
border: 0;
background: rgb(255, 255, 255);
height: 30px;
padding-left: 0.5rem;
    }
}
.app__button {
    margin-top: 2rem;
    margin-bottom: 5rem;
    border-radius: 10px;
    padding: 0.5rem;
    background: rgb(115, 54, 254);
    display: flex;
    justify-content: center;
    text-decoration: none;
    color: rgb(255, 255, 255);
    font-size: 1rem;
    font-weight: 500;
    border: none;
}
.app__button:hover {
      color: rgb(37, 42, 193);
    }
.prop__total {
    a {
        color: rgb(8, 106, 217);
        text-decoration: none;
        font-size: 1rem;
        font-weight: 600;

    }
}
.prop_sum {
    width: 300px;
    box-sizing: border-box;
    border: 1px solid rgb(0, 0, 0);
    border-radius: 5px;
    height: 40px;
    padding-left: 0.5rem;
    background: rgb(255, 255, 255);
}
.btn-pay  {
    box-sizing: border-box;
border: 1px solid rgb(0, 0, 0);
border-radius: 5px;
width: 300px;
background: rgb(255, 255, 255);
}
.dropdown-menu {
    width: 600px;
    @media screen and (max-width: 430px) {
    width: 100%;
    }
}
.bgc__prop {
    background: rgb(242, 234, 255);
    margin-top: 5rem;
    padding-top: 1rem;
    padding-bottom: 1rem;
    margin-bottom: 5rem;
}
.drop__time {
    color: rgb(8, 106, 217);
    font-size: 1rem;
    font-weight: 500;
}
.btn-prop {
    background: rgb(125, 177, 255);
    box-sizing: border-box;
    border: 2px solid rgb(125, 177, 255);
    border-radius: 5px;
    height: 100%;
    width: 600px;
    @media screen and (max-width: 430px) {
    width: 100%;
    }
}
.prop__name {
    margin-bottom: 3rem;
    width: 600px;
    
    p {
        color: rgb(0, 0, 0);
        font-size: 1rem;
        margin-bottom: 0.5rem;
        font-weight: 500;
    }

    input {
        box-sizing: border-box;
        border: 2px solid rgb(125, 177, 255);
        border-radius: 5px;
        background: rgba(255, 255, 255, 0.71);
        height: 90%;
        width: 600px;
        padding-left: 0.5rem;
        @media screen and (max-width: 430px) {
        width: 100%;
    }
    }
}
</style>