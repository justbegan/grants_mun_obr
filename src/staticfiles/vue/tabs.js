Vue.component('tabs', {
    template: `
        <div>
            <div class="tabs float-right">
                <ul>
                    <a v-for="tab in tabs" :href="tab.href" @click="selectTab(tab)">
                        <li :class="{ 'is-active': tab.isActive }">{{ tab.name }}</li>
                    </a>
                </ul>
            </div>
            <div class="tabs-details">
            <br><br><br>
                <div class="row">
                    <div class="col-sm-12 text-center" >
                        <button :disabled="disabled" v-show="showsave" class="btn btn-primary" v-on:click="validateAndSave">Сохранить</button>
                        <div v-show="showsave"><br>
                         Выключить автосохранение <input type="checkbox" v-model="disabledAutosave" @change="updateValue">
                         </div>
                    </div>
                </div>    <br>
                <slot></slot>
            </div>
            <div class="text-center">
                <button v-show="showsave" class="btn btn-primary" v-on:click="validateAndSave">Сохранить</button>
            </div><br>
            <div class="tabs float-right">
                <ul>
                    <a v-for="tab in tabs" :href="tab.href" @click="selectTab(tab)">
                        <li :class="{ 'is-active': tab.isActive }">{{ tab.name }}</li>
                    </a>
                </ul>
            </div>
        </div>
    `,
    props: {
        default: {default: null},
        save: {
            type: Function, default: function () {
            }
        },
        showsave: {type: Boolean, default: true},
        disabled: {default: false},
        propDisabledAutosave: {default: false}
    },
    data() {
        return {
            tabs: [],
            disabledAutosave: this.propDisabledAutosave
        };
    },
    created() {
        this.tabs = this.$children;
    },
    methods: {
        updateValue: function (e) {
            this.$emit('autosave-checkbox-toggle', e.target.checked);
        },
        selectTab(selectedTab) {
            this.tabs.forEach(tab => tab.isActive = (tab.name == selectedTab.name));
            this.$emit('change', selectedTab);
        },
        validateAndSave() {
            this.save()
        }
    },
    mounted() {
        let activeTab =
            this.tabs.find(tab => tab.href === decodeURI(window.location.hash)) ||
            this.tabs.find(tab => tab.id === this.default);
        if (activeTab) {
            this.selectTab(activeTab);
        }
    }
});

Vue.component('tab', {
    template: `<div v-show="isActive"><slot></slot></div> `,
    props: {
        id: {required: true},
        name: {required: true},
        selected: {default: false}
    },
    data() {
        return {
            isActive: false
        };
    },
    computed: {
        href() {
            return '#' + this.id;
        }
    }
});