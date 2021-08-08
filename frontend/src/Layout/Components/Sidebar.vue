<template>
    <div class="app-sidebar sidebar-shadow" @mouseover="toggleSidebarHover('add','closed-sidebar-open')" @mouseleave="toggleSidebarHover('remove','closed-sidebar-open')">
        <div class="app-header__logo">
            <!-- <div class="logo-src"/> -->
            <h5 class="card-title">Bank Management</h5>
            <!-- <label>Bank Management System</label> -->
            <div class="header__pane ml-auto">
                <button type="button" class="hamburger close-sidebar-btn hamburger--elastic" v-bind:class="{ 'is-active' : isOpen }" @click="toggleBodyClass('closed-sidebar')">
                    <span class="hamburger-box">
                        <span class="hamburger-inner"></span>
                    </span>
                </button>
            </div>
        </div>
        <div class="app-sidebar-content">
            <VuePerfectScrollbar class="app-sidebar-scroll" v-once>
                <sidebar-menu showOneChild :menu="menu"/>
            </VuePerfectScrollbar>
        </div>

    </div>
</template>

<script>
    import {SidebarMenu} from 'vue-sidebar-menu'
    import VuePerfectScrollbar from 'vue-perfect-scrollbar'

    export default {
        components: {
            SidebarMenu,
            VuePerfectScrollbar
        },
        data() {
            return {
                isOpen: false,
                sidebarActive: false,

                menu: [
                    {
                        header: true,
                        title: 'Main Navigation',
                    },
                    {
                        title: 'Analytics',
                        icon: 'pe-7s-graph2',
                        href: '/',
                    },
                    {
                        title: 'Users',
                        icon: 'pe-7s-users',
                        href: '/users',
                    },
                    {
                        title: 'Accounts',
                        icon: 'pe-7s-wallet',
                        href: '/accounts',
                    },
                    {
                        title: 'Loans',
                        icon: 'pe-7s-credit',
                        href: '/loans',
                    },
                    // {
                    //     title: 'Login',
                    //     icon: 'pe-7s-browser',
                    //     href: '/login',
                    // },
                    // {
                    //     header: true,
                    //     title: 'UI Components',
                    // },
                    // {
                    //     icon: 'pe-7s-diamond',
                    //     title: 'Elements',
                    //     child: [
                    //         {
                    //             title: 'Buttons',
                    //             child: [
                    //                 {
                    //                     title: 'Standard',
                    //                     href: '/elements/buttons-standard',
                    //                 },
                    //             ]
                    //         },
                    //         {
                    //             title: 'Dropdowns',
                    //             href: '/elements/dropdowns',
                    //         },
                    //         {
                    //             title: 'Icons',
                    //             href: '/elements/icons',
                    //         },
                    //         {
                    //             title: 'Badges',
                    //             href: '/elements/badges-labels',
                    //         },
                    //         {
                    //             title: 'Cards',
                    //             href: '/elements/cards',
                    //         },
                    //         {
                    //             title: 'List Groups',
                    //             href: '/elements/list-group',
                    //         },
                    //         {
                    //             title: 'Timeline',
                    //             href: '/elements/timelines',
                    //         },
                    //         {
                    //             title: 'Utilities',
                    //             href: '/elements/utilities',
                    //         },
                    //     ],
                    // },
                    // {
                    //     icon: 'pe-7s-car',
                    //     title: 'Components',
                    //     child: [
                    //         {
                    //             title: 'Tabs',
                    //             href: '/components/tabs',
                    //         },
                    //         {
                    //             title: 'Accordions',
                    //             href: '/components/accordions',
                    //         },
                    //         {
                    //             title: 'Modals',
                    //             href: '/components/modals',
                    //         },
                    //         {
                    //             title: 'Progress Bar',
                    //             href: '/components/progress-bar',
                    //         },
                    //         {
                    //             title: 'Tooltips & Popovers',
                    //             href: '/components/tooltips-popovers',
                    //         },
                    //         {
                    //             title: 'Pagination',
                    //             href: '/components/pagination',
                    //         },
                    //     ],
                    // },
                    // {
                    //     header: true,
                    //     title: 'Forms',
                    // },
                    // {
                    //     icon: 'pe-7s-light',
                    //     title: 'Elements',
                    //     child: [
                    //         {
                    //             title: 'Controls',
                    //             href: '/forms/controls',
                    //         },
                    //         {
                    //             title: 'Layouts',
                    //             href: '/forms/layouts',
                    //         },
                    //     ],
                    // },
                ],
                collapsed: true,

                windowWidth: 0,

            }
        },
        props: {
            sidebarbg: String,
        },
        methods: {

            toggleBodyClass(className) {
                const el = document.body;
                this.isOpen = !this.isOpen;

                if (this.isOpen) {
                    el.classList.add(className);
                } else {
                    el.classList.remove(className);
                }
            },
            toggleSidebarHover(add, className) {
                const el = document.body;
                this.sidebarActive = !this.sidebarActive;

                this.windowWidth = document.documentElement.clientWidth;

                if (this.windowWidth > '992') {
                    if (add === 'add') {
                        el.classList.add(className);
                    } else {
                        el.classList.remove(className);
                    }
                }
            },
            getWindowWidth() {
                const el = document.body;

                this.windowWidth = document.documentElement.clientWidth;

                if (this.windowWidth < '1350') {
                    el.classList.add('closed-sidebar', 'closed-sidebar-md');
                } else {
                    el.classList.remove('closed-sidebar', 'closed-sidebar-md');
                }
            },
        },
        mounted() {
            this.$nextTick(function () {
                window.addEventListener('resize', this.getWindowWidth);

                //Init
                this.getWindowWidth()
            })
        },

        beforeDestroy() {
            window.removeEventListener('resize', this.getWindowWidth);
        }
    }
</script>
