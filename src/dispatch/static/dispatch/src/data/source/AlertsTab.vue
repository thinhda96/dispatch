<template>
  <v-container fluid>
    <v-row>
      <v-col>
        <v-card>
          <v-sheet color="primary">
            <v-sparkline
              :labels="labels"
              :value="value"
              color="white"
              line-width="1"
              height="50"
              padding="15"
            />
          </v-sheet>
          <v-card-text class="pt-0">
            <div class="text-h6 font-weight-light mb-2">Alert Volume</div>
            <v-data-table :headers="headers" :items="alerts" />
            <v-divider class="my-2" />
            <v-icon class="mr-2" small> mdi-clock </v-icon>
            <span class="text-caption grey--text font-weight-light">last alert 10min ago</span>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapFields } from "vuex-map-fields"

export default {
  name: "SourceAlertsTab",

  components: {},

  computed: {
    ...mapFields("source", ["selected.alerts", "selected.loading"]),
  },

  data() {
    return {
      labels: ["12am", "3am", "6am", "9am", "12pm", "3pm", "6pm", "9pm"],
      value: [200, 675, 410, 390, 310, 460, 250, 240],
      headers: [
        {
          text: "Name",
          align: "start",
          sortable: false,
          value: "name",
        },
        { text: "Description", value: "description" },
        { text: "Source", value: "originator" },
      ],
    }
  },
}
</script>
