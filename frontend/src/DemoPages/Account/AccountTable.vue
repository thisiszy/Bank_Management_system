<template>
  <div>
    <page-title
      :heading="heading"
      :subheading="subheading"
      :icon="icon"
      @add="addclicked"
      @del="delclicked"
      @alter="alterclicked"
      leftbtn="Create Account"
      midbtn="Alter Account"
      rightbtn="Delete Account"
      :btndefined="true"
    >
      <template #extbtn>
        <button
          type="button"
          class="btn-shadow mr-3 btn btn-alternate"
          @click="extbtnclicled"
        >
          Add User to Account
        </button>
      </template>
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
        <h5 class="card-title">Search Accounts</h5>
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
              <b-form-group label="AccNum" label-for="AccNum-input">
                <b-form-input
                  id="SearchFormAddress"
                  type="number"
                  v-model.trim="SearchFormText.AccNum"
                ></b-form-input>
              </b-form-group>
            </b-input-group>
          </div>
          <div class="col-md-2">
            <div class="position-relative form-group">
              <label for="exampleCustomSelect" class="">Account Type</label
              ><select
                type="select"
                id="exampleCustomSelect"
                name="customSelect"
                class="custom-select"
                v-model="SearchFormText.AccType"
              >
                <option value="">Select</option>
                <option>Checking</option>
                <option>Saving</option>
              </select>
            </div>
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
              <b-form-group label="BalanceMin" label-for="BalanceMin-input">
                <b-form-input
                  id="BalanceMin"
                  type="number"
                  v-model.trim="SearchFormText.BalanceMin"
                ></b-form-input>
              </b-form-group>
            </b-input-group>
          </div>
          <div class="col-md-2">
            <b-input-group>
              <b-form-group label="BalanceMax" label-for="BalanceMax-input">
                <b-form-input
                  id="BalanceMax"
                  type="number"
                  v-model.trim="SearchFormText.BalanceMax"
                ></b-form-input>
              </b-form-group>
            </b-input-group>
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
    <b-card title="Accounts" class="main-card mb-4">
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
      id="addacc"
      size="lg"
      :title="modelTitleadd"
      :close-on-click-modal="false"
      @cancel="handleCancel"
      @ok="submitadd"
    >
      <form @submitadd.stop.prevent="submitadd">
        <div class="position-relative form-group" required>
          <div>
            <div class="custom-checkbox custom-control custom-control-inline">
              <label class="form-check-label"
                ><input
                  name="radio1"
                  type="radio"
                  class="form-check-input"
                  @click="saving"
                />
                Saving Account</label
              >
            </div>
            <div class="custom-checkbox custom-control custom-control-inline">
              <label class="form-check-label"
                ><input
                  name="radio1"
                  type="radio"
                  class="form-check-input"
                  @click="checking"
                />
                Checking Account</label
              >
            </div>
          </div>
          <div class="error" v-if="!radiostatus">Please select one</div>
        </div>
        <b-form-group label="Account Number" label-for="acc-input">
          <b-form-input
            id="acc-input"
            v-model.trim="$v.addAccountForm.AccNum.$model"
            type="number"
            :state="
              $v.addAccountForm.AccNum.$anyDirty
                ? !$v.addAccountForm.AccNum.$anyError
                : null
            "
          ></b-form-input>
          <div class="error" v-if="!$v.addAccountForm.AccNum.required">
            Account Number is required
          </div>
          <div class="error" v-if="!$v.addAccountForm.AccNum.minLength">
            Account Number must have
            {{ $v.addAccountForm.AccNum.$params.minLength.min }} numbers.
          </div>
          <div class="error" v-if="!$v.addAccountForm.AccNum.maxLength">
            Account Number must have
            {{ $v.addAccountForm.AccNum.$params.maxLength.max }} numbers.
          </div>
        </b-form-group>
        <b-form-group label="ID" label-for="id-input">
          <b-form-input
            id="id-input"
            v-model.trim="$v.addAccountForm.ID.$model"
            type="text"
            :state="
              $v.addAccountForm.ID.$anyDirty
                ? !$v.addAccountForm.ID.$anyError
                : null
            "
          ></b-form-input>
          <div class="error" v-if="!$v.addAccountForm.ID.required">
            ID is required
          </div>
          <div class="error" v-if="!$v.addAccountForm.ID.minLength">
            ID must have
            {{ $v.addAccountForm.ID.$params.minLength.min }} letters.
          </div>
          <div class="error" v-if="!$v.addAccountForm.ID.maxLength">
            ID must have
            {{ $v.addAccountForm.ID.$params.maxLength.max }} letters.
          </div>
        </b-form-group>
        <b-form-group label="Balance" label-for="address-input">
          <b-form-input
            id="address-input"
            v-model.trim="$v.addAccountForm.Balance.$model"
            type="number"
            :state="
              $v.addAccountForm.Balance.$anyDirty
                ? !$v.addAccountForm.Balance.$anyError
                : null
            "
          ></b-form-input>
          <div class="error" v-if="!$v.addAccountForm.Balance.required">
            Balance is required
          </div>
        </b-form-group>
        <b-form-group label="OpenDate" label-for="OpenDate-input">
          <b-form-input
            id="OpenDate-input"
            v-model.trim="$v.addAccountForm.OpenDate.$model"
            type="date"
            :state="
              $v.addAccountForm.OpenDate.$anyDirty
                ? !$v.addAccountForm.OpenDate.$anyError
                : null
            "
          ></b-form-input>
          <div class="error" v-if="!$v.addAccountForm.OpenDate.required">
            OpenDate is required
          </div>
        </b-form-group>
        <b-form-group label="SubName" label-for="SubName-input">
          <b-form-input
            id="SubName-input"
            v-model.trim="$v.addAccountForm.SubName.$model"
            type="text"
            :state="
              $v.addAccountForm.SubName.$anyDirty
                ? !$v.addAccountForm.SubName.$anyError
                : null
            "
          ></b-form-input>
          <div class="error" v-if="!$v.addAccountForm.SubName.required">
            SubName is required
          </div>
        </b-form-group>
        <b-form-group label="Rate" label-for="Rate-input" v-if="acctype == '0'">
          <b-form-input
            id="Rate-input"
            v-model.trim="$v.SavingForm.Rate.$model"
            type="text"
            :state="
              $v.SavingForm.Rate.$anyDirty
                ? !$v.SavingForm.Rate.$anyError
                : null
            "
          ></b-form-input>
          <div
            class="error"
            v-if="!$v.SavingForm.Rate.required && acctype == '0'"
          >
            Rate is required
          </div>
        </b-form-group>
        <b-form-group
          label="CurrencyType"
          label-for="CurrencyType-input"
          v-if="acctype == '0'"
        >
          <b-form-input
            id="CurrencyType-input"
            v-model.trim="$v.SavingForm.CurrencyType.$model"
            type="text"
            :state="
              $v.SavingForm.CurrencyType.$anyDirty
                ? !$v.SavingForm.CurrencyType.$anyError
                : null
            "
          ></b-form-input>
          <div
            class="error"
            v-if="!$v.SavingForm.CurrencyType.required && acctype == '0'"
          >
            CurrencyType is required
          </div>
        </b-form-group>
        <b-form-group
          label="Overdraft"
          label-for="Overdraft-input"
          v-if="acctype == '1'"
        >
          <b-form-input
            id="Overdraft-input"
            v-model.trim="$v.CheckingForm.Overdraft.$model"
            type="text"
            :state="
              $v.CheckingForm.Overdraft.$anyDirty
                ? !$v.CheckingForm.Overdraft.$anyError
                : null
            "
          ></b-form-input>
          <div
            class="error"
            v-if="!$v.CheckingForm.Overdraft.required && acctype == '1'"
          >
            Overdraft is required
          </div>
        </b-form-group>
      </form>
    </b-modal>

    <b-modal
      id="alteracc"
      size="lg"
      :title="modelTitleAlter"
      :close-on-click-modal="false"
      @cancel="handleCancel"
      @ok="submitalter"
    >
      <form @submitalter.stop.prevent="submitalter">
        <b-form-group label="Account Number" label-for="acc-input">
          <b-form-input
            id="acc-input"
            v-model.trim="$v.addAccountForm.AccNum.$model"
            type="number"
            disabled
          ></b-form-input>
        </b-form-group>
        <b-form-group label="Balance" label-for="address-input">
          <b-form-input
            id="address-input"
            v-model.trim="$v.addAccountForm.Balance.$model"
            type="number"
            :state="
              $v.addAccountForm.Balance.$anyDirty
                ? !$v.addAccountForm.Balance.$anyError
                : null
            "
          ></b-form-input>
          <div class="error" v-if="!$v.addAccountForm.Balance.required">
            Balance is required
          </div>
        </b-form-group>
        <b-form-group label="Rate" label-for="Rate-input" v-if="acctype == '0'">
          <b-form-input
            id="Rate-input"
            v-model.trim="$v.SavingForm.Rate.$model"
            type="text"
            :state="
              $v.SavingForm.Rate.$anyDirty
                ? !$v.SavingForm.Rate.$anyError
                : null
            "
          ></b-form-input>
          <div
            class="error"
            v-if="!$v.SavingForm.Rate.required && acctype == '0'"
          >
            Rate is required
          </div>
        </b-form-group>
        <b-form-group
          label="CurrencyType"
          label-for="CurrencyType-input"
          v-if="acctype == '0'"
        >
          <b-form-input
            id="CurrencyType-input"
            v-model.trim="$v.SavingForm.CurrencyType.$model"
            type="text"
            :state="
              $v.SavingForm.CurrencyType.$anyDirty
                ? !$v.SavingForm.CurrencyType.$anyError
                : null
            "
          ></b-form-input>
          <div
            class="error"
            v-if="!$v.SavingForm.CurrencyType.required && acctype == '0'"
          >
            CurrencyType is required
          </div>
        </b-form-group>
        <b-form-group
          label="Overdraft"
          label-for="Overdraft-input"
          v-if="acctype == '1'"
        >
          <b-form-input
            id="Overdraft-input"
            v-model.trim="$v.CheckingForm.Overdraft.$model"
            type="text"
            :state="
              $v.CheckingForm.Overdraft.$anyDirty
                ? !$v.CheckingForm.Overdraft.$anyError
                : null
            "
          ></b-form-input>
          <div
            class="error"
            v-if="!$v.CheckingForm.Overdraft.required && acctype == '1'"
          >
            Overdraft is required
          </div>
        </b-form-group>
      </form>
    </b-modal>

    <b-modal
      id="adduser"
      size="lg"
      :title="modelTitleAddUser"
      :close-on-click-modal="false"
      @cancel="handleCancel"
      @ok="submitadduser"
    >
      <form @submitalter.stop.prevent="submitalter">
        <b-form-group label="Account Number" label-for="acc-input">
          <b-form-input
            id="acc-input"
            v-model.trim="$v.addAccountForm.AccNum.$model"
            type="number"
          ></b-form-input>
        </b-form-group>
        <b-form-group label="ID" label-for="id-input">
          <b-form-input
            id="id-input"
            v-model.trim="$v.addAccountForm.ID.$model"
            type="text"
            :state="
              $v.addAccountForm.ID.$anyDirty
                ? !$v.addAccountForm.ID.$anyError
                : null
            "
          ></b-form-input>
          <div class="error" v-if="!$v.addAccountForm.ID.required">
            ID is required
          </div>
          <div class="error" v-if="!$v.addAccountForm.ID.minLength">
            ID must have
            {{ $v.addAccountForm.ID.$params.minLength.min }} letters.
          </div>
          <div class="error" v-if="!$v.addAccountForm.ID.maxLength">
            ID must have
            {{ $v.addAccountForm.ID.$params.maxLength.max }} letters.
          </div>
        </b-form-group>
      </form>
    </b-modal>

    <b-modal
      id="delacc"
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
import { required, minLength, maxLength } from "vuelidate/lib/validators";
import axios from "axios";

