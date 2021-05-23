<template>
  <v-container fill-height fluid>
    <v-row justify="space-around">
      <v-col cols="auto">
        <v-dialog transition="dialog-bottom-transition" max-width="600">
          <template v-slot:activator="{ on, attrs }">
            <v-btn color="primary" v-bind="attrs" v-on="on"
              >INICIAR PROCESSO DE CASAMENTO</v-btn
            >
          </template>
          <template v-slot:default="dialog">
            <v-card>
              <v-toolbar color="primary" dark
                >Iniciar processo de casamento</v-toolbar
              >
              <v-card-text>
                <v-checkbox label="União Estável" color="green"></v-checkbox>

                <v-checkbox
                  label="Dividir bens anteriores ao casamento"
                  color="green"
                ></v-checkbox>
              </v-card-text>

              <v-card-actions class="justify-center">
                <v-btn color="success" class="mr-4" @click="validate">
                  ACEITAR
                </v-btn>

                <v-btn color="error" class="mr-4" @click="dialog.value = false">
                  DESISTIR
                </v-btn>
              </v-card-actions>
            </v-card>
          </template>
        </v-dialog>
      </v-col>
    </v-row>

    <v-row justify="space-around">
      <v-col cols="auto">
        <v-dialog transition="dialog-bottom-transition" max-width="600">
          <template v-slot:activator="{ on, attrs }">
            <v-btn color="primary" v-bind="attrs" v-on="on"
              >CONTINUAR PROCESSO DE CASAMENTO</v-btn
            >
          </template>
          <template v-slot:default="dialog">
            <v-card>
              <v-toolbar color="primary" dark
                >Continuar Processo de Casamento</v-toolbar
              >
              <v-card-text>
                <v-text-field label="Endereço da conta do cônjuge"></v-text-field>

                <v-checkbox label="União Estável" color="green"></v-checkbox>

                <v-checkbox
                  label="Dividir bens anteriores ao casamento"
                  color="green"
                ></v-checkbox>
              </v-card-text>

              <v-card-actions class="justify-center">
                <v-btn color="success" class="mr-4" @click="validate">
                  ACEITAR
                </v-btn>

                <v-btn color="error" class="mr-4" @click="dialog.value = false">
                  DESISTIR
                </v-btn>
              </v-card-actions>
            </v-card>
          </template>
        </v-dialog>
      </v-col>
    </v-row>

    <v-row justify="space-around">
      <v-col cols="auto">
        <v-dialog transition="dialog-bottom-transition" max-width="600">
          <template v-slot:activator="{ on, attrs }">
            <v-btn color="primary" v-bind="attrs" v-on="on"
              >VERIFICAR CASAMENTO</v-btn
            >
          </template>
          <template v-slot:default="dialog">
            <v-card>
              <v-toolbar color="primary" dark
                >Continue Marriage Process</v-toolbar
              >
              <v-card-text>
                <v-text-field label="Endereço da conta de algum dos cônjuges"></v-text-field>
              </v-card-text>

              <v-card-actions class="justify-center">

                <v-btn color="error" class="mr-4" @click="dialog.value = false">
                  FECHAR
                </v-btn>
              </v-card-actions>
            </v-card>
          </template>
        </v-dialog>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "Choice",

  data: () => ({
    message: "ola",
    items: [
      { header: "Today" },
      {
        avatar: "https://cdn.vuetifyjs.com/images/lists/1.jpg",
        title: "Brunch this weekend?",
        subtitle: `<span class="font-weight-bold">Ali Connors</span> &mdash; I'll be in your neighborhood doing errands this weekend. Do you want to hang out?`,
      },
      { divider: true, inset: true },
      {
        avatar: "https://cdn.vuetifyjs.com/images/lists/2.jpg",
        title: 'Summer BBQ <span class="grey--text text--lighten-1">4</span>',
        subtitle: `<span class="font-weight-bold">to Alex, Scott, Jennifer</span> &mdash; Wish I could come, but I'm out of town this weekend.`,
      },
      { divider: true, inset: true },
      {
        avatar: "https://cdn.vuetifyjs.com/images/lists/3.jpg",
        title: "Oui oui",
        subtitle:
          '<span class="font-weight-bold">Sandra Adams</span> &mdash; Do you have Paris recommendations? Have you ever been?',
      },
    ],
  }),
};
</script>
