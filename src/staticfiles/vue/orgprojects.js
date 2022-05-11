Vue.component('orgprojects', {
    template: `
    <div class="form-group">
        <div class="row">
            <label class="col-sm-12">
                22. Основные реализованные проекты и программы за последние 5 лет:
            </label>
        </div>
        <div v-for="item in filteredValues"> 
            <div class="row"> 
                <div class="col-sm-4">
                    Дата начала
                </div>
                <div class="col-sm-8">
                    <date-picker value-type="YYYY-MM-DD" format="DD.MM.YYYY" v-model="item.start_date" lang="ru">
                    </date-picker><br>
                </div>
            </div>

            <div class="row"> 
                <div class="col-sm-4">
                    Дата окончания
                </div>
                <div class="col-sm-8">
                    <date-picker value-type="YYYY-MM-DD" format="DD.MM.YYYY" v-model="item.finish_date" lang="ru">
                    </date-picker><br>
                    <small>Данное поле обязательно для заполнения.</small>
                </div>
            </div>

            <div class="row"> 
                <div class="col-sm-4">
                    Название проекта
                </div>
                <div class="col-sm-8">
                    <input required maxlength="200" v-model="item.name" class="form-control"></input>
                    <small>Осталось символов: <span v-text="(200 - item.name.length)"></span> <br></small>
                </div>
            </div>
            
            <div class="row"> 
                <div class="col-sm-4">
                    Объем финансирования (в руб.):
                </div>
                <div class="col-sm-8">
                    <input required type="number" v-model="item.finance" class="form-control"></input>
                </div>
            </div>

            <div class="row"> 
                <div class="col-sm-4">
                    Источники финансирования:
                </div>
                <div class="col-sm-8">
                    <autocomplete :minMatchingChars="0" ref="typeahead" v-model="item.finance_source" :data="finances" >
                    </autocomplete>
                </div>
            </div>

            <div class="row"> 
                <div class="col-sm-4">
                    Основные результаты:
                </div>
                <div class="col-sm-8">
                    <textarea required maxlength="3000" v-model="item.results" class="form-control" rows="5"></textarea>
                    <small>Осталось символов: <span v-text="(3000 - item.results.length)"></span> <br></small>
                </div>
            </div>

            <div class="row"> 
                <div class="col-sm-10">
                </div>
                <div class="col-sm-2">
                    <button class="btn btn-danger btn-sm pull-right" v-on:click="deleteValue(item)">
                        <i class="fas fa-trash fa-inverse"></i>
                    </button>
                </div>
            </div>
            <hr>
        </div>
        <button class="btn btn-primary btn-sm" v-on:click="addValue">Добавить проект</button>
    </div>
    `,
    components: {
        vuejsDatepicker,
        DatePicker,
        autocomplete: VueBootstrapTypeahead
    },
    props: {
    },
    computed: {
        filteredValues() {
            return this.$root.project.organization.success_projects
        }
    },
    data() {
        return { 
            ru: vdp_translation_ru.js,
            finances: [
                'Субсидия (грант) из местного бюджета',
                'Субсидия (грант) из регионального бюджета',
                'Субсидия (грант) из федерального бюджета'
            ]
        };
    },
    methods: {
    
        addValue() {
            if (this.$root.project.organization.success_projects.length < 5) {
                this.$root.project.organization.success_projects.push({
                    "start_date": "",
                    "finish_date": "",
                    "name": "",
                    "finance": "",
                    "finance_source": "",
                    "results": "",
                })
            }
        },
        deleteValue(item) {
            if (window.confirm("Вы действительно хотите удалить этот элемент?")) { 
                item.status = "delete"
                this.$root.project.organization.success_projects.splice(this.$root.project.organization.success_projects.indexOf(item), 1)
            }
        }
    }
});