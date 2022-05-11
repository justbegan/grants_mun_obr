Vue.component('partners', {
    template: `
    <div class="form-group row">
        <label class="col-sm-4 col-form-label">
            {{label}}
        </label>
        <div class="col-sm-8">
            <div v-for="item in partners">
                <div class="row"> 
                    <div class="col-sm-6">
                        <textarea :maxlength="max" v-model="item.name" class="form-control" rows="2"></textarea>
                        <small>
                        Данное поле обязательно для заполнения.<br>
                        </small>
                    </div>
                    <div class="col-sm-5">
                        <vue-tags-input
                            placeholder="Выбрать поддержку"
                            v-model="tag"
                            :tags="item.supports"
                            :autocomplete-items="supports"
                            @tags-changed="newTags => item.supports = newTags"
                            :add-only-from-autocomplete="true"
                            :autocomplete-min-length="0"
                        />
                    </div>
                    <div class="col-sm-1">
                        <button class="btn btn-danger btn-sm pull-right" v-on:click="deleteValue(item)">
                            <i class="fas fa-trash fa-inverse"></i>
                        </button>
                    </div>
                </div>
               
                
            </div>
            <button class="btn btn-primary" v-on:click="addValue">Добавить</button>
        </div>
    </div>
    `,
    props: {
        label: {default: ''},
        max: { default: 255 },
        maxItems: {
            default: 5
        }
    },
    data() {
        return { 
            tag: '',
           
            autocompleteItems: [{
                text: 'Организационная',
            }, {
                text: 'Консультационная',
            }, {
                text: 'Имущественная',
            }, {
                text: 'Материальная',
            }, {
                text: 'Информационная',
            },{
                text: 'Иная поддержка',
            }],
        };
    },
    computed: {
        partners() {
            return this.$root.project.partners.filter(v => (v.status !== "delete"))
        },
        supports() {
            return this.autocompleteItems.filter(i => {
                return i.text.toLowerCase().indexOf(this.tag.toLowerCase()) !== -1;
            });
        },
    },
    methods: {
        addValue() {
            //if (this.partners.length < this.maxItems) {
                this.$root.project.partners.push({
                    "name": "",
                    "guid": uuidv4(),
                    "status": "new",
                    "supports": []
                })
            //}
        },
        deleteValue($v) {
            if (window.confirm("Вы действительно хотите удалить этот элемент?")) { 
                $v.status = "delete"
            }
        }
    }
});