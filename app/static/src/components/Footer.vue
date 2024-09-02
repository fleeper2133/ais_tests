<template>
    <div class="footer footer-margin footer--border">
        <p class="footer__date">2023-2024 @ ООО</p>
        <p class="footer__tech">Техническая поддержка:<a href="#">support@dfbg</a></p>
        <nav class="doc-links">
            <a class="footer__docs" href="#">Условия использования</a>
            <a class="footer__docs" href="#">Политика конфиденциальности</a>
        </nav>
    </div>
</template>

<script setup lang="ts">

</script>

<style lang="scss"scoped>
@import '../sass/main.scss';

.footer {
    display: flex;
    justify-content: space-between;
    padding: 1.25rem 15vw;
    gap: 10px;
    width: 100%;
    height: 60px;

    @media (max-width: 1440px) {
        flex-direction: column;
        align-items: center;
        height: auto;
    }
}
.footer__tech {
    display: flex;
    gap: 0.625rem;

    @media (max-width: 400px) {
        flex-direction: column;
        align-items: center;
    }
}
.doc-links {
    display: flex;
    gap: 20px;

    @media (max-width: 600px) {
        flex-direction: column;
        align-items: center;
        gap: 10px;
        margin-top: 10px;
    }
}
.footer__docs {
    text-align: center;
}
.footer-margin {
    margin-top: 50px;
}
.footer--border {
    border-top: 1px solid $border;
}

@media (max-width: 600px) {
    .footer {
      padding: 1.25rem 4vw;
    }
}
@media (max-width: 1440px) {
    .footer {
        padding: 1.25rem 10vw;
    }
}
</style>