import Vue from 'vue'
import router from './router'
import axios from "axios";

import BootstrapVue from "bootstrap-vue"

import App from './App'

import Default from './Layout/Wrappers/baseLayout.vue';
import Pages from './Layout/Wrappers/pagesLayout.vue';

import Vuelidate from 'vuelidate'

import store from './store/index';
import Vuex from 'vuex'

Vue.config.productionTip = false;

Vue.use(BootstrapVue);
Vue.use(Vuelidate)
Vue.use(Vuex)

Vue.component('default-layout', Default);
Vue.component('userpages-layout', Pages);

router.beforeEach((to, from, next) => {
	if (!to.meta.isLogin) {
		next()
	} else {
		let token = localStorage.getItem('Authorization');
		if (token == null || token == '') {
			next('/login')
		} else {
			next()
		}
	}
})

axios.interceptors.request.use(
	config => {
		let token = localStorage.getItem('Authorization');
		if (token) {
			config.headers.common['token'] = token
		}
		return config
	},
	err => {
		return Promise.reject(err);
	});

axios.interceptors.response.use(
	response => {
		return response
	},
	error => {
		// console.log('err' + error); // for debug
		if (error.response.status == 401) {//登录过期
			router.replace({ path: '/login' });//返回登录页
		}
		return Promise.reject(error)
	}
);

new Vue({
	el: '#app',
	router,
	store,
	template: '<App/>',
	components: { App },
});
