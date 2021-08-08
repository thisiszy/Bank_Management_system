<template>
  <div>
    <page-title
      :heading="heading"
      :subheading="subheading"
      :icon="icon"
    ></page-title>

    <div>
      <b-alert
        :show="dismissCountDown"
        dismissible
        fade
        variant="danger"
        @dismissed="dismissCountDown = 0"
        @dismiss-count-down="countDownChanged"
      >
        {{ alertmsg }}
      </b-alert>
    </div>
    <div class="row">
      <div class="col-md-6">
        <div class="main-card mb-3 card">
          <div class="card-body">
            <h5 class="card-title">Select Subbranch to view</h5>
            <b-dropdown
              no-flip
              :text="dropdowntext"
              class="mb-2 mr-2"
              variant="outline-primary"
              :size="'lg'"
              slot="prepend"
            >
              <b-dropdown-item @click="selectsub('All', '0')">
                All
              </b-dropdown-item>
              <template v-for="sub in subbranchList">
                <b-dropdown-item
                  :key="sub.id"
                  @click="selectsub(sub.name, sub.id)"
                  >{{ sub.name }}</b-dropdown-item
                >
              </template>
            </b-dropdown>
          </div>
        </div>
      </div>
      <div class="col-md-6">
        <div class="main-card mb-3 card">
          <div class="card-body">
            <template>
              <div>
                <label for="start-input">Choose start date</label>
                <b-input-group class="mb-3">
                  <b-form-input
                    id="start-input"
                    v-model="startvalue"
                    type="text"
                    placeholder="YYYY-MM-DD"
                    autocomplete="off"
                    disabled
                  ></b-form-input>
                  <b-input-group-append>
                    <b-form-datepicker
                      v-model="startvalue"
                      button-only
                      right
                      aria-controls="start-input"
                      @context="onContext"
                    ></b-form-datepicker>
                  </b-input-group-append>
                </b-input-group>
              </div>
              <div>
                <label for="end-input">Choose end date</label>
                <b-input-group class="mb-3">
                  <b-form-input
                    id="end-input"
                    v-model="endvalue"
                    type="text"
                    placeholder="YYYY-MM-DD"
                    autocomplete="off"
                    disabled
                  ></b-form-input>
                  <b-input-group-append>
                    <b-form-datepicker
                      v-model="endvalue"
                      button-only
                      right
                      aria-controls="end-input"
                      @context="onContext"
                    ></b-form-datepicker>
                  </b-input-group-append>
                </b-input-group>
              </div>
            </template>
            <button class="btn btn-success" @click="onsearch">Search</button>
          </div>
        </div>
      </div>
    </div>

    <div class="row">
      <div class="col-sm-12 col-lg-12">
        <div class="card-hover-shadow-2x mb-3 card">
          <div class="card-header-tab card-header">
            <div
              class="
                card-header-title
                font-size-lg
                text-capitalize
                font-weight-normal
              "
            >
              <i class="header-icon lnr-laptop-phone mr-3 text-muted opacity-6">
              </i>
              Statistic
            </div>
          </div>
          <div class="card-body">
            <b-table striped hover :items="items" :fields="fields"></b-table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import PageTitle from "../../Layout/Components/PageTitle.vue";

import { library } from "@fortawesome/fontawesome-svg-core";
import {
  faTrashAlt,
  faCheck,
  faCalendarAlt,
  faAngleDown,
  faAngleUp,
  faTh,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import axios from "axios";

library.add(faTrashAlt, faCheck, faAngleDown, faAngleUp, faTh, faCalendarAlt);

export default {
  components: {
    PageTitle,
    "font-awesome-icon": FontAwesomeIcon,
  },
  data: () => ({
    heading: "Analytics",
    subheading: "View each subbranch statistic.",
    icon: "pe-7s-graph1 icon-gradient bg-tempting-azure",
    items: [],
    fields: [
      "Subbranch",
      "Assets",
      "SavingAccountNum",
      "SavingAssets",
      "CheckingAccountNum",
      "CheckingAssets",
      "LoanAssets",
    ],
    dropdowntext: "Select Subbranch",
    dropdownstatus: "0",
    subbranchList: [],
    startvalue: "",
    endvalue: "",
    formatted: "",
    selected: "",
    dismissSecs: 3,
    dismissCountDown: 0,
    alertmsg: "",
  }),

  methods: {
    selectsub(name, num) {
      this.dropdowntext = name;
      this.dropdownstatus = toString(num);
    },
    getSub() {
      const path = "http://localhost:5000/subbranch";
      axios
        .get(path, {
          params: {
            type: this.dropdownstatus,
            content: this.dropdowntext,
            start: this.startvalue,
            end: this.endvalue,
          },
        })
        .then((res) => {
          this.items = res.data.sub;
        })
        .catch((error) => {
          // eslint-disable-next-line
          this.errorHandle(error);
          window.console.error(error);
        });
    },
    onContext(ctx) {
      // The date formatted in the locale, or the `label-no-date-selected` string
      this.formatted = ctx.selectedFormatted;
      // The following will be an empty string until a valid date is entered
      this.selected = ctx.selectedYMD;
    },
    onsearch() {
      var starttime = new Date(this.startvalue);
      var endtime = new Date(this.endvalue);
      if (
        starttime < endtime ||
        (this.startvalue == "" && this.endvalue == "")
      ) {
        this.getSub();
      }
    },
    getStatistic() {
      const path = "http://localhost:5000/subbranch";
      axios
        .get(path, {
          params: {
            type: this.dropdownstatus,
            content: this.dropdowntext,
            start: this.startvalue,
            end: this.endvalue,
          },
        })
        .then((res) => {
          this.items = res.data.sub;
        })
        .catch((error) => {
          // eslint-disable-next-line
          this.errorHandle(error);
          window.console.error(error);
        });
    },
    countDownChanged(dismissCountDown) {
      this.dismissCountDown = dismissCountDown;
    },
    showAlert(msg) {
      this.dismissCountDown = this.dismissSecs;
      this.alertmsg = msg;
    },
    errorHandle(err) {
      window.console.log(err.response.data.msg);
      this.showAlert(err.response.data.msg);
    },
  },
  created() {
    const path = "http://localhost:5000/sublist";
    axios
      .get(path)
      .then((res) => {
        this.subbranchList = res.data.subbranch;
      })
      .catch((error) => {
        // eslint-disable-next-line
        this.errorHandle(error);
        window.console.error(error);
      });
    this.getSub();
  },
};
</script>
