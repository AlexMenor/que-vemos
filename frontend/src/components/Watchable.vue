<template>
  <card :img="watchable.poster">
    <div
      style="display:flex; background-color: rgba(0,0,0,0.5); flex-direction: column; height: 100%; justify-content: space-between"
    >
      <div>
        <v-container fluid class="d-flex justify-space-between">
          <v-chip>
            {{ watchable.type }}
          </v-chip>
          <div style="color: white">
            {{ watchable.year }}
          </div>
        </v-container>
        <v-card-title style="color:white; font-size:2em">{{
          watchable.title
        }}</v-card-title>
        <v-card-text style="color:white; font-size:1.2em; line-height:1.6">
          <p>
            {{ watchable.synopsis }}
          </p>
        </v-card-text>
      </div>
      <v-container fluid class="d-flex justify-end align-center">
        <div style="color: white">
          Popularity:
        </div>
        <v-chip class="ml-2">
          {{ watchable.popularity }}
        </v-chip>
      </v-container>
    </div>
  </card>
</template>

<script>
import Card from "@/components/Card.vue";
export default {
  props: ["watchable"],
  components: { Card },
};
</script>
