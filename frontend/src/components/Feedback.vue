<template>
  <div class="text-center">
    <v-dialog v-model="dialog" width="500">
      <template v-slot:activator="{ on, attrs }">
        <v-btn color="red lighten-2" dark v-bind="attrs" v-on="on">
          Send Feedback
        </v-btn>
      </template>

      <v-card>
        <v-card-title class="headline grey lighten-2">
          What can we do better?
        </v-card-title>

        <v-card-text class="mt-3">
          The message you submit below will be sent towards our developer
          feedback channel in Telegram!
        </v-card-text>
        <v-textarea class="pa-3" outlined v-model="text"></v-textarea>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="dialog = false">
            Close
          </v-btn>
          <v-btn color="primary" @click="send">
            Send
          </v-btn>
        </v-card-actions>
      </v-card>
      <v-snackbar v-model="snackbar">
        {{ snackbarText }}

        <template v-slot:action="{ attrs }">
          <v-btn color="white" text v-bind="attrs" @click="snackbar = false">
            Close
          </v-btn>
        </template>
      </v-snackbar>
    </v-dialog>
  </div>
</template>

<script>
import axios from "axios";
const SEND_FEEDBACK_ENDPOINT =
  "https://amazing-villani-e2d732.netlify.app/.netlify/functions/send_feedback";

export default {
  data() {
    return {
      dialog: false,
      text: "",
      snackbarText: "",
      snackbar: false,
    };
  },
  methods: {
    async send() {
      try {
        await axios.post(SEND_FEEDBACK_ENDPOINT, { feedback: this.text });
        this.snackbarText = "Thanks!";
      } catch (err) {
        const { status } = err.response;
        if (status == "400")
          this.snackbarText = "Your feedback is not useful 😔";
        else this.snackbarText = "Ups... Something went wrong";
      }
      this.snackbar = true;
    },
  },
};
</script>
