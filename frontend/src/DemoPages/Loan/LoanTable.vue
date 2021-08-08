<template>
  <div>
    <page-title
      :heading="heading"
      :subheading="subheading"
      :icon="icon"
      @add="addclicked"
      @del="delclicked"
      @alter="alterclicked"
      leftbtn="Create Loan"
      midbtn="Grant Loan"
      rightbtn="Delete Loan"
      :btndefined="true"
    >
      <!-- <template #extbtn>
        <button
          type="button"
          class="btn-shadow mr-3 btn btn-danger"
          v-b-modal.deluser
        >
          Delete User
        </button>
      </template> -->
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
        <h5 class="card-title">Search Loans</h5>
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
            <b-dropdown-item @click="chooseID"
              >By Account Subbranch</b-dropdown-item
            >
            <b-dropdown-item @click="chooseAccount">By User ID</b-dropdown-item>
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
              <b-form-group label="LoanNum" label-for="LoanNum-input">
                <b-form-input
                  id="SearchFormAddress"
                  type="number"
                  v-model.trim="SearchFormText.LoanNum"
                ></b-form-input>
              </b-form-group>
            </b-input-group>
          </div>
          <div class="col-md-2">
            <b-input-group>
              <b-form-group label="SubName" label-for="SubName-input">
                <b-form-input
                  id="SubName"
                  type="search"
                  v-model.trim="SearchFormText.SubName"
                ></b-form-input>
              </b-form-group>
            </b-input-group>
          </div>
          <div class="col-md-2">
            <b-input-group>
              <b-form-group label="MinBudget" label-for="MinBudget-input">
                <b-form-input
                  id="SearchFormAddress"
                  type="number"
                  v-model.trim="SearchFormText.MinBudget"
                ></b-form-input>
              </b-form-group>
            </b-input-group>
          </div>
          <div class="col-md-2">
            <b-input-group>
              <b-form-group label="MaxBudget" label-for="MaxBudget-input">
                <b-form-input
                  id="MaxBudget"
                  type="number"
                  v-model.trim="SearchFormText.MaxBudget"
                ></b-form-input>
              </b-form-group>
            </b-input-group>
          </div>
          <div class="col-md-2">
            <div class="position-relative form-group">
              <label for="exampleCustomSelect" class="">Status</label
              ><select
                type="select"
                id="exampleCustomSelect"
                name="customSelect"
                class="custom-select"
                v-model="SearchFormText.Status"
              >
                <option value="">Select</option>
                <option>IDLE</option>
                <option>ING</option>
                <option>DONE</option>
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
        <!-- <b-input-group>
          <b-dropdown
            :text="dropdowntext"
            variant="info"
            slot="prepend"
            v-for="i in 1"
            :key="i"
          >
            <b-dropdown-item @click="chooseAll">All</b-dropdown-item>
            <b-dropdown-item @click="chooseID">By User ID</b-dropdown-item>
            <b-dropdown-item @click="chooseAccount"
              >By Loan Number</b-dropdown-item
            >
          </b-dropdown>

          <b-form-input
            id="SearchForm"
            type="search"
            v-model.trim="$v.SearchFormText.$model"
          ></b-form-input>

          <div class="input-group-append">
            <button class="btn btn-success" @click="onsearch">Search</button>
          </div>
        </b-input-group> -->
      </div>
    </div>
    <b-card title="Loans" class="main-card mb-4">
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
        <b-form-group label="LoanNum" label-for="LoanNum-input">
          <b-form-input
            id="LoanNum-input"
            v-model.trim="$v.addUserForm.LoanNum.$model"
            type="number"
            :state="
              $v.addUserForm.LoanNum.$anyDirty
                ? !$v.addUserForm.LoanNum.$anyError
                : null
            "
          ></b-form-input>
          <div class="error" v-if="!$v.addUserForm.LoanNum.required">
            LoanNum is required
          </div>
        </b-form-group>
        <b-form-group label="Budget" label-for="Budget-input">
          <b-form-input
            id="Budget-input"
            v-model.trim="$v.addUserForm.Budget.$model"
            type="number"
            :state="
              $v.addUserForm.Budget.$anyDirty
                ? !$v.addUserForm.Budget.$anyError
                : null
            "
          ></b-form-input>
          <div class="error" v-if="!$v.addUserForm.Budget.required">
            Budget is required
          </div>
        </b-form-group>
        <b-form-group label="SubName" label-for="SubName-input">
          <b-form-input
            id="SubName-input"
            v-model.trim="$v.addUserForm.SubName.$model"
            type="text"
            :state="
              $v.addUserForm.SubName.$anyDirty
                ? !$v.addUserForm.SubName.$anyError
                : null
            "
          ></b-form-input>
          <div class="error" v-if="!$v.addUserForm.SubName.required">
            SubName is required
          </div>
        </b-form-group>
      </form>
      <div>
        <div v-for="(v, index) in $v.idlist.$each.$iter" :key="index">
          <label class="form__label">User {{ index }}</label>
          <b-form-group label-for="id-input">
            <b-form-input
              id="id-input"
              v-model.trim="v.ID.$model"
              type="text"
              :state="v.ID.$anyDirty ? !v.ID.$anyError : null"
            ></b-form-input>
            <div class="error" v-if="!v.ID.required">ID is required</div>
            <div class="error" v-if="!v.ID.minLength">
              ID must have
              {{ v.ID.$params.minLength.min }} letters.
            </div>
            <div class="error" v-if="!v.ID.maxLength">
              ID must have
              {{ v.ID.$params.maxLength.max }} letters.
            </div>
          </b-form-group>
        </div>
        <div>
          <!-- <button class="button" @click="idlist.push({ ID: '' })">Add</button>
          <button class="button" @click="idlist.pop()">Remove</button> -->
          <button
            type="button"
            class="
              btn-shadow
              mr-3
              d-inline-flex
              align-items-center
              btn btn-success
            "
            @click="idlist.push({ ID: '' })"
          >
            <font-awesome-icon class="mr-2" icon="plus" />
            Add New User
          </button>
        </div>
      </div>
    </b-modal>




    <b-modal
      id="grantloan"
      size="lg"
      :title="modelTitleAlter"
      :close-on-click-modal="false"
      @cancel="handleCancel"
      @ok="submitalter"
    >
    <!-- PayNum, LoanNum, PayDate, Amount -->
      <form @submitalter.stop.prevent="submitalter">
        <b-form-group label="Pay Number" label-for="PayNum-input">
          <b-form-input
            id="PayNum-input"
            v-model.trim="$v.GrantForm.PayNum.$model"
            type="number"
            :state="
              $v.GrantForm.PayNum.$anyDirty
                ? !$v.GrantForm.PayNum.$anyError
                : null
            "
          ></b-form-input>
          <div class="error" v-if="!$v.GrantForm.PayNum.required">
            Pay Number is required
          </div>
        </b-form-group>
        <b-form-group label="Loan Number" label-for="LoanNum-input">
          <b-form-input
            id="LoanNum-input"
            v-model.trim="$v.GrantForm.LoanNum.$model"
            type="number"
            :state="
              $v.GrantForm.LoanNum.$anyDirty
                ? !$v.GrantForm.LoanNum.$anyError
                : null
            "
          ></b-form-input>
          <div class="error" v-if="!$v.GrantForm.LoanNum.required">
            Loan Number is required
          </div>
        </b-form-group>
        <b-form-group label="PayDate" label-for="PayDate-input">
          <b-form-input
            id="PayDate-input"
            v-model.trim="$v.GrantForm.PayDate.$model"
            type="date"
            :state="
              $v.GrantForm.PayDate.$anyDirty
                ? !$v.GrantForm.PayDate.$anyError
                : null
            "
          ></b-form-input>
          <div
            class="error"
            v-if="!$v.GrantForm.PayDate.required"
          >
            Pay Date is required
          </div>
        </b-form-group>
        <b-form-group
          label="Amount"
          label-for="Amount-input"
        >
          <b-form-input
            id="Amount-input"
            v-model.trim="$v.GrantForm.Amount.$model"
            type="number"
            :state="
              $v.GrantForm.Amount.$anyDirty
                ? !$v.GrantForm.Amount.$anyError
                : null
            "
          ></b-form-input>
          <div
            class="error"
            v-if="!$v.GrantForm.Amount.required"
          >
            Amount is required
          </div>
        </b-form-group>
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
} from "vuelidate/lib/validators";
import axios from "axios";

