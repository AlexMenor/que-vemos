<template>
  <card>
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
    <v-img :src="watchable.poster" class="ma-4" max-height="30vh"></v-img>
    <v-container fluid class="d-flex justify-end align-center">
      <div>
        Popularity:
      </div>
      <v-chip class="ml-2" color="primary">
        {{ watchable.popularity }}
      </v-chip>
    </v-container>
  </card>
</template>

<script>
import Card from "@/components/Card.vue";
export default {
  props: ["watchable"],
  components: { Card },
};
</script>
