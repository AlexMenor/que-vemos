<template>
  <v-layout justify-center align-center style="min-height:100%">
    <card class="pa-8">
      <div v-if="!qr" class="presession-card-content">
        <v-img src="@/assets/logo-lemur.png"></v-img>
        <v-btn class="ma-5" color="primary" @click="createSession">
          Crea una sesión</v-btn
        >
        <v-btn class="ma-5"> O únete a una</v-btn>
      </div>
      <div id="qr-parent"></div>
    </card>
  </v-layout>
</template>

<script>
import Card from "@/components/Card.vue";
import axios from "axios";
import * as QRCode from "qrcode";

const API_ENDPOINT = "https://que-vemos.herokuapp.com";
export default {
  components: { Card },
  data() {
    return {
      sessionId: null,
      qr: null,
    };
  },
  methods: {
    async createSession() {
      const { data } = await axios.post(`${API_ENDPOINT}/session`);

      this.sessionId = data["session_id"];

      this.qr = await this.generateQr(this.sessionId);
    },
    generateQr(content) {
      return new Promise((resolve, reject) => {
        QRCode.toCanvas(
          content,
          { errorCorrectionLevel: "H" },
          (err, canvas) => {
            if (err) reject(err);
            resolve(canvas);
          }
        );
      });
    },
  },
  watch: {
    qr() {
      const parent = document.getElementById("qr-parent");
      parent.appendChild(this.qr);
    },
  },
};
</script>

<style>
.presession-card-content {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
</style>
