<template>
  <v-card class="ma-4 vemos-card" max-width="350" raised hover rounded="lg">
    <slot></slot>
  </v-card>
</template>

<style>
.vemos-card {
  display: flex !important;
  flex-direction: column;
  justify-content: space-between;
  overflow: hidden;
  min-height: 100%;
  min-width: 100%;
  max-height: 100%;
  max-width: 100%;
}
</style>
