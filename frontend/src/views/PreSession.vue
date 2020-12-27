<template>
  <v-layout
    justify-center
    align-center
    style="height:100%;width:100%;overflow:hidden"
    class="pa-4"
  >
    <card style="max-width:700px">
      <div v-if="!qr" class="presession-card-content">
        <v-img src="@/assets/logo-lemur.png" max-height="400px" contain></v-img>
        <v-btn class="ma-5" color="primary" @click="createSession">
          Crea una sesión</v-btn
        >
        <v-btn class="ma-5" @click="scanQr"> O únete a una</v-btn>
      </div>
      <v-layout v-show="qr" column justify-center align-center class="pa-4">
        <p>Los demás tienen que escanear este código</p>
        <div id="qr-parent"></div>
        <p>O entrar en:</p>
        <router-link :to="relativeSessionLink">{{ sessionLink }}</router-link>
      </v-layout>
    </card>
  </v-layout>
</template>

<script>
import Card from "@/components/Card.vue";
import axios from "axios";
import * as QRCode from "qrcode";
import QRScanner from "qr-code-scanner";

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
      const { data } = await axios.post(
        `${process.env.VUE_APP_API_ENDPOINT}/session`
      );

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
    scanQr() {
      QRScanner.initiate({
        onResult: console.log,
        timeout: 10000,
      });
    },
  },
  watch: {
    qr() {
      const parent = document.getElementById("qr-parent");
      parent.appendChild(this.qr);
    },
  },
  computed: {
    sessionLink() {
      return window.location.href + "/" + this.sessionId;
    },
    relativeSessionLink() {
      return "/session/" + this.sessionId;
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
