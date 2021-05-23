<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <span>CASAMENTO ETHEREUM</span>

      <v-spacer></v-spacer>

      <v-btn
        href="https://github.com/BiancaCristina/SMC-Contract/"
        target="_blank"
        text
      >
        <span class="mr-2">Código Fonte</span>
        <v-icon>mdi-open-in-new</v-icon>
      </v-btn>
    </v-app-bar>

    <v-main>
      <Choice />
    </v-main>
  </v-app>
</template>

<script>
import Choice from "./components/Choice";

export default {
  name: "App",

  components: {
    Choice, 
  },

  data: () => ({
    info: null
  })
};
</script>
