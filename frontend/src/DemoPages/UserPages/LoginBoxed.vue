<template>
  <div>
    <div class="h-100 bg-plum-plate bg-animation">
      <div class="d-flex h-100 justify-content-center align-items-center">
        <b-col md="8" class="mx-auto app-login-box">
          <div class="mx-auto mb-3" >
            <h5 class="card-title" align="center">
              <font size="6" color="white">Bank Management System</font>
            </h5>
          </div>
          <div class="modal-dialog w-100 mx-auto">
            <div class="modal-content">
              <div class="modal-body">
                <div class="h5 modal-title text-center">
                  <h4 class="mt-2">
                    <div>Welcome back,</div>
                    <span>Please sign in to your account below.</span>
                  </h4>
                </div>
                <b-form-group id="exampleInputGroup1" label-for="exampleInput1">
                  <b-form-input
                    id="exampleInput1"
                    v-model.trim="LoginForm.Account"
                    type="text"
                    required
                    placeholder="Enter account name..."
                  >
                  </b-form-input>
                </b-form-group>
                <b-form-group id="exampleInputGroup2" label-for="exampleInput2">
                  <b-form-input
                    id="exampleInput2"
                    v-model.trim="LoginForm.Password"
                    type="password"
                    required
                    placeholder="Enter password..."
                  >
                  </b-form-input>
                  <br />
                  <div style="color: red" v-if="Loginstatus">
                    Account or password incorect!
                  </div>
                </b-form-group>
              </div>
              <div class="modal-footer clearfix">
                <div class="float-right">
                  <b-button variant="primary" size="lg" @click="onLogin"
                    >Login</b-button
                  >
                </div>
              </div>
            </div>
          </div>
          <div class="text-center text-white opacity-8 mt-3">
            Copyright &copy; ArchitectUI 2019 ❤ Modified by MacGuffin
          </div>
        </b-col>
      </div>
    </div>
  </div>
</template>


<script>
import axios from "axios";
import {mapMutations} from 'vuex'

export default {
  components: {},
  data: () => ({
    Loginstatus: 0,
    LoginForm: {
      Account: "",
      Password: "",
    },
  }),

  methods: {
			...mapMutations([
				'changeLogin'
			]),
    onLogin() {
      const path = "http://localhost:5000/login";
      let payload = {
        username: this.LoginForm.Account,
        password: this.LoginForm.Password,
      };
      axios
        .post(path, payload)
        .then((response) => {
          let token = response.data.token;
          window.console.log(response.data);
          this.changeLogin({ Authorization: token });
          this.Loginstatus = 0;
          this.$router.push({
            path: "/",
          });
        })
        .catch((error) => {
          this.Loginstatus = 1;
          // eslint-disable-next-line
          window.console.log(error);
        });
    },
  },
  oncreate() {
    this.Loginstatus = 0;
  }
};
</script>
