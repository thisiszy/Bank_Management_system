<template>
    <div class="d-flex">
        <div class="header-btn-lg pr-0">
            <div class="widget-content p-0">
                <div class="widget-content-wrapper">
                    <div class="widget-content-left">
                        <b-dropdown toggle-class="p-0 mr-2" menu-class="dropdown-menu-lg" variant="link" right>
                            <span slot="button-content">
                                <div class="icon-wrapper icon-wrapper-alt rounded-circle">
                                    <i class="pe-7s-user icon-gradient bg-night-fade"> </i>
                                </div>
                            </span>
                            <router-link to='/users'  style="text-decoration: none; color: inherit;">
                            <button type="button" tabindex="0" class="dropdown-item">Profile</button>
                            </router-link>
                            <!-- <button type="button" tabindex="0" class="dropdown-item">Settings</button> -->
                            <!-- <h6 tabindex="-1" class="dropdown-header">Header</h6> -->
                            <!-- <button type="button" tabindex="0" class="dropdown-item">Actions</button> -->
                            <div tabindex="-1" class="dropdown-divider"></div>
                            <button type="button" tabindex="0" class="dropdown-item" @click="onLogout">Logout</button>
                        </b-dropdown>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    // import VuePerfectScrollbar from 'vue-perfect-scrollbar'

    import {library} from '@fortawesome/fontawesome-svg-core'
    import {
        faAngleDown,
        faCalendarAlt,
        faTrashAlt,
        faCheck,
        faFileAlt,
        faCloudDownloadAlt,
        faFileExcel,
        faFilePdf,
        faFileArchive,
        faEllipsisH,
    } from '@fortawesome/free-solid-svg-icons'
    import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome'
    // import axios from "axios";
    import {mapMutations} from 'vuex'

    library.add(
        faAngleDown,
        faCalendarAlt,
        faTrashAlt,
        faCheck,
        faFileAlt,
        faCloudDownloadAlt,
        faFileExcel,
        faFilePdf,
        faFileArchive,
        faEllipsisH,
    );

    export default {
        components: {
            'font-awesome-icon': FontAwesomeIcon,
        },
        data: () => ({

        }),

        methods: {
			...mapMutations([
				'changeLogin'
			]),
            onLogout() {
                window.console.log("logout!");
                this.changeLogin({Authorization: ""});
                this.$router.push({
                    path: "/login",
                });
            },
        }
    }


</script>
