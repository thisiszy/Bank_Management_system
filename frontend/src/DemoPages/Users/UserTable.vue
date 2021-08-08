<template>
  <div>
    <page-title
      :heading="heading"
      :subheading="subheading"
      :icon="icon"
      @add="addclicked"
      @del="delclicked"
      @alter="alterclicked"
      leftbtn="Create User"
      midbtn="Alter User"
      rightbtn="Delete User"
      :btndefined="true"
    >
    </page-title>

    <div>
      <b-alert
        :show="dismissCountDown"
        dismissible
        fade
        variant="danger"
        @dismissed="dismissCountDown = 0"
        @dismiss-count-down="countDownChanged"
      >
        {{alertmsg}}
      </b-alert>
    </div>
    <div class="main-card mb-3 card">
      <div class="card-body">
        <h5 class="card-title">Search Users</h5>
        <div class="row">
          <div class="col-md-2">
            <b-input-group>
              <!-- <b-dropdown
                :text="dropdowntext"
                variant="info"
                slot="prepend"
                v-for="i in 1"
                :key="i"
              >
                <b-dropdown-item @click="chooseAll">All</b-dropdown-item>
                <b-dropdown-item @click="chooseID">By ID</b-dropdown-item>
                <b-dropdown-item @click="chooseAccount"
                  >By Account</b-dropdown-item
                >
              </b-dropdown> -->

              <b-form-group label="ID" label-for="ID-input">
                <b-form-input
                  id="SearchFormID"
                  type="search"
                  v-model.trim="SearchFormText.ID"
                ></b-form-input>
              </b-form-group>
              <!-- <div class="input-group-append">
                <button class="btn btn-success" @click="onsearch">
                  Search
                </button>
              </div> -->
            </b-input-group>
          </div>
          <div class="col-md-2">
            <b-input-group>
              <b-form-group label="Address" label-for="Address-input">
                <b-form-input
                  id="SearchFormAddress"
                  type="search"
                  v-model.trim="SearchFormText.Address"
                ></b-form-input>
              </b-form-group>
            </b-input-group>
          </div>
          <div class="col-md-2">
            <b-input-group>
              <b-form-group label="ContectName" label-for="ContectName-input">
                <b-form-input
                  id="ContectName"
                  type="search"
                  v-model.trim="SearchFormText.ContectName"
                ></b-form-input>
              </b-form-group>
            </b-input-group>
          </div>
          <div class="col-md-2">
            <b-input-group>
              <b-form-group label="ContectTel" label-for="ContectTel-input">
                <b-form-input
                  id="ContectTel"
                  type="search"
                  v-model.trim="SearchFormText.ContectTel"
                ></b-form-input>
              </b-form-group>
            </b-input-group>
          </div>
          <div class="col-md-2">
            <b-input-group>
              <b-form-group label="ContectEmail" label-for="ContectEmail-input">
                <b-form-input
                  id="ContectEmail"
                  type="search"
                  v-model.trim="SearchFormText.ContectEmail"
                ></b-form-input>
              </b-form-group>
            </b-input-group>
          </div>
          <div class="col-md-2">
            <b-input-group>
              <b-form-group label="Relationship" label-for="Relationship-input">
                <b-form-input
                  id="Relationship"
                  type="search"
                  v-model.trim="SearchFormText.Relationship"
                ></b-form-input>
              </b-form-group>
            </b-input-group>
          </div>
          <div class="col-md-2">
            <b-input-group>
              <b-form-group label="WorkerID" label-for="WorkerID-input">
                <b-form-input
                  id="WorkerID"
                  type="search"
                  v-model.trim="SearchFormText.WorkerID"
                ></b-form-input>
              </b-form-group>
            </b-input-group>
          </div>
          <div class="col-md-2">
            <div class="position-relative form-group">
              <label for="exampleCustomSelect" class="">Role</label
              ><select
                type="select"
                id="exampleCustomSelect"
                name="customSelect"
                class="custom-select"
                v-model="SearchFormText.Role"
              >
                <option value="">Select</option>
                <option>Loan Manager</option>
                <option>Account Manager</option>
              </select>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-md-6">
            <button class="btn btn-primary mr-3" @click="onsearch">
              Search
            </button>
            <button class="btn btn-danger" @click="onreset">Reset</button>
          </div>
        </div>
      </div>
    </div>
    <b-card title="Users" class="main-card mb-4">
      <b-table
        :striped="striped"
        :bordered="bordered"
        :outlined="outlined"
        :small="small"
        :hover="hover"
        :dark="dark"
        :fixed="fixed"
        :foot-clone="footClone"
        :items="items"
        :fields="fields"
        selectable
        select-mode="single"
        @row-selected="onRowSelected"
      >
      </b-table>
    </b-card>
    <b-modal
      id="adduser"
      size="lg"
      :title="modelTitleadd"
      :close-on-click-modal="false"
      @cancel="handleCancel"
      @ok="submitadd"
    >
      <form @submitadd.stop.prevent="submitadd">
        <b-form-group label="ID" label-for="id-input">
          <b-form-input
            id="id-input"
            v-model.trim="$v.addUserForm.ID.$model"
            type="text"
            :state="
              $v.addUserForm.ID.$anyDirty ? !$v.addUserForm.ID.$anyError : null
            "
          ></b-form-input>
          <div class="error" v-if="!$v.addUserForm.ID.required">
            ID is required
          </div>
          <div class="error" v-if="!$v.addUserForm.ID.minLength">
            ID must have
            {{ $v.addUserForm.ID.$params.minLength.min }} letters.
          </div>
          <div class="error" v-if="!$v.addUserForm.ID.maxLength">
            ID must have
            {{ $v.addUserForm.ID.$params.maxLength.max }} letters.
          </div>
        </b-form-group>
        <b-form-group label="Address" label-for="address-input">
          <b-form-input
            id="address-input"
            v-model.trim="$v.addUserForm.Address.$model"
            type="text"
            :state="
              $v.addUserForm.Address.$anyDirty
                ? !$v.addUserForm.Address.$anyError
                : null
            "
          ></b-form-input>
          <div class="error" v-if="!$v.addUserForm.Address.required">
            Address is required
          </div>
        </b-form-group>
        <b-form-group label="ContectName" label-for="ContectName-input">
          <b-form-input
            id="ContectName-input"
            v-model.trim="$v.addUserForm.ContectName.$model"
            type="text"
            :state="
              $v.addUserForm.ContectName.$anyDirty
                ? !$v.addUserForm.ContectName.$anyError
                : null
            "
          ></b-form-input>
          <div class="error" v-if="!$v.addUserForm.ContectName.required">
            ContectName is required
          </div>
        </b-form-group>
        <b-form-group label="ContectTel" label-for="ContectTel-input">
          <b-form-input
            id="ContectTel-input"
            v-model.trim="$v.addUserForm.ContectTel.$model"
            type="number"
            :state="
              $v.addUserForm.ContectTel.$anyDirty
                ? !$v.addUserForm.ContectTel.$anyError
                : null
            "
          ></b-form-input>
          <div class="error" v-if="!$v.addUserForm.ContectTel.required">
            ContectTel is required
          </div>
          <div class="error" v-if="!$v.addUserForm.ContectTel.validTel">
            ContectTel must be 8 or 11 digits.
          </div>
        </b-form-group>
        <b-form-group label="ContectEmail" label-for="ContectEmail-input">
          <b-form-input
            id="ContectEmail-input"
            v-model.trim="$v.addUserForm.ContectEmail.$model"
            type="email"
            :state="
              $v.addUserForm.ContectEmail.$anyDirty
                ? !$v.addUserForm.ContectEmail.$anyError
                : null
            "
          ></b-form-input>
          <div class="error" v-if="!$v.addUserForm.ContectEmail.required">
            ContectEmail is required
          </div>
          <div class="error" v-if="!$v.addUserForm.ContectEmail.email">
            Invalid Email
          </div>
        </b-form-group>
        <b-form-group label="Relationship" label-for="Relationship-input">
          <b-form-input
            id="Relationship-input"
            v-model.trim="$v.addUserForm.Relationship.$model"
            type="text"
            :state="
              $v.addUserForm.Relationship.$anyDirty
                ? !$v.addUserForm.Relationship.$anyError
                : null
            "
          ></b-form-input>
          <div class="error" v-if="!$v.addUserForm.Relationship.required">
            Relationship is required
          </div>
        </b-form-group>
        <b-form-group label="WorkerID" label-for="WorkerID-input">
          <b-form-input
            id="WorkerID-input"
            v-model.trim="$v.addUserForm.WorkerID.$model"
            type="text"
            :state="
              $v.addUserForm.WorkerID.$anyDirty
                ? !$v.addUserForm.WorkerID.$anyError
                : null
            "
          ></b-form-input>
          <div class="error" v-if="!$v.addUserForm.WorkerID.required">
            WorkerID is required
          </div>
        </b-form-group>
        <label for="exampleCustomSelect" class="">Role</label
        ><select
          type="select"
          id="exampleCustomSelect"
          name="customSelect"
          class="custom-select"
          v-model.trim="$v.addUserForm.Role.$model"
        >
          <option value="">Select</option>
          <option>Loan Manager</option>
          <option>Account Manager</option>
        </select>
        <div class="error" v-if="!$v.addUserForm.Role.required">
          Role is required
        </div>
      </form>
    </b-modal>
    <b-modal
      id="deluser"
      :title="modelTitledel"
      :close-on-click-modal="false"
      @ok="delconfirm"
    >
      <p class="my-4" v-text="selectedID"></p>
    </b-modal>
  </div>
