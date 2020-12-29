<template>
  <v-card class="vemos-card" raised hover rounded="lg" :img="img">
    <slot></slot>
  </v-card>
</template>

<script>
export default {
  props: ["img"],
};
</script>

<style>
.vemos-card {
  display: flex !important;
  flex-direction: column;
  justify-content: space-between;
  overflow: hidden;
  height: 100%;
  width: 100%;
}
</style>
