<template>
  <v-app>
    <v-app-bar app color="white">
      <v-img
        :src="require('@/assets/logo.png')"
        alt="que-vemos logo"
        max-width="200px"
      />
      <v-spacer></v-spacer>
      <feedback></feedback>
    </v-app-bar>

    <v-main style="background-color: #f2b987">
      <trending-watchables></trending-watchables>
    </v-main>
  </v-app>
</template>

<script>
import TrendingWatchables from "@/components/TrendingWatchables.vue";
import Feedback from "@/components/Feedback.vue";
export default {
  name: "App",

  components: { TrendingWatchables, Feedback },

  data: () => ({
    //
  }),
};
</script>
