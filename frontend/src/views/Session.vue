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
      :queue.sync="queue"
      :offset-y="10"
      @submit="onSubmit"
      v-if="queue"
    >
      <template slot-scope="scope">
        <watchable :watchable="scope.data"></watchable>
      </template>
    </Tinder>
    <card v-else class="pa-4">
      <v-card-title>¡Ya estás casi dentro!</v-card-title>
      <v-text-field
        label="Tu nombre (opcional)"
        v-model="userName"
      ></v-text-field>
      <v-btn color="primary" @click="joinSession">Continuar</v-btn>
    </card>
  </v-layout>
</template>

<script>
import axios from "axios";
import Watchable from "@/components/Watchable.vue";
import Card from "@/components/Card.vue";
import Tinder from "vue-tinder";

export default {
  components: { Watchable, Tinder, Card },
  data() {
    return {
      sessionId: this.$route.params.id,
      session: null,
      watchableIndex: 0,
      queue: null,
      userName: "",
    };
  },
  methods: {
    async joinSession() {
      const { data } = await axios.post(
        `${process.env.VUE_APP_API_ENDPOINT}/session/${this.sessionId}/user${
          this.userName ? `?user_name=${this.userName}` : ""
        }`
      );
      this.session = data;
      this.queue = [...this.session.watchables];
    },
    async onSubmit(item) {
      const { key, type } = item;
      await axios.post(
        `${process.env.VUE_APP_API_ENDPOINT}/session/${this.sessionId}/user/${this.session.user_id}/vote`,
        {
          watchable_index: this.session.watchables.findIndex(
            (watchable) => watchable.title === key
          ),
          content: type === "like",
        }
      );
    },
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
}
.tinder-card {
  display: flex;

  justify-content: center;
  align-items: center;
}
</style>
