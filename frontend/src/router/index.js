import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router);

export default new Router({
    scrollBehavior() {
        return window.scrollTo({ top: 0, behavior: 'smooth' });
    },
    routes: [
        // Dashboards

        {
            path: '/',
            name: 'analytics',
            component: () => import('../DemoPages/Analytics/Analytics.vue'),
            meta: {
                isLogin: true
            }
        },

        // Users

        {
            path: '/users',
            name: 'user-tables',
            component: () => import('../DemoPages/Users/UserTable.vue'),
            meta: {
                isLogin: true
            }
        },
        // Accounts
        {
            path: '/accounts',
            name: 'account-tables',
            component: () => import('../DemoPages/Account/AccountTable.vue'),
            meta: {
                isLogin: true
            }
        },
        // Loans
        {
            path: '/loans',
            name: 'loan-tables',
            component: () => import('../DemoPages/Loan/LoanTable.vue'),
            meta: {
                isLogin: true
            }
        },
        // Pages

        {
            path: '/login',
            name: 'login-boxed',
            meta: { layout: 'userpages' },
            component: () => import('../DemoPages/UserPages/LoginBoxed.vue'),
        },

        // // Elements

        // {
        //     path: '/elements/buttons-standard',
        //     name: 'buttons-standard',
        //     component: () => import('../DemoPages/Elements/Buttons/Standard.vue'),
        // },
        // {
        //     path: '/elements/dropdowns',
        //     name: 'dropdowns',
        //     component: () => import('../DemoPages/Elements/Dropdowns.vue'),
        // },
        // {
        //     path: '/elements/icons',
        //     name: 'icons',
        //     component: () => import('../DemoPages/Elements/Icons.vue'),
        // },
        // {
        //     path: '/elements/badges-labels',
        //     name: 'badges',
        //     component: () => import('../DemoPages/Elements/Badges.vue'),
        // },
        // {
        //     path: '/elements/cards',
        //     name: 'cards',
        //     component: () => import('../DemoPages/Elements/Cards.vue'),
        // },
        // {
        //     path: '/elements/list-group',
        //     name: 'list-group',
        //     component: () => import('../DemoPages/Elements/ListGroups.vue'),
        // },
        // {
        //     path: '/elements/timelines',
        //     name: 'timeline',
        //     component: () => import('../DemoPages/Elements/Timeline.vue'),
        // },
        // {
        //     path: '/elements/utilities',
        //     name: 'utilities',
        //     component: () => import('../DemoPages/Elements/Utilities.vue'),
        // },

        // // Components

        // {
        //     path: '/components/tabs',
        //     name: 'tabs',
        //     component: () => import('../DemoPages/Components/Tabs.vue'),
        // },
        // {
        //     path: '/components/accordions',
        //     name: 'accordions',
        //     component: () => import('../DemoPages/Components/Accordions.vue'),
        // },
        // {
        //     path: '/components/modals',
        //     name: 'modals',
        //     component: () => import('../DemoPages/Components/Modals.vue'),
        // },
        // {
        //     path: '/components/progress-bar',
        //     name: 'progress-bar',
        //     component: () => import('../DemoPages/Components/ProgressBar.vue'),
        // },
        // {
        //     path: '/components/tooltips-popovers',
        //     name: 'tooltips-popovers',
        //     component: () => import('../DemoPages/Components/TooltipsPopovers.vue'),
        // },
        // {
        //     path: '/components/pagination',
        //     name: 'pagination',
        //     component: () => import('../DemoPages/Components/Pagination.vue'),
        // },

        // // Forms

        // {
        //     path: '/forms/controls',
        //     name: 'controls',
        //     component: () => import('../DemoPages/Forms/Elements/Controls.vue'),
        // },
        // {
        //     path: '/forms/layouts',
        //     name: 'layouts',
        //     component: () => import('../DemoPages/Forms/Elements/Layouts.vue'),
        // },
    ]
})

