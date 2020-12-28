<template>
  <video id="qr-video"></video>
</template>

<script>
import QrScanner from "qr-scanner";
export default {
  mounted() {
    const videoElem = document.querySelector("#qr-video");
    const qrScanner = new QrScanner(videoElem, (result) => {
      this.$emit("result", result);
      qrScanner.destroy();
    });
    qrScanner.start();
  },
};
</script>
