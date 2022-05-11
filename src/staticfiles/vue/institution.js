Vue.component('institution', {
    template: `
    <div class="form-group">
        <div class="row">
            <label class="col-sm-12">
                <b>{{ label }}:</b>
            </label>
        </div>
        <div v-for="item in filteredValues"> 
            <div class="row"> 
                <div class="col-sm-4">
                    <span v-if="type=='education'">Образовательная организация</span>
                    <span v-if="type=='work'">Организация</span>
                </div>
                <div class="col-sm-8">
                    <textarea required maxlength="200" v-model="item.organization" class="form-control" rows="2"></textarea>
                    <small>Осталось символов: <span v-text="(200 - item.organization.length)"></span> <br>
                    Данное поле обязательно для заполнения.<br></small>
                </div>
            </div>
            
            <div class="row"> 
                <div class="col-sm-4">
                    <span v-if="type=='education'">Специальность</span>
                    <span v-if="type=='work'">Должность</span>
                </div>
                <div class="col-sm-8">
                    <input required maxlength="100" v-model="item.position" class="form-control" rows="2"></input>
                    <small>Осталось символов: <span v-text="(100 - item.position.length)"></span> <br>
                    Данное поле обязательно для заполнения.</small>
                </div>
            </div>

            <div class="row"> 
                <div class="col-sm-4">
                    <span v-if="type=='education'">Дата поступления</span>
                    <span v-if="type=='work'">Дата начала работы</span>
                </div>
                <div class="col-sm-8">
                    <date-picker value-type="YYYY-MM-DD" format="YYYY" type="year" v-model="item.start_date" lang="ru">
                    </date-picker><br>
                    <small>Данное поле обязательно для заполнения.</small>
                </div>
            </div>

            <div class="row"> 
                <div class="col-sm-4">
                    <span v-if="type=='education'">Дата окончания</span>
                    <span v-if="type=='work'">Дата окончания работы</span>
                </div>
                <div class="col-sm-8">
                    <input type="checkbox" class="form-check-input" v-model="item.in_present" @change="item.finish_date = ''">
                    <label class="form-check-label">По настоящее время</label><br>
                    <date-picker v-if="!item.in_present" value-type="YYYY-MM-DD" format="YYYY" type="year" v-model="item.finish_date" lang="ru">
                    </date-picker><br>
                    <small>Данное поле обязательно для заполнения.</small>
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
        <button class="btn btn-primary btn-sm" v-on:click="addValue">Добавить</button>
    </div>
    `,
    components: {
        vuejsDatepicker,
        DatePicker,
    },
    props: {
        label: { required: true },
        member_id: { default: null },
        manager_id: { default: null },
        type: { required: true },
    },
    computed: {
        filteredValues() {
            if(!!this.member_id) {
                return this.$root.project
                            .institutions
                            .filter(v => (v.status !== "delete" && v.type === this.type && v.member_id === this.member_id))
            }

            if(!!this.manager_id !== null) {
                return this.$root.project
                            .institutions
                            .filter(v => (v.status !== "delete" && v.type === this.type && v.manager_id === this.manager_id))
            }
        }
    },
    data() {
        return { 
            ru: vdp_translation_ru.js,
        };
    },
    methods: {
        addValue() {
            this.$root.project.institutions.push({
                "organization": "",
                "position": "",
                "start_date": "",
                "finish_date": "",
                "status": "new",
                "member_id": this.member_id,
                "manager_id": this.manager_id,
                "type": this.type,
                "guid": uuidv4()
            })
        },
        deleteValue($v) {
            if (window.confirm("Вы действительно хотите удалить этот элемент?")) { 
                $v.status = "delete"
            }
        }
    }
});