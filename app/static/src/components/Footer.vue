<template>
    <div class="footer footer-margin footer--border">
        <p class="">2023-2024 @ ООО</p>
        <p class="footer__tech">Техническая поддержка:<a href="#">support@dfbg</a></p>
        <nav class="doc-links">
            <a href="#">Условия использования</a>
            <a href="#">Политика конфиденциальности</a>
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
    padding: 1.25rem 10vw;
    flex-wrap: wrap;
    gap: 10px;
}
.footer__tech {
    display: flex;
    gap: 0.625rem;
}
.doc-links {
    display: flex;
    gap: 20px;
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

// copied
.fw-bold {
  font-weight: bold;
}
.fw-medium {
  font-weight: medium;
}
.main-blue {
  color: $main-blue !important;
}
.grey-text {
  color: $main-grey;
}

.fs-14 {
  font-size: 14px;
}
.fs-18 {
  font-size: 18px;
}
.fs-20 {
  font-size: 20px;
}
.fs-24 {
  font-size: 24px;
}
// copied
</style>