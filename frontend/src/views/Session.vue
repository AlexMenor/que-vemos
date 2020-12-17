<template>
  <v-layout
    style="min-width:100%; min-height:100%"
    justify-center
    align-center
    class="pa-4"
  >
    <Tinder
      ref="tinder"
      key-name="title"
      :queue.sync="session.watchables"
      :offset-y="10"
      @submit="onSubmit"
      v-if="session"
    >
      <template slot-scope="scope">
        <watchable :watchable="scope.data"></watchable>
      </template>
    </Tinder>
  </v-layout>
</template>

<script>
import axios from "axios";
import Watchable from "@/components/Watchable.vue";
import Tinder from "vue-tinder";

export default {
  components: { Watchable, Tinder },
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
    onSubmit() {},
  },
};
</script>

<style>
#app .vue-tinder {
  position: absolute;
  z-index: 1;
  left: 0;
  right: 0;
  margin: auto;

  width: 90%;
  height: 90%;

  display: flex;

  justify-content: center;
  align-items: center;
}
</style>
