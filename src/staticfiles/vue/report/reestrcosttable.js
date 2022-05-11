Vue.component('reestrcosttable', {
    template: `
    <div>
        <modal :name="mtype" height='630'>
            <div class="mdialog" style="padding: 16px">
                <div class="form-group">
                    <label>Наименование (вид) расхода</label>
                    <textarea v-model="row.name" class="form-control" rows="2"></textarea>
                </div>
                <div class="form-group">
                    <label>Дата расхода</label>
                    <vuejs-datepicker format="dd.MM.yyyy" class="form-control" v-model="row.date" :language="ru">
                    </vuejs-datepicker>
                </div>
                <div class="form-group">
                    <label>Сумма (рублей)</label>
                    <input type="number" lang="en" v-model.number="row.cost" class="form-control"></input>
                </div>
                <div class="form-group">
                    <label>Документы, подтверждающие осуществление расходов</label>
                    <textarea v-model="row.documents" class="form-control" rows="5"></textarea>
                </div>
                <button class="btn btn-primary" v-on:click="addRow">Сохранить</button>
            </div>
            
        </modal>
        <div class="row" style="background: #ebf6fe; padding: 8px">
            <div class="col-sm-10"><h4 >{{label}}</h4></div>
            <div class="col-sm-2 align-bottom">
                <button class="btn btn-info btn-sm" v-on:click="showModal">Добавить строку</button>
            </div>
        </div>
        <table class="table">
            <thead>
                <tr>
                    <th scope="col">№ п/п</th>
                    <th scope="col">Наименование (вид) расхода</th>
                    <th width="140px" scope="col">Дата расхода</th>
                    <th scope="col">Сумма расходов</th>
                    <th scope="col">Документы, подтверждающие осуществление расходов</th>
                    <th width="100px"></th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(item, index) in filteredValues">
                    <td>{{index+1}}</td>
                    <td>{{item.name}}</td>
                    <td>{{formatDate(item.date)}}</td>
                    <td>{{item.cost}}</td>
                    <td>{{item.documents}}</td>
                    <td>
                        <a class="btn btn-primary btn-sm" v-on:click="showUpdateModal(item)"><i class="fas fa-pen fa-inverse"></i></a>
                        <a class="btn btn-danger btn-sm" v-on:click="deleteRow(item)"><i class="fas fa-trash fa-inverse"></i></a>
                    </td>
                </tr>
                <tr>
                    <td></td>
                    <td></td>
                    <td><b>Итого</b></td>
                    <td><b>{{total_cost}}</b></td>
                    <td></td>
                </tr>
            </tbody>
        </table>
    </div>
    `,
    props: {
        label: { required: true },
    },
    components: {
        vuejsDatepicker,
    },
    data() {
        return {
            values: [],
            row: {
                name: '',

                cost: 0,
                documents: '',
            },
            addNew: true,
            ru: vdp_translation_ru.js,
            mtype: 'reestrcost'
        };
    },
    computed: {
        filteredValues() {
            if (this.$root.report.cost.reestr_items === undefined) {
                this.$root.report.cost['reestr_items'] = []
            }
            return this.$root.report.cost.reestr_items
        },
        total_cost() {
            sum = 0
            this.filteredValues.forEach(value => {
                sum += value.cost
            });
            return sum.toFixed(2);
        },
    },
    methods: {
        formatDate(date) {
            const d = new Date(date)
            const dtf = new Intl.DateTimeFormat('ru', { year: 'numeric', month: 'long', day: '2-digit' })
            const [{ value: da },,{ value: mo },,{ value: ye }] = dtf.formatToParts(d)

            return `${da} ${mo} ${ye}`
        },
        clearRow() {
            this.row = {
                name: '',
                cost: 0,
            }
        },
        addRow() {
            if(this.addNew) {
                this.$root.report.cost.reestr_items.push(Object.assign({}, this.row))
            }
            this.clearRow()
            this.$modal.hide(this.mtype)
        },
        deleteRow(item) {
            if (window.confirm("Вы действительно хотите удалить этот элемент?")) {
                this.$root.report.cost.reestr_items.splice(this.$root.report.cost.reestr_items.indexOf(item), 1)
            }
        },
        showUpdateModal(value) {
            this.addNew = false
            this.row = value
            this.$modal.show(this.mtype)
        },
        showModal() {
            this.addNew = true
            this.clearRow()
            this.$modal.show(this.mtype)
        },
    }
})
