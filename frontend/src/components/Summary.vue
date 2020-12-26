<template>
  <v-layout
    column
    justify-space-between
    align-center
    style="width:100%;height:100vh; overflow:scroll;padding-bottom:85px"
    class="summary"
  >
    <v-layout align-center justify-space-around style="width:100%">
      <v-avatar
        color="primary"
        size="56"
        v-for="user in summary.users"
        :key="user.id"
        class="mb-3"
      >
        <span class="white--text headline">
          {{ user.name ? user.name : "?" | compactUsername }}
        </span>
      </v-avatar>
    </v-layout>
    <v-expansion-panels>
      <v-expansion-panel
        v-for="watchable in summary.votes"
        :key="watchable.title"
      >
        <v-expansion-panel-header
          :color="negativeVotes(watchable).length === 0 ? '#e4ffe8' : undefined"
        >
          {{ watchable.title }}
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <p>
            <v-icon color="green">mdi-check</v-icon>
            {{ positiveVotes(watchable).length }}
            <b
              v-for="(vote, i) in positiveVotes(watchable)"
              :key="i"
              class="ml-2"
              >{{ vote[0].name ? vote[0].name : "?" }}</b
            >
          </p>
          <p>
            <v-icon color="red">mdi-close</v-icon>
            {{ negativeVotes(watchable).length }}
            <b
              v-for="(vote, i) in negativeVotes(watchable)"
              :key="i"
              class="ml-2"
              >{{ vote[0].name ? vote[0].name : "?" }}</b
            >
          </p>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </v-layout>
</template>

<script>
import axios from "axios";

export default {
  props: ["sessionId"],
  data() {
    return {
      summary: null,
      POLLING_INTERVAL: 8000,
    };
  },
  async mounted() {
    this.fetchSummary();
    setInterval(this.fetchSummary, this.POLLING_INTERVAL);
  },
  methods: {
    async fetchSummary() {
      const { data } = await axios.get(
        `${process.env.VUE_APP_API_ENDPOINT}/session/${this.sessionId}/summary`
      );
      this.summary = data;
    },
    positiveVotes(watchable) {
      return watchable.votes.filter((vote) => vote[1]);
    },
    negativeVotes(watchable) {
      return watchable.votes.filter((vote) => !vote[1]);
    },
  },
  filters: {
    compactUsername(userName) {
      return userName.slice(0, 2).toUpperCase();
    },
  },
};
</script>
