Vue.component('geography', {
    template: `
    <div class="form-group row">
        <label class="col-sm-4 col-form-label">
            {{ label }}
        </label>
        <div class="col-sm-8">
            <div class="row"> 
                <div class="col-sm-11">
                    <autocomplete ref="autocomplete"
                        :search="search"
                        :get-result-value="getResultValue"
                        placeholder="Введите географию и нажмите +"
                        aria-label=""></autocomplete>
                </div>
                <div class="col-sm-1">
                    <button class="btn btn-info" v-on:click="addValue"><i class="fas fa-plus fa-inverse"></i></button>
                </div>
            </div>
            <small>Данное поле обязательно для заполнения.</small>
            <hr>
            <div v-for="item in filteredValues">
                <div class="row"> 
                    <div class="col-sm-11">
                        {{item.name}}
                    </div>
                    <div class="col-sm-1">
                        <button class="btn btn-danger btn-sm pull-right" v-on:click="deleteValue(item)">
                            <i class="fas fa-trash fa-inverse"></i>
                        </button>
                    </div>
                </div>
            </div>
            
        </div>
    </div>
    `,
    props: {
        label: { required: true },
        type: { default: 'project' },
        id: { required: true },
        maxItems: {
            default: 36
        }
    },
    components: {
        Autocomplete
    },
    data() {
        return { 
            values: [],
            name: ''
        };
    },
    computed: {
        filteredValues() {
            if(this.type === 'project') {
                return this.$root.project.geography.filter(v => v.status !== "delete" && v.organization_id === null)
            }
            return this.$root.project.geography.filter(v => v.status !== "delete" && v.organization_id === this.id)
        }
    },
   
    methods: {
        search(input) {
            const url = `/user/regions/${encodeURI(input)}`
            if (input.length < 3) {
                return []
            }
            return new Promise(resolve => {
                fetch(url)
                    .then(response => response.json())
                    .then(data => {
                        resolve(data)
                    })
            })          
        },
        getResultValue(result) {
            this.name = result
            return result
        },
       
        addValue() {
            if(this.name !== '') {
                if(this.type === 'project') {
                    this.$root.project.geography.push({
                        "name": this.name,
                        "status": "new",
                        "organization_id": null,
                        "guid": uuidv4()
                    })
                } else {
                    if (this.filteredValues.length < this.maxItems) {
                        this.$root.project.geography.push({
                            "name": this.name,
                            "status": "new",
                            "organization_id": this.id,
                            "guid": uuidv4()
                        })
                    }
                }
                this.$refs.autocomplete.setValue('')
                this.name = ''
            }
        },
        deleteValue($v) {
            if (window.confirm("Вы действительно хотите удалить этот элемент?")) { 
                $v.status = "delete"
            }
        }
    }
});