</template>

<script>
import { library } from "@fortawesome/fontawesome-svg-core";
import PageTitle from "../../Layout/Components/PageTitle.vue";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { faStar, faPlus } from "@fortawesome/free-solid-svg-icons";
import {
  required,
  minLength,
  maxLength,
  numeric,
  email,
} from "vuelidate/lib/validators";
import axios from "axios";
const validTel = (value) => (value.length == 11) | (value.length == 8);

library.add(faStar, faPlus);
export default {
  components: {
    PageTitle,
    "font-awesome-icon": FontAwesomeIcon,
  },
  data: () => ({
    heading: "Users",
    subheading: "You can add delete alter search users here.",
    icon: "pe-7s-add-user icon-gradient bg-happy-itmeo",

    fields: [
      "ID",
      "Address",
      "ContectName",
      "ContectTel",
      "ContectEmail",
      "Relationship",
      "WorkerID",
      "Role",
    ],
    items: [],
    striped: false,
    bordered: false,
    outlined: false,
    small: false,
    hover: false,
    dark: false,
    fixed: false,
    footClone: false,

    visible: false,
    //模态对话框标题
    modelTitleadd: "New User",
    submitStatusAdd: null,
    addUserForm: {
      ID: "",
      Address: "",
      ContectName: "",
      ContectTel: "",
      ContectEmail: "",
      Relationship: "",
      WorkerID: "",
      Role: "",
    },

    modelTitledel: "Are you sure to delete?",
    submitStatusDel: null,
    delUserForm: {
      ID: "",
    },
    selected: [],
    isAlter: null,
    dropdowntext: "All",
    // dropdownstatus: 0,
    SearchFormText: {
      ID: "",
      Address: "",
      ContectName: "",
      ContectTel: "",
      ContectEmail: "",
      Relationship: "",
      WorkerID: "",
      Role: "",
    },
    selectedID: "",
    dismissSecs: 3,
    dismissCountDown: 0,
    alertmsg: "",
  }),

  validations: {
    addUserForm: {
      ID: {
        required,
        minLength: minLength(18),
        maxLength: maxLength(18),
      },
      Address: {
        required,
      },
      ContectName: {
        required,
      },
      ContectTel: {
        required,
        validTel,
        numeric,
      },
      ContectEmail: {
        email,
        required,
      },
      Relationship: {
        required,
      },
      WorkerID: {
        required,
      },
      Role: {
        required,
      },
    },
    delUserForm: {
      ID: {
        required,
        minLength: minLength(18),
        maxLength: maxLength(18),
      },
    },
    SearchFormText: {
      required,
    },
  },
  created() {
    this.getUsers();
  },
  methods: {
    // chooseAll() {
    //   this.dropdowntext = "All";
    //   this.dropdownstatus = 0;
    // },
    // chooseID() {
    //   this.dropdowntext = "By ID";
    //   this.dropdownstatus = 1;
    // },
    // chooseAccount() {
    //   this.dropdowntext = "By Account";
    //   this.dropdownstatus = 2;
    // },
    addclicked() {
      this.isAlter = 0;
      this.$bvModal.show("adduser");
    },
    onsearch() {
      this.getUsers();
    },
    onreset() {
      this.SearchFormText.ID = "";
      this.SearchFormText.Address = "";
      this.SearchFormText.ContectName = "";
      this.SearchFormText.ContectTel = "";
      this.SearchFormText.ContectEmail = "";
      this.SearchFormText.Relationship = "";
      this.SearchFormText.WorkerID = "";
      this.SearchFormText.Role = "";
    },

    getUsers() {
      const path = "http://localhost:5000/user";
      axios
        .get(path, {
          params: {
            ID: this.SearchFormText.ID,
            Address: this.SearchFormText.Address,
            ContectName: this.SearchFormText.ContectName,
            ContectTel: this.SearchFormText.ContectTel,
            ContectEmail: this.SearchFormText.ContectEmail,
            Relationship: this.SearchFormText.Relationship,
            WorkerID: this.SearchFormText.WorkerID,
            Role:
              this.SearchFormText.Role == "Loan Manager"
                ? "1"
                : this.SearchFormText.Role == "Account Manager"
                ? "0"
                : "",
          },
        })
        .then((res) => {
          this.items = res.data.users;
          for (var item of this.items) {
            item["Role"] =
              item.Role == "1"
                ? "Loan Manager"
                : item.Role == "0"
                ? "Account Manager"
                : "";
          }
        })
        .catch((error) => {
          // eslint-disable-next-line
          this.errorHandle(error);
          window.console.error(error);
        });
    },
    delclicked() {
      if (typeof this.selected[0] != "undefined") {
        // this.$bvModal.show("deluser");
        // window.console.log(this.selected[0].ID);
        this.selectedID = "ID: " + this.selected[0].ID + "?";
        this.$bvModal.show("deluser");
      }
    },
    alterclicked() {
      if (typeof this.selected[0] != "undefined") {
        this.addUserForm.ID = this.selected[0].ID;
        this.addUserForm.Address = this.selected[0].Address;
        this.addUserForm.ContectName = this.selected[0].ContectName;
        this.addUserForm.ContectTel = this.selected[0].ContectTel;
        this.addUserForm.ContectEmail = this.selected[0].ContectEmail;
        this.addUserForm.Relationship = this.selected[0].Relationship;
        this.addUserForm.WorkerID = this.selected[0].WorkerID;
        this.addUserForm.Role = this.selected[0].Role;
        this.isAlter = 1;
        this.$bvModal.show("adduser");
      }
    },
    initForm() {
      this.addUserForm.ID = "";
      this.addUserForm.Address = "";
      this.addUserForm.ContectName = "";
      this.addUserForm.ContectTel = "";
      this.addUserForm.ContectEmail = "";
      this.addUserForm.Relationship = "";
      this.addUserForm.WorkerID = "";
      this.addUserForm.Role = "";
    },
    //关闭模态框
    handleCancel() {
      this.initForm();
      this.$bvModal.hide("adduser");
    },
    submitadd(bvModalEvt) {
      bvModalEvt.preventDefault();
      this.$v.$touch();
      if (!this.$v.addUserForm.$invalid) {
        const payload = {
          ID: this.addUserForm.ID,
          Address: this.addUserForm.Address,
          ContectName: this.addUserForm.ContectName,
          ContectTel: this.addUserForm.ContectTel,
          ContectEmail: this.addUserForm.ContectEmail,
          Relationship: this.addUserForm.Relationship,
          WorkerID: this.addUserForm.WorkerID,
          Role: this.addUserForm.Role == "Loan Manager" ? "1" : "0",
        };
        if (this.isAlter) {
          this.alterUser(payload);
        } else {
          this.addUser(payload);
        }
        // do your submit logic here
        this.submitStatusAdd = "PENDING";
        setTimeout(() => {
          this.submitStatusAdd = "OK";
        }, 500);
        this.initForm();
        this.$nextTick(() => {
          this.$bvModal.hide("adduser");
        }, 2500);
      }
    },
    addUser(payload) {
      const path = "http://localhost:5000/user";
      axios
        .post(path, payload)
        .then(() => {
          this.onreset();
          this.getUsers();
        })
        .catch((error) => {
          // eslint-disable-next-line
          window.console.log(error);
          this.errorHandle(error);
          this.onreset();
          this.getUsers();
        });
    },
    alterUser(payload) {
      const path = "http://localhost:5000/alteruser";
      axios
        .post(path, payload)
        .then(() => {
          this.onreset();
          this.getUsers();
        })
        .catch((error) => {
          // eslint-disable-next-line
          this.errorHandle(error);
          window.console.log(error);
          this.onreset();
          this.getUsers();
        });
    },
    delconfirm(bvModalEvt) {
      bvModalEvt.preventDefault();
      this.$v.$touch();
      const payload = {
        ID: this.selected[0].ID,
      };
      this.delUser(payload);
      this.submitStatusDel = "PENDING";
      setTimeout(() => {
        this.submitStatusDel = "OK";
      }, 500);
      this.initForm();
      this.$nextTick(() => {
        this.$bvModal.hide("deluser");
      }, 2500);
    },
    delUser(payload) {
      const path = "http://localhost:5000/deluser";
      axios
        .post(path, payload)
        .then(() => {
          this.onreset();
          this.getUsers();
        })
        .catch((error) => {
          window.console.log(error);
          this.errorHandle(error);
          this.onreset();
          this.getUsers();
        });
    },
    onRowSelected(item) {
      this.selected = item;
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
};
</script>
