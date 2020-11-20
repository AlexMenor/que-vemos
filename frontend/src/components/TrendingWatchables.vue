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
        ></v-select>
        <v-radio label="From low to high" value="ASC"></v-radio>
        <v-radio label="From high to low" value="DESC"></v-radio>
      </v-radio-group>
      <v-text-field
        placeholder="Search..."
        style="max-width:300px"
        v-model="search"
      ></v-text-field>
      <v-btn @click="fetch" color="primary">Go</v-btn>
    </v-row>
    <v-row align="center" justify="center">
      <v-card
        class="ma-4"
        v-for="(watchable, i) in watchables"
        :key="i"
        max-width="300"
      >
        <v-container fluid class="d-flex justify-space-between">
          <v-chip>
            {{ watchable.type }}
          </v-chip>
          <div>
            {{ watchable.year }}
          </div>
        </v-container>
        <v-card-title>{{ watchable.title }}</v-card-title>
        <v-card-text class="watchable-body">
          <p>
            {{ watchable.synopsis }}
          </p>
          <v-img :src="watchable.poster"></v-img>
        </v-card-text>
        <v-container fluid class="d-flex justify-end align-center">
          <div>
            Popularity:
          </div>
          <v-chip class="ml-2" color="primary">
            {{ watchable.popularity }}
          </v-chip>
        </v-container>
      </v-card>
    </v-row>
  </v-container>
</template>

<script>
import axios from "axios";

const TRENDING_WATCHABLES_ENDPOINT =
  "https://amazing-villani-e2d732.netlify.app/.netlify/functions/get_trending_watchables";

export default {
  data() {
    return {
      watchables: [],
      order: "DESC",
      orderField: null,
      type: undefined,
      search: undefined,
    };
  },
  async mounted() {
    await this.fetch();
  },
  methods: {
    async fetch() {
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
    },
  },
};
</script>

<style>
.watchable-body {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
}
</style>