library.add(faStar, faPlus);
export default {
  components: {
    PageTitle,
    "font-awesome-icon": FontAwesomeIcon,
  },
  data: () => ({
    heading: "Loans",
    subheading: "You can add delete grant search loans here.",
    icon: "pe-7s-wallet icon-gradient bg-happy-itmeo",

    fields: [
      "LoanNum",
      // "ID",
      "SubName",
      "Budget",
      "Paied",
      "Status",
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
    modelTitleadd: "New Loan",
    submitStatusAdd: null,
    addUserForm: {
      // ID: "",
      LoanNum: "",
      Budget: "",
      SubName: "",
      Paied: "",
      Status: "",
    },
    GrantForm: {
      PayNum: "",
      LoanNum: "", 
      PayDate: "", 
      Amount: "", 
    },
    modelTitledel: "Are you sure to delete?",
    submitStatusDel: null,
    modelTitleAlter: "Grant Loan",
    delUserForm: {
      ID: "",
    },
    selected: [],
    dropdowntext: "All",
    // dropdownstatus: 0,
    SearchFormText: {
      ID: "",
      LoanNum: "",
      SubName: "",
      MinBudget: "",
      MaxBudget: "",
      Status: "",
    },
    selectedID: "",
    idlist: [
      {
        ID: "",
      },
    ],
    dismissSecs: 3,
    dismissCountDown: 0,
    alertmsg: "",
  }),

  validations: {
    idlist: {
      required,
      minLength: minLength(3),
      $each: {
        ID: {
          required,
          minLength: minLength(18),
          maxLength: maxLength(18),
        },
      },
    },
    addUserForm: {
      // ID: {
      //   required,
      //   minLength: minLength(18),
      //   maxLength: maxLength(18),
      // },
      LoanNum: {
        required,
        numeric,
      },
      Budget: {
        required,
        numeric,
      },
      SubName: {
        required,
      },
      // ContectEmail: {
      //   email,
      //   required,
      // },
      // Relationship: {
      //   required,
      // },
    },
    SearchFormText: {
      required,
    },
    GrantForm: {
      PayNum: {
        required,
        numeric,
      },
      LoanNum: {
        required,
        numeric,
        
      },
      PayDate: {
        required
        
      },
      Amount: {
        required,
        numeric,
      },
    },
  },
  created() {
    this.getUsers();
  },
  methods: {
    addclicked() {
      this.$bvModal.show("adduser");
    },
    onsearch() {
      this.getUsers();
    },
    onreset() {
      this.SearchFormText.ID = "";
      this.SearchFormText.LoanNum = "";
      this.SearchFormText.SubName = "";
      this.SearchFormText.MinBudget = "";
      this.SearchFormText.MaxBudget = "";
      this.SearchFormText.Status = "";
    },
    submitalter(bvModalEvt) {
      bvModalEvt.preventDefault();
      this.$v.$touch();
      if (!this.$v.GrantForm.$invalid)
      {
        const payload = {
          PayNum: this.GrantForm.PayNum,
          LoanNum: this.GrantForm.LoanNum,
          PayDate: this.GrantForm.PayDate,
          Amount: this.GrantForm.Amount,
        };
        this.grantLoan(payload);
        // do your submit logic here
        this.submitStatusAdd = "PENDING";
        setTimeout(() => {
          this.submitStatusAdd = "OK";
        }, 500);
        this.initForm();
        this.$nextTick(() => {
          this.$bvModal.hide("grantloan");
        }, 2500);
      }
    },
    grantLoan(payload) {
      const path = "http://localhost:5000/grantloan";
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
    getUsers() {
      const path = "http://localhost:5000/loan";
      axios
        .get(path, {
          params: {
            ID: this.SearchFormText.ID,
            LoanNum: this.SearchFormText.LoanNum,
            SubName: this.SearchFormText.SubName,
            MinBudget: this.SearchFormText.MinBudget,
            MaxBudget: this.SearchFormText.MaxBudget,
            Status: this.SearchFormText.Status,
          },
        })
        .then((res) => {
          this.items = res.data.loans;
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
        this.selectedID = "Loan Number: " + this.selected[0].LoanNum + "?";
        this.$bvModal.show("deluser");
      }
    },
    alterclicked() {
      if (typeof this.selected[0] != "undefined") {
        this.GrantForm.LoanNum = this.selected[0].LoanNum;
        this.$bvModal.show("grantloan");
      }
    },
    initForm() {
      this.addUserForm.LoanNum = "";
      this.addUserForm.Budget = "";
      this.addUserForm.SubName = "";
      this.addUserForm.Paied = "";
      this.addUserForm.Status = "";
      this.GrantForm.Amount = "";
      this.GrantForm.LoanNum = "";
      this.GrantForm.Budget = "";
      this.GrantForm.PayDate = "";
      this.idlist = [
        {
          ID: "",
        },
      ];
      // this.addUserForm.ContectEmail = "";
      // this.addUserForm.Relationship = "";
    },
    //关闭模态框
    handleCancel() {
      this.initForm();
      this.idlist = [
        {
          ID: "",
        },
      ];
      this.$bvModal.hide("adduser");
    },
    submitadd(bvModalEvt) {
      bvModalEvt.preventDefault();
      this.$v.$touch();
      if (!this.$v.addUserForm.$invalid) {
        let List = [];
        for (var id of this.idlist) {
          List.push(id.ID);
        }
        const payload = {
          LoanNum: this.addUserForm.LoanNum,
          Budget: this.addUserForm.Budget,
          SubName: this.addUserForm.SubName,
          ID: List,
        };
        this.addUser(payload);
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
      const path = "http://localhost:5000/loan";
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
        LoanNum: this.selected[0].LoanNum,
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
      const path = "http://localhost:5000/delloan";
      axios
        .post(path, payload)
        .then(() => {
          this.onreset();
          this.getUsers();
        })
        .catch((error) => {
          this.errorHandle(error);
          window.console.log(error);
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
