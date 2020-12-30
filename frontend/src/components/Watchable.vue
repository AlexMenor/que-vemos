<template>
  <card :img="watchable.poster">
    <div
      style="display:flex; background-color: rgba(255,255,255,0.8); flex-direction: column; height: 100%; justify-content: space-between"
    >
      <div>
        <v-container fluid class="d-flex justify-space-between">
          <v-chip color="primary">
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
      <v-container fluid class="d-flex justify-end align-center">
        <div>
          Popularity:
        </div>
        <v-chip class="ml-2" color="primary">
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
