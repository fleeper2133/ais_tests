<template>
  <router-view></router-view>
</template>

<script setup lang="ts">

</script>

<style lang="scss">
@import '/src/sass/main.scss';

.button {
  cursor: pointer;
  width: 100%;
  height: 3.75rem;
  border-radius: 0.25rem;
  transition: .2s;
  &:hover {
    transition: .2s;
    opacity: 0.8;
  }
}
</style>
