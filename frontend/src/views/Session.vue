<template>
  <v-layout
    style="min-width:100%; min-height:100%"
    justify-center
    align-center
    class="pa-4"
  >
    <watchable
      v-if="session"
      :watchable="session.watchables[watchableIndex]"
    ></watchable>
  </v-layout>
</template>

<script>
import axios from "axios";
import Watchable from "@/components/Watchable.vue";

export default {
  components: { Watchable },
  data() {
    return {
      sessionId: this.$route.params.id,
      session: null,
      watchableIndex: 0,
    };
  },
  mounted() {
    this.joinSession();
  },
  methods: {
    async joinSession() {
      const { data } = await axios.post(
        `${process.env.VUE_APP_API_ENDPOINT}/session/${this.sessionId}/user`
      );
      this.session = data;
    },
  },
};
</script>
