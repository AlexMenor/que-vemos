<template>
  <v-dialog v-model="dialog" width="500">
    <template v-slot:activator="{ on, attrs }">
      <v-btn class="ma-5" v-bind="attrs" v-on="on"> O únete a una</v-btn>
    </template>
    <qr-scanner @result="(result) => this.$emit('result', result)"></qr-scanner>
  </v-dialog>
</template>

<script>
import QrScanner from "@/components/QrScanner.vue";
export default {
  components: { QrScanner },
  data() {
    return {
      dialog: false,
    };
  },
};
</script>
