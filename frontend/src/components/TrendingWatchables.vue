<template>
  <v-container>
    <v-row align="center" justify="space-around">
      <v-radio-group v-model="type" style="max-width:100px;">
        <template v-slot:label>
          <div>Type</div>
        </template>
        <v-radio label="Movie" value="MOVIE"></v-radio>
        <v-radio label="Series" value="SERIES"></v-radio>
      </v-radio-group>
      <v-radio-group v-model="order" style="max-width:200px;">
        <template v-slot:label>
          <div>Order</div>
        </template>
        <v-select
          v-model="orderField"
          :items="['popularity', 'year']"
          outlined
          placeholder="Select a field "
        ></v-select>
        <v-radio label="From low to high" value="ASC"></v-radio>
        <v-radio label="From high to low" value="DESC"></v-radio>
      </v-radio-group>
      <v-text-field
        placeholder="Search..."
        style="max-width:300px"
        v-model="search"
        outlined
      ></v-text-field>
      <v-btn @click="fetch" color="primary">Go</v-btn>
    </v-row>
    <v-row v-if="loading" align="center" justify="center">
      <v-progress-circular indeterminate color="primary"></v-progress-circular>
    </v-row>
    <v-row v-else align="stretch" justify="center">
      <watchable
        v-for="(watchable, i) in watchables"
        :key="i"
        :watchable="watchable"
      ></watchable>
    </v-row>
  </v-container>
</template>

<script>
import axios from "axios";
import Watchable from "@/components/Watchable.vue";

const TRENDING_WATCHABLES_ENDPOINT =
  "https://amazing-villani-e2d732.netlify.app/.netlify/functions/get_trending_watchables";

export default {
  components: { Watchable },
  data() {
    return {
      watchables: [],
      order: "DESC",
      orderField: null,
      type: undefined,
      search: undefined,
      loading: true,
    };
  },
  async mounted() {
    await this.fetch();
  },
  methods: {
    async fetch() {
      this.loading = true;
      const params = {
        type: this.type,
        orderBy: this.orderField
          ? `${this.orderField},${this.order}`
          : undefined,
        search: this.search,
      };
      const { data } = await axios.get(TRENDING_WATCHABLES_ENDPOINT, {
        params,
      });

      this.watchables = data;
      this.loading = false;
    },
  },
};
</script>