library.add(faStar, faPlus);
export default {
  components: {
    PageTitle,
    "font-awesome-icon": FontAwesomeIcon,
  },
  data: () => ({
    heading: "Accounts",
    subheading: "You can add delete alter search accounts here.",
    icon: "pe-7s-cash icon-gradient bg-happy-itmeo",

    fields: [
      "AccNum",
      "ID",
      "SubName",
      "Balance",
      "LastAccessTime",
      "OpenDate",
      "Rate",
      "CurrencyType",
      "Overdraft",
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
    modelTitleadd: "New Account",
    modelTitleAlter: "Alter Account",
    modelTitleAddUser: "Add a user to account",
    submitStatusAdd: null,
    addAccountForm: {
      AccNum: "",
      ID: "",
      Balance: "",
      OpenDate: "",
      SubName: "",
    },
    SavingForm: {
      Rate: "",
      CurrencyType: "",
    },
    CheckingForm: {
      Overdraft: "",
    },

    modelTitledel: "Are you sure to delete?",
    submitStatusDel: null,
    selected: [],
    dropdowntext: "All",
    // dropdownstatus: 0,
    SearchFormText: {
      AccNum: "",
      AccType: "",
      SubName: "",
      BalanceMin: "",
      BalanceMax: "",
      ID: "",
    },
    selectedID: "",
    acctype: null,
    radiostatus: false,
    dismissSecs: 3,
    dismissCountDown: 0,
    alertmsg: "",
  }),

  validations: {
    addAccountForm: {
      AccNum: {
        required,
        minLength: minLength(19),
        maxLength: maxLength(19),
      },
      ID: {
        required,
        minLength: minLength(18),
        maxLength: maxLength(18),
      },
      Balance: {
        required,
      },
      OpenDate: {
        required,
      },
      SubName: {
        required,
      },
    },
    SavingForm: {
      Rate: {
        required,
      },
      CurrencyType: {
        required,
      },
    },
    CheckingForm: {
      Overdraft: {
        required,
      },
    },
    SearchFormText: {
      required,
    },
  },
  created() {
    this.getAccounts();
  },
  methods: {
    saving() {
      this.acctype = "0";
      this.radiostatus = true;
    },
    checking() {
      this.acctype = "1";
      this.radiostatus = true;
    },
    // chooseAll() {
    //   this.dropdowntext = "All";
    //   this.dropdownstatus = 0;
    // },
    // chooseID() {
    //   this.dropdowntext = "By Account Num";
    //   this.dropdownstatus = 1;
    // },
    // chooseAccount() {
    //   this.dropdowntext = "By ID";
    //   this.dropdownstatus = 2;
    // },
    addclicked() {
      this.$bvModal.show("addacc");
    },
    extbtnclicled() {
      if (typeof this.selected[0] != "undefined") {
        this.addAccountForm.AccNum = this.selected[0].AccNum;
      }
      this.$bvModal.show("adduser");
    },
    onsearch() {
      this.getAccounts();
      // window.console.log(this.SearchFormText.AccType);
    },
    onreset() {
      this.SearchFormText.ID = "";
      this.SearchFormText.AccNum = "";
      this.SearchFormText.AccType = "";
      this.SearchFormText.SubName = "";
      this.SearchFormText.BalanceMin = "";
      this.SearchFormText.BalanceMax = "";
    },
    getAccounts() {
      const path = "http://localhost:5000/account";
      axios
        .get(path, {
          params: {
            ID: this.SearchFormText.ID,
            AccNum: this.SearchFormText.AccNum,
            AccType: this.SearchFormText.AccType,
            SubName: this.SearchFormText.SubName,
            BalanceMin: this.SearchFormText.BalanceMin,
            BalanceMax: this.SearchFormText.BalanceMax,
          },
        })
        .then((res) => {
          this.items = res.data.accounts;
        })
        .catch((error) => {
          // eslint-disable-next-line
          this.errorHandle(error);
          window.console.error(error);
        });
    },
    getAccountType(param) {
      const path = "http://localhost:5000/acctype";
      axios
        .get(path, {
          params: {
            AccNum: param,
          },
        })
        .then((res) => {
          this.acctype = res.data.acctype;
        })
        .catch((error) => {
          // eslint-disable-next-line
          this.errorHandle(error);
          this.window.console.error(error);
        });
    },
    delclicked() {
      if (typeof this.selected[0] != "undefined") {
        this.selectedID = "Account Number: " + this.selected[0].AccNum + "?";
        this.$bvModal.show("delacc");
      }
    },
    alterclicked() {
      if (typeof this.selected[0] != "undefined") {
        this.getAccountType(this.selected[0].AccNum);
        this.addAccountForm.AccNum = this.selected[0].AccNum;
        this.addAccountForm.Balance = this.selected[0].Balance;
        this.addAccountForm.OpenDate = this.selected[0].OpenDate;
        this.addAccountForm.SubName = this.selected[0].SubName;
        this.SavingForm.Rate = this.selected[0].Rate;
        this.SavingForm.CurrencyType = this.selected[0].CurrencyType;
        this.CheckingForm.Overdraft = this.selected[0].Overdraft;
        this.$bvModal.show("alteracc");
      }
    },
    initForm() {
      this.radiostatus = false;
      this.addAccountForm.AccNum = "";
      this.addAccountForm.ID = "";
      this.addAccountForm.Balance = "";
      this.addAccountForm.OpenDate = "";
      this.addAccountForm.SubName = "";
      this.SavingForm.Rate = "";
      this.SavingForm.CurrencyType = "";
      this.CheckingForm.Overdraft = "";
    },
    //关闭模态框
    handleCancel() {
      this.initForm();
      this.visible = false;
    },
    submitadduser() {
      if (
        !this.$v.addAccountForm.AccNum.$invalid &&
        !this.$v.addAccountForm.ID.$invalid
      ) {
        const payload = {
          AccNum: this.addAccountForm.AccNum,
          ID: this.addAccountForm.ID,
        };
        this.adduser(payload);
        // do your submit logic here
        this.submitStatusAdd = "PENDING";
        setTimeout(() => {
          this.submitStatusAdd = "OK";
        }, 500);
        this.initForm();
        this.$nextTick(() => {
          this.$bvModal.hide("addacc");
        }, 2500);
      }
    },
    submitadd(bvModalEvt) {
      bvModalEvt.preventDefault();
      this.$v.$touch();
      if (!this.$v.addAccountForm.Balance.$invalid) {
        if (
          (!this.$v.CheckingForm.$invalid && this.acctype == "1") ||
          (!this.$v.SavingForm.$invalid && this.acctype == "0")
        ) {
          const payload = {
            type: this.acctype,
            AccNum: this.addAccountForm.AccNum,
            ID: this.addAccountForm.ID,
            Balance: this.addAccountForm.Balance,
            OpenDate: this.addAccountForm.OpenDate,
            SubName: this.addAccountForm.SubName,
            Rate: this.SavingForm.Rate,
            CurrencyType: this.SavingForm.CurrencyType,
            Overdraft: this.CheckingForm.Overdraft,
          };
          this.addAccount(payload);
          // do your submit logic here
          this.submitStatusAdd = "PENDING";
          setTimeout(() => {
            this.submitStatusAdd = "OK";
          }, 500);
          this.initForm();
          this.$nextTick(() => {
            this.$bvModal.hide("addacc");
          }, 2500);
        }
      }
    },
    submitalter(bvModalEvt) {
      bvModalEvt.preventDefault();
      this.$v.$touch();
      if (
        ((!this.$v.CheckingForm.$invalid && this.acctype == "1") ||
          (!this.$v.SavingForm.$invalid && this.acctype == "0")) &&
        !this.$v.addAccountForm.Balance.$invalid
      ) {
        const payload = {
          AccNum: this.addAccountForm.AccNum,
          Balance: this.addAccountForm.Balance,
          Rate: this.SavingForm.Rate,
          CurrencyType: this.SavingForm.CurrencyType,
          Overdraft: this.CheckingForm.Overdraft,
        };
        this.alterAccount(payload);
        // do your submit logic here
        this.submitStatusAdd = "PENDING";
        setTimeout(() => {
          this.submitStatusAdd = "OK";
        }, 500);
        this.initForm();
        this.$nextTick(() => {
          this.$bvModal.hide("alteracc");
        }, 2500);
      }
    },
    addAccount(payload) {
      const path = "http://localhost:5000/account";
      axios
        .post(path, payload)
        .then(() => {
          this.onreset();
          this.getAccounts();
        })
        .catch((error) => {
          // eslint-disable-next-line
          window.console.log(error);
          this.errorHandle(error);
          this.onreset();
          this.getAccounts();
        });
    },
    adduser(payload) {
      const path = "http://localhost:5000/adduser2acc";
      axios
        .post(path, payload)
        .then(() => {
          this.onreset();
          this.getAccounts();
        })
        .catch((error) => {
          // eslint-disable-next-line
          window.console.log(error);
          this.errorHandle(error);
          this.onreset();
          this.getAccounts();
        });
    },
    alterAccount(payload) {
      const path = "http://localhost:5000/alteracc";
      axios
        .post(path, payload)
        .then(() => {
          this.onreset();
          this.getAccounts();
        })
        .catch((error) => {
          // eslint-disable-next-line
          window.console.log(error);
          this.errorHandle(error);
          this.onreset();
          this.getAccounts();
        });
    },
    delconfirm(bvModalEvt) {
      bvModalEvt.preventDefault();
      this.$v.$touch();
      const payload = {
        AccNum: this.selected[0].AccNum,
      };
      this.delAccount(payload);
      this.submitStatusDel = "PENDING";
      setTimeout(() => {
        this.submitStatusDel = "OK";
      }, 500);
      this.initForm();
      this.$nextTick(() => {
        this.$bvModal.hide("delacc");
      }, 2500);
    },
    delAccount(payload) {
      const path = "http://localhost:5000/delacc";
      axios
        .post(path, payload)
        .then(() => {
          this.onreset();
          this.getAccounts();
        })
        .catch((error) => {
          window.console.log(error);
          this.errorHandle(error);
          this.onreset();
          this.getAccounts();
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
