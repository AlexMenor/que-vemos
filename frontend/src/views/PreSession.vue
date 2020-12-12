<template>
  <v-layout justify-center align-center style="min-height:100%">
    <card class="pa-8">
      <v-img src="@/assets/logo-lemur.png"></v-img>
      <v-btn class="ma-5" color="primary" @click="createSession">
        Crea una sesión</v-btn
      >
      <v-btn class="ma-5"> O únete a una</v-btn>
    </card>
  </v-layout>
</template>

<script>
import Card from "@/components/Card.vue";
import axios from "axios";

const API_ENDPOINT = "https://que-vemos.herokuapp.com";
export default {
  components: { Card },
  data() {
    return {
      sessionId: null,
    };
  },
  methods: {
    async createSession() {
      const { data } = await axios.post(`${API_ENDPOINT}/session`);

      this.sessionId = data["session_id"];
    },
  },
};
</script>

<style></style>
