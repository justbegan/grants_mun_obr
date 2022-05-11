Vue.component('quantresults', {
    template: `
    <div class="form-group row">
        <label class="col-sm-4 col-form-label">
            {{label}}
        </label>
        <div class="col-sm-8">
            <div v-for="item in results">
                <div class="row"> 
                    <div class="col-sm-8">
                        <textarea :readonly="!canDelete(item)" required :maxlength="max" v-model="item.name" class="form-control" rows="2"></textarea>
                        <small>
                        Это поле обязательно для заполнения
                        </small>
                    </div>
                    <div class="col-sm-3">
                        <input required v-model="item.count" type="number" :min="minValue(item)" class="form-control"></input>
                        <small>
                        Количество.<br>
                        Это поле обязательно для заполнения
                        </small>
                    </div>
                    <div class="col-sm-1">
                        <button v-show="canDelete(item)" class="btn btn-danger btn-sm pull-right" v-on:click="deleteValue(item)">
                            <i class="fas fa-trash fa-inverse"></i>
                        </button>
                    </div>
                </div><hr>
            </div>
            <button class="btn btn-primary" v-on:click="addValue">Добавить</button>
        </div>
    </div>
    `,
    props: {
        label: {default: ''},
        max: { default: 500 },
        maxItems: {
            default: 15
        }
    },
    data() {
        return {
        };
    },
    created() {
        let notFound = true
        this.results.forEach(function (item) {
            if(item.name === "Количество благополучателей" || item.name === "Количество граждан, вовлеченных в культурную деятельность путем поддержки и реализации творческих инициатив") {
                notFound = false;
            }
        })
        if(notFound) {
            this.$root.project.quant_results.push({
                "name": "Количество благополучателей",
                "status": "new",
                "count": 0,
                "guid": uuidv4()
            })
        }
    },
    computed: {
        results() {
            return this.$root.project.quant_results.filter(v => (v.status !== "delete"))
        },
    },
    methods: {
        minValue(item) {
            if(item.name === "Количество благополучателей" || item.name === "Количество граждан, вовлеченных в культурную деятельность путем поддержки и реализации творческих инициатив") {
                return 50
            }

            return 1
        },
        addValue() {
            if (this.results.length < this.maxItems) {
                this.$root.project.quant_results.push({
                    "name": "",
                    "status": "new",
                    "count": 0,
                    "guid": uuidv4()
                })
            }
        },
        canDelete(v) {
            //return true
            return v.name !== "Количество благополучателей" && v.name !== "Количество граждан, вовлеченных в культурную деятельность путем поддержки и реализации творческих инициатив"
        },
        deleteValue($v) {
            if (window.confirm("Вы действительно хотите удалить этот элемент?")) { 
                $v.status = "delete"
            }
        }
    }
});