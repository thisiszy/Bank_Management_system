<template>
    <div class="app-page-title">
        <div class="page-title-wrapper">
            <div class="page-title-heading">
                <div class="page-title-icon">
                    <i :class="icon"/>
                </div>
                <div>
                    {{heading}}
                    <div
                        class="page-title-subheading">
                        {{subheading}}
                    </div>
                </div>
            </div>
            <div class="page-title-actions" v-if="btndefined">
                <!-- <button type="button" class="btn-shadow mr-3 btn btn-dark">
                    <font-awesome-icon icon="star"/>
                </button> -->
                <button type="button" class="btn-shadow mr-3 d-inline-flex align-items-center btn btn-success" @click="onClickCreate">
                    <font-awesome-icon class="mr-2" icon="plus"/>
                    {{leftbtn}}
                </button>
                <slot name="extbtn"></slot>
                <button
                type="button"
                class="btn-shadow mr-3 btn btn-danger"
                @click="onClickAlter"
                >
                {{midbtn}}
                </button>
                <button
                type="button"
                class="btn-shadow mr-3 btn btn-dark"
                @click="onClickDelete"
                >
                {{rightbtn}}
                </button>
            </div>
        </div>
    </div>
</template>

<script>
    import {library} from '@fortawesome/fontawesome-svg-core'
    import {
        faStar,
        faPlus
    } from '@fortawesome/free-solid-svg-icons'
    import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome'

    library.add(
        faStar,
        faPlus,
    );

    export default {
        components: {
            'font-awesome-icon': FontAwesomeIcon,
        },
        props: {
            icon: String,
            heading: String,
            subheading: String,
            leftbtn: String,
            midbtn: String,
            rightbtn: String,
            btndefined: Boolean,
        },
        methods: {
            getParams: function () {
            },
            onClickCreate: function () {
                this.$emit("add");
            },
            onClickDelete: function () {
                this.$emit("del");
            },
            onClickAlter: function () {
                this.$emit("alter");
            },
        }
    }
</script>
