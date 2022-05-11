Vue.component('multicomplete', {
    template: `
    <div class="form-group row">
        <label class="col-sm-4 col-form-label">
            {{ label }}*
        </label>
        <div class="col-sm-8">
            <div v-for="item in filteredValues">
                <div class="row"> 
                    <div class="col-sm-11">
                        <autocomplete ref="autocomplete"
                            :search="search"
                            placeholder="Введите целевую группу"
                            aria-label=""
                            maxlength="254"
                            :defaultValue="item.content"
                            :get-result-value="getResultValue"
                            @input="handleInput(item)"
                            @submit="handleInput(item)"
                            auto-select> </autocomplete>
                    </div>
                    <div class="col-sm-1">
                        <button class="btn btn-danger btn-sm pull-right" v-on:click="deleteValue(item)">
                            <i class="fas fa-trash fa-inverse"></i>
                        </button>
                    </div>
                </div>
            </div><br>
            <button class="btn btn-primary" v-on:click="addValue">Добавить</button>
        </div>
    </div>
    `,
    props: {
        label: { required: true },
        value: { required: true },
        organization_id: { default: null },
        type: { default: "project" }
    },
    components: {
        Autocomplete
    },
    data() {
        return { 
            values: [],
            content: '',
            items: [
                "дети и подростки до 14 лет",
                "молодежь",
                "люди, попавшие в трудную жизненную ситуацию",
                "люди с ограниченными возможностями здоровья",
                "несовершеннолетние, находящиеся в трудной жизненной ситуации",
                "семьи с детьми",
            ],
        };
    },
    computed: {
        filteredValues() {
            return this.$root.project.target_groups.filter(v => (v.status !== "delete" && v.type === this.type))
        }
    },
    created: function () {
        this.values = this.value
    },
    methods: {
        search(input) {
            this.content = input
            //console.log(input)
            return this.items.filter(item => {
              return item.toLowerCase()
                .startsWith(input.toLowerCase())
            })
        },
        addValue() {
            return this.$root.project.target_groups.push({
                "content": "",
                "guid": uuidv4(),
                "status": "new",
                "type": this.type,
                "organization_id": this.organization_id,
            })
        },
        deleteValue($v) {
            if (window.confirm("Вы действительно хотите удалить этот элемент?")) { 
                $v.status = "delete"
            }
        },
        getResultValue(result) {
            this.content = result
            return result
        },
        handleInput(item) {
            item.content = this.content
        }
    }
});