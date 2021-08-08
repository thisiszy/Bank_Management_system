<template>
  <div>
    <page-title
      :heading="heading"
      :subheading="subheading"
      :icon="icon"
    ></page-title>

    <div class="content">
      <b-card class="main-card mb-3 text-center">
        <b-button class="mr-2" v-b-modal.modal1>Launch demo modal</b-button>
        <b-button class="mr-2" v-b-modal.modallg variant="primary"
          >Large modal</b-button
        >
        <b-button class="mr-2" v-b-modal.modallg>Small modal</b-button>
      </b-card>
    </div>
    <b-modal
      id="worker"
      size="lg"
      :visible="visible"
      :title="modelTitle"
      :close-on-click-modal="false"
      okText="确认"
      cancel-text="取消"
      @cancel="handleCancel"
      @ok="submit"
    >
      <form @submit.stop.prevent="submit">
        <b-form-group label="ID" label-for="id-input">
          <b-form-input
            id="id-input"
            class="good"
            v-model.trim="$v.addUserForm.SubName.$model"
            type="text"
            minlength="4"
            maxlength="5"
            required
          ></b-form-input>
          <div class="error" v-if="!$v.addUserForm.SubName.required">Name is required</div>
          <div class="error" v-if="!$v.addUserForm.SubName.minLength">
            Name must have at least
            {{ $v.addUserForm.SubName.$params.minLength.min }} letters.
          </div>
        </b-form-group>
      </form>
    </b-modal>
  </div>
</template>

<script>
import PageTitle from "../../Layout/Components/PageTitle.vue";
import { required, minLength } from "vuelidate/lib/validators";
import axios from "axios";

export default {
  components: {
    PageTitle,
  },
  data: () => ({
    heading: "Modals",
    subheading:
      "Wide selection of modal dialogs styles and animations available.",
    icon: "pe-7s-phone icon-gradient bg-premium-dark",
    visible: false,
    //模态对话框标题
    modelTitle: "New User",
    name: "",
    age: 0,
    submitStatus: null,
    addUserForm: {
      SubName: "123",
      DepartNum: "",
      WorkerID: "",
      WorkerAddr: "",
      StartDate: "",
    },
    // state: null,
  }),
  validations: {
    addUserForm: {
      SubName: {
        required,
        minLength: minLength(4),
      },
    },
  },
  methods: {
    initForm() {
      this.addUserForm.SubName = "";
      this.addUserForm.DepartNum = "";
      this.addUserForm.WorkerID = "";
      this.addUserForm.WorkerAddr = "";
      this.addUserForm.StartDate = "";
    },
    //显示模态框
    showModal() {
      this.visible = true;
    },
    //关闭模态框
    handleCancel() {
      this.visible = false;
    },
    submit(bvModalEvt) {
      bvModalEvt.preventDefault();
      window.console.log("submit!");
      this.$v.$touch();
      if (this.$v.$invalid) {
        window.console.log("error!");
        window.console.log(this.addUserForm.SubName);
        this.submitStatus = "ERROR";
      } else {
        // do your submit logic here
        this.submitStatus = "PENDING";
        setTimeout(() => {
          this.submitStatus = "OK";
        }, 500);
        this.initForm();
        this.$nextTick(() => {
          this.$bvModal.hide("worker");
        }, 2500);
      }
    },
    getUsers() {
      const path = "http://localhost:5000/user";
      axios
        .get(path)
        .then((res) => {
          this.workers = res.data.workers;
        })
        .catch((error) => {
          // eslint-disable-next-line
          window.console.error(error);
        });
    },
    addUser(payload) {
      const path = "http://localhost:5000/user";
      axios
        .post(path, payload)
        .then(() => {
          this.getworkers();
        })
        .catch((error) => {
          // eslint-disable-next-line
          window.console.log(error);
          this.getworkers();
        });
    },
  },
};
</script>
