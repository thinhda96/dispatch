<template>
  <v-app-bar
    clipped-left
    clipped-right
    app
    flat
    style="border-bottom: 1px solid #d2d2d2 !important"
    color="background0"
  >
    <organization-create-edit-dialog />
    <!--<v-app-bar-nav-icon @click="handleDrawerToggle" />-->
    <router-link :to="{ name: 'IncidentOverview' }" style="text-decoration: none">
      <span class="button font-weight-bold">D I S P A T C H</span>
    </router-link>
    <v-spacer />
    <v-text-field
      v-model="queryString"
      hide-details
      prepend-inner-icon="search"
      label="Search"
      clearable
      solo-inverted
      flat
      @keyup.enter="performSearch()"
    />
    <v-spacer />
    <v-toolbar-items>
      <v-tooltip v-if="!$vuetify.theme.dark" bottom>
        <template #activator="{ on }">
          <v-btn v-on="on" small icon @click="toggleDarkTheme">
            <v-icon class="mr-1"> mdi-moon-waxing-crescent </v-icon>
          </v-btn>
        </template>
        <span>Dark Mode On</span>
      </v-tooltip>
      <v-tooltip v-else bottom>
        <template #activator="{ on }">
          <v-btn v-on="on" small icon @click="toggleDarkTheme">
            <v-icon>mdi-white-balance-sunny</v-icon>
          </v-btn>
        </template>
        <span>Dark Mode Off</span>
      </v-tooltip>
      <v-menu offset-y>
        <template #activator="{ on, attrs }">
          <v-btn icon v-bind="attrs" v-on="on">
            <v-icon>help_outline</v-icon>
          </v-btn>
        </template>
        <v-list dense>
          <v-list-item href="/api/v1/docs" target="_blank">
            <v-list-item-title>API Documentation</v-list-item-title>
            <v-list-item-action>
              <v-list-item-icon>
                <v-icon small>open_in_new</v-icon>
              </v-list-item-icon>
            </v-list-item-action>
          </v-list-item>
          <v-list-item href="https://netflix.github.io/dispatch/" target="_blank">
            <v-list-item-title>App Documentation</v-list-item-title>
            <v-list-item-action>
              <v-list-item-icon>
                <v-icon small>open_in_new</v-icon>
              </v-list-item-icon>
            </v-list-item-action>
          </v-list-item>
          <v-list-item v-if="currentVersion()" @click="showCommitMessage">
            <v-list-item-title>
              Current version: {{ currentVersion() | formatHash }}
            </v-list-item-title>
            <v-list-item-action>
              <v-list-item-icon>
                <v-icon small>read_more</v-icon>
              </v-list-item-icon>
            </v-list-item-action>
          </v-list-item>
        </v-list>
      </v-menu>
      <v-menu offset-y>
        <template #activator="{ on }">
          <v-btn icon large text v-on="on">
            <v-avatar size="30px" v-if="userAvatarUrl(currentUser())">
              <v-img :src="userAvatarUrl(currentUser())" />
            </v-avatar>
            <v-avatar size="30px" v-else>
              <v-icon> account_circle </v-icon>
            </v-avatar>
          </v-btn>
        </template>
        <v-card width="400">
          <v-list>
            <v-list-item class="px-2">
              <v-list-item-avatar v-if="userAvatarUrl(currentUser())">
                <v-img :src="userAvatarUrl(currentUser())" />
              </v-list-item-avatar>
              <v-list-item-avatar v-else>
                <v-icon size="30px"> account_circle </v-icon>
              </v-list-item-avatar>
              <v-list-item-content>
                <v-list-item-title class="title">
                  {{ currentUser().name || currentUser().email }}
                </v-list-item-title>
                <v-list-item-subtitle> {{ currentUser().email }} </v-list-item-subtitle>
              </v-list-item-content>
              <v-list-item-action>
                <v-tooltip bottom>
                  <template #activator="{ on }">
                    <v-btn icon v-on="on" @click="logout()"><v-icon>logout</v-icon></v-btn>
                  </template>
                  <span>Logout</span>
                </v-tooltip>
              </v-list-item-action>
            </v-list-item>
            <v-divider />
            <v-subheader>Experimental Features</v-subheader>
            <v-switch
              v-model="currentUser().experimental_features"
              inset
              class="ml-5"
              color="blue"
              @change="updateExperimentalFeatures()"
              :label="currentUser().experimental_features ? 'Enabled' : 'Disabled'"
            />
            <v-divider />
            <v-subheader>Organizations</v-subheader>
            <v-list-item v-for="(item, i) in organizations" :key="i">
              <v-list-item-content>
                <v-list-item-title>{{ item.name }}</v-list-item-title>
                <v-list-item-subtitle>{{ item.description }}</v-list-item-subtitle>
              </v-list-item-content>
              <v-list-item-action>
                <v-tooltip bottom>
                  <template #activator="{ on }">
                    <v-btn icon v-on="on" @click="showCreateEditDialog(item)">
                      <v-icon>mdi-pencil-outline</v-icon>
                    </v-btn>
                  </template>
                  <span>Edit Organization</span>
                </v-tooltip>
              </v-list-item-action>
              <v-list-item-action>
                <v-tooltip bottom>
                  <template #activator="{ on }">
                    <v-btn @click="switchOrganizations(item.slug)" icon v-on="on">
                      <v-icon>mdi-swap-horizontal</v-icon>
                    </v-btn>
                  </template>
                  <span>Switch Organization</span>
                </v-tooltip>
              </v-list-item-action>
            </v-list-item>
          </v-list>
          <v-list-item @click="showCreateEditDialog()">
            <v-list-item-avatar>
              <v-icon size="30px">mdi-plus</v-icon>
            </v-list-item-avatar>
            <v-list-item-content>
              <v-list-item-title>Create a new organization</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-card>
      </v-menu>
    </v-toolbar-items>
  </v-app-bar>
