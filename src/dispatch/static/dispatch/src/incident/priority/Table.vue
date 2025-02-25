<template>
  <v-container fluid>
    <new-edit-sheet />
    <v-row no-gutters>
      <v-col>
        <v-alert dismissible icon="mdi-school" prominent text type="info">
          Priorities adds another dimension to Dispatch's incident categorization. They also allow
          for some configurability (e.g. only page a command for 'high' priority incidents).
        </v-alert>
      </v-col>
    </v-row>
    <v-row align="center" justify="space-between" no-gutters>
      <v-col cols="8">
        <settings-breadcrumbs v-model="project" />
      </v-col>
      <v-col class="text-right">
        <v-btn color="info" class="mr-2" @click="createEditShow()"> New </v-btn>
      </v-col>
    </v-row>
    <v-row no-gutters>
      <div class="text-body-1 ml-4 mt-3">Incident priority types</div>
    </v-row>
    <v-row no-gutters>
      <v-col>
        <v-card elevation="0">
          <v-card-title>
            <v-text-field
              v-model="q"
              append-icon="search"
              label="Search"
              single-line
              hide-details
              clearable
            />
          </v-card-title>
          <v-data-table
            :headers="headers"
            :items="items"
            :server-items-length="total"
            :page.sync="page"
            :items-per-page.sync="itemsPerPage"
            :sort-by.sync="sortBy"
            :sort-desc.sync="descending"
            :loading="loading"
            loading-text="Loading... Please wait"
          >
            <template #item.page_commander="{ item }">
              <v-simple-checkbox v-model="item.page_commander" disabled />
            </template>
            <template #item.default="{ item }">
              <v-simple-checkbox v-model="item.default" disabled />
            </template>
            <template #item.enabled="{ item }">
              <v-simple-checkbox v-model="item.enabled" disabled />
            </template>
            <template #item.data-table-actions="{ item }">
              <v-menu bottom left>
                <template #activator="{ on }">
                  <v-btn icon v-on="on">
                    <v-icon>mdi-dots-vertical</v-icon>
                  </v-btn>
                </template>
                <v-list>
                  <v-list-item @click="createEditShow(item)">
                    <v-list-item-title>View / Edit</v-list-item-title>
                  </v-list-item>
                </v-list>
              </v-menu>
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>
    <v-divider />
    <v-row no-gutters>
      <v-col>
        <div class="text-body-1 ml-4 mt-6">Incident priority settings</div>
        <v-row align="start" no-gutters>
          <v-col class="d-flex justify-start">
            <v-checkbox
              class="ml-10 mr-5"
              v-model="restrictStable"
              label="Restrict Stable status to this priority:"
              @change="updateStablePriority"
            />
            <v-tooltip max-width="500px" open-delay="50" bottom>
              <template #activator="{ on }">
                <v-icon v-on="on"> mdi-information </v-icon>
              </template>
              <span>
                If activated, Dispatch will automatically change Stable incidents to this priority.
                Also, users will not be permitted to change the priority on Stable incidents.
              </span>
            </v-tooltip>
            <span max-width="500px">
              <incident-priority-select
                class="ml-4"
                max-width="400px"
                v-model="stablePriority"
                :project="project[0]"
              />
            </span>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapFields } from "vuex-map-fields"
import { mapActions } from "vuex"

import NewEditSheet from "@/incident/priority/NewEditSheet.vue"
import SettingsBreadcrumbs from "@/components/SettingsBreadcrumbs.vue"
import IncidentPrioritySelect from "@/incident/priority/IncidentPrioritySelect.vue"

export default {
  name: "IncidentPriorityTable",

  components: {
    NewEditSheet,
    SettingsBreadcrumbs,
    IncidentPrioritySelect,
  },
  data() {
    return {
      headers: [
        { text: "Name", value: "name", sortable: true },
        { text: "Description", value: "description", sortable: false },
        { text: "Page Commander", value: "page_commander", sortable: true },
        { text: "Default", value: "default", sortable: true },
        { text: "Enabled", value: "enabled", sortable: true },
        { text: "Tactical Report Reminder", value: "tactical_report_reminder", sortable: true },
        { text: "Executive Report Reminder", value: "executive_report_reminder", sortable: true },
        { text: "View Order", value: "view_order", sortable: true },
        { text: "", value: "data-table-actions", sortable: false, align: "end" },
      ],
      restrictStable: false,
    }
  },

  computed: {
    ...mapFields("incident_priority", [
      "table.options.q",
      "table.options.page",
      "table.options.itemsPerPage",
      "table.options.sortBy",
      "table.options.descending",
      "table.options.filters.project",
      "table.loading",
      "table.rows.items",
      "table.rows.total",
      "stablePriority",
    ]),
    ...mapFields("route", ["query", "params"]),
  },

  created() {
    this.project = [{ name: this.query.project }]

    this.getAll()
    this.restrictStable = this.stablePriority != null

    this.$watch(
      (vm) => [vm.q, vm.itemsPerPage, vm.sortBy, vm.descending, vm.project],
      () => {
        this.page = 1
        this.$router.push({ query: { project: this.project[0].name } })
        this.getAll()
        this.restrictStable = this.stablePriority != null
      }
    )

    this.$watch(
      (vm) => [vm.stablePriority],
      () => {
        this.restrictStable = this.stablePriority != null
        this.updateStablePriority(this.restrictStable)
      }
    )
  },

  methods: {
    ...mapActions("incident_priority", [
      "getAll",
      "createEditShow",
      "removeShow",
      "updateStablePriority",
    ]),
  },
}
</script>
