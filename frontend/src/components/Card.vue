<template>
  <v-card class="vemos-card" raised hover rounded="lg">
    <slot></slot>
  </v-card>
</template>

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
