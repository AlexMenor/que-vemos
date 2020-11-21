<template>
  <v-card class="ma-4 watchable" max-width="300">
    <div>
      <v-container fluid class="d-flex justify-space-between">
        <v-chip>
          {{ watchable.type }}
        </v-chip>
        <div>
          {{ watchable.year }}
        </div>
      </v-container>
      <v-card-title>{{ watchable.title }}</v-card-title>
      <v-card-text>
        <p>
          {{ watchable.synopsis }}
        </p>
      </v-card-text>
    </div>
    <v-img :src="watchable.poster" class="ma-4"></v-img>
    <v-container fluid class="d-flex justify-end align-center">
      <div>
        Popularity:
      </div>
      <v-chip class="ml-2" color="primary">
        {{ watchable.popularity }}
      </v-chip>
    </v-container>
  </v-card>
</template>

<script>
export default {
  props: ["watchable"],
};
</script>

<style>
.watchable {
  display: flex !important;
  flex-direction: column;
  justify-content: space-between;
}
</style>