</template>
<script>
import { mapActions, mapGetters, mapMutations, mapState } from "vuex"

import Util from "@/util"
import OrganizationApi from "@/organization/api"
import OrganizationCreateEditDialog from "@/organization/CreateEditDialog.vue"
import UserApi from "@/auth/api"

export default {
  name: "AppToolbar",
  data: () => ({
    organizations: [],
    query: "",
  }),
  components: {
    OrganizationCreateEditDialog,
  },
  computed: {
    queryString: {
      set(query) {
        this.$store.dispatch("search/setQuery", query)
        this.query = query
      },
      get() {
        return this.$store.state.query.q
      },
    },
  },
  methods: {
    updateExperimentalFeatures() {
      UserApi.getUserInfo()
        .then((response) => {
          let userId = response.data.id
          let newUserExperimentalFeatures = this.currentUser().experimental_features
          UserApi.update(userId, {
            id: userId,
            experimental_features: newUserExperimentalFeatures,
          })
        })
        .catch((error) => {
          console.error("Error occurred while updating experimental features: ", error)
        })
    },
    handleDrawerToggle() {
      this.$store.dispatch("app/toggleDrawer")
    },
    handleFullScreen() {
      Util.toggleFullScreen()
    },
    performSearch() {
      let query = this.query
      this.$store.dispatch("search/getResults", this.$store.state.query)
      this.$router.push({ name: "ResultList", query: { q: query } })
    },
    toggleDarkTheme() {
      this.$vuetify.theme.dark = !this.$vuetify.theme.dark
      localStorage.setItem("dark_theme", this.$vuetify.theme.dark.toString())
    },
    switchOrganizations(slug) {
      this.$router.push({ params: { organization: slug } }).then(() => {
        this.$router.go()
      })
    },
    ...mapState("auth", ["currentUser"]),
    ...mapState("app", ["currentVersion"]),
    ...mapActions("auth", ["logout", "getExperimentalFeatures"]),
    ...mapActions("search", ["setQuery"]),
    ...mapActions("organization", ["showCreateEditDialog"]),
    ...mapActions("app", ["showCommitMessage"]),
    ...mapMutations("search", ["SET_QUERY"]),
    ...mapGetters("auth", ["userAvatarUrl"]),
  },

  created() {
    this.error = null
    this.loading = "error"
    let filterOptions = {
      itemsPerPage: 50,
      sortBy: ["name"],
      descending: [false],
    }

    let theme = localStorage.getItem("dark_theme")
    if (theme) {
      if (theme === "true") {
        this.$vuetify.theme.dark = true
      } else {
        this.$vuetify.theme.dark = false
      }
    }

    OrganizationApi.getAll(filterOptions).then((response) => {
      this.organizations = response.data.items
      this.loading = false
    })

    this.getExperimentalFeatures()
  },
}
</script>
