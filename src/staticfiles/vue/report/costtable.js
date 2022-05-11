Vue.component('costtable', {
    template: `
    <div>
        <modal :name="mtype" height='350'>
            <div class="mdialog" style="padding: 16px">
                <div class="form-group">
                    <label>Источники софинансирования расходов на реализацию программы</label>
                    <textarea v-model="row.name" class="form-control" rows="5"></textarea>
                </div>
                <div class="form-group">
                    <label>Сумма расходов (рублей)</label>
                    <input type="number" lang="en" v-model.number="row.cost" class="form-control"></input>
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
                    <th scope="col">Источники софинансирования расходов на реализацию программы</th>
                    <th scope="col">Сумма расходов (рублей)</th>
                    <th width="100px"></th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(item, index) in filteredValues">
                    <td>{{index+1}}</td>
                    <td>{{item.name}}</td>
                    <td>{{item.cost}}</td>
                    <td>
                        <a class="btn btn-primary btn-sm" v-on:click="showUpdateModal(item)"><i class="fas fa-pen fa-inverse"></i></a>
                        <a class="btn btn-danger btn-sm" v-on:click="deleteRow(item)"><i class="fas fa-trash fa-inverse"></i></a>
                    </td>
                </tr>
                <tr>
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
    data() {
        return {
            values: [],
            row: {
                name: '',
                cost: 0,
            },
            addNew: true,
            mtype: 'cost'
        };
    },
    computed: {
        filteredValues() {
            if (this.$root.report.cost.social_items === undefined) {
                this.$root.report.cost['social_items'] = []
            }
            return this.$root.report.cost.social_items
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
        clearRow() {
            this.row = {
                name: '',
                cost: 0,
            }
        },
        addRow() {
            if(this.addNew) {
                this.$root.report.cost.social_items.push(Object.assign({}, this.row))
            }
            this.clearRow()
            this.$modal.hide(this.mtype)
        },
        deleteRow(item) {
            if (window.confirm("Вы действительно хотите удалить этот элемент?")) {
                this.$root.report.cost.social_items.splice(this.$root.report.cost.social_items.indexOf(item), 1)
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
