Vue.component('successtable', {
    template: `
    <div>
        <modal :name="mtype" height='630'>
            <div class="mdialog" style="padding: 16px">
                <div class="form-group">
                    <label>Показатель результативности, установленный соглашением</label>
                    <textarea v-model="row.name" class="form-control" rows="2"></textarea>
                </div>
                <div class="form-group">
                    <label>Значение показателя, установленное соглашением</label>
                    <input type="number" lang="en" v-model.number="row.plan_value" class="form-control">
                </div>
                <div class="form-group">
                    <label>Фактическое значение показателя</label>
                    <input type="number" lang="en" v-model.number="row.fact_value" class="form-control"></input>
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
                    <th scope="col">Показатель результативности, установленный соглашением</th>
                    <th scope="col">Значение показателя, установленное соглашением</th>
                    <th scope="col">Фактическое значение показателя</th>
                    <th width="100px"></th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(item, index) in filteredValues">
                    <td>{{index+1}}</td>
                    <td>{{item.name}}</td>
                    <td>{{item.plan_value}}</td>
                    <td>{{item.fact_value}}</td>
                    <td>
                        <a class="btn btn-primary btn-sm" v-on:click="showUpdateModal(item)"><i class="fas fa-pen fa-inverse"></i></a>
                        <a class="btn btn-danger btn-sm" v-on:click="deleteRow(item)"><i class="fas fa-trash fa-inverse"></i></a>
                    </td>
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
            mtype: 'success'
        };
    },
    computed: {
        filteredValues() {
            if (this.$root.report.result.success_items === undefined) {
                this.$root.report.result['success_items'] = []
            }
            return this.$root.report.result.success_items
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
                this.$root.report.result.success_items.push(Object.assign({}, this.row))
            }
            this.clearRow()
            this.$modal.hide(this.mtype)
        },
        deleteRow(item) {
            if (window.confirm("Вы действительно хотите удалить этот элемент?")) {
                this.$root.report.result.success_items.splice(this.$root.report.result.success_items.indexOf(item), 1)
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
