Vue.component('moneytable', {
    template: `
    <div>
        <modal :name="mtype" height='450' width="650">
            <div class="mdialog" style="padding: 16px">
                <div class="form-group">
                    <label>{{col1}}</label>
                    <textarea v-model="row.name" class="form-control" rows="2"></textarea>
                </div>
                <div class="row">
                    <div class="col-sm-4">
                        <label>{{col2}}</label>
                        <input type="number" lang="en" v-model="row.cost" class="form-control"></input>
                    </div>
                    <div class="col-sm-4"  style="height: 100px">
                        <label style="min-height: 48px">{{col3}}</label>
                        <input type="number" v-model="row.items_count" class="form-control" ></input>
                    </div>
                    <div class="col-sm-4">
                        <label>Софинансирование в рублях</label>
                        <input type="number" v-model="row.co_financing" class="form-control"></input>
                    </div>
                </div>
                <div class="form-group">
                    <label>Комментарий</label>
                    <textarea v-model="row.comment" class="form-control" rows="3"></textarea>
                    <small>Количество символов: {{row.comment.length}}</small>
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
                    <th scope="col">{{col1}}</th>
                    <th scope="col">{{col2}}</th>
                    <th scope="col">{{col3}}</th>
                    <th scope="col">Общая стоимость</th>
                    <th scope="col">Софинансирование</th>
                    <th scope="col">Запрашиваемая сумма</th>
                    <th width="100px"></th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="item in filteredValues">
                    <td>{{item.name}}</td>
                    <td>{{item.cost}}</td>
                    <td>{{item.items_count}}</td>
                    <td>{{item.cost * item.items_count}}</td>
                    <td>{{item.co_financing}}</td>
                    <td>{{item.cost * item.items_count - item.co_financing}}</td>
                    <td>
                        <a class="btn btn-primary btn-sm" v-on:click="showUpdateModal(item)"><i class="fas fa-pen fa-inverse"></i></a>
                        <a class="btn btn-danger btn-sm" v-on:click="deleteRow(item)"><i class="fas fa-trash fa-inverse"></i></a>
                    </td>
                </tr>
                <tr>
                    <td colspan="3"><b>Итого</b></td>
                    <td><b>{{total_cost}}</b></td>
                    <td><b>{{total_co_financing}}</b></td>
                    <td><b>{{total_request_sum}}</b></td>
                    <td></td>
                </tr>
            </tbody>
        </table>
    </div>
    `,
    props: {
        col1: { required: true },
        col2: { required: true },
        col3: { required: true },
        label: { required: true },
        type: { required: true },
    },
    data() {
        return {
            values: [],
            row: {
                name: '',
                cost: 0,
                items_count: 0,
                co_financing: 0,
                comment: '',
                type: this.type,
                status: 'new'
            },
            mtype: this.type,
            addNew: true,
        };
    },
    computed: {
        filteredValues() {
            return this.$root.project.generic_costs.filter(v => (v.status !== "delete" && v.type === this.mtype))
        },
        total_cost() {
            sum = 0
            this.filteredValues.forEach(value => {
                sum += value.cost * value.items_count
            });
            return sum.toFixed(2);
        },
        total_co_financing() {
            sum = 0
            this.filteredValues.forEach(value => {
                sum += 1 * value.co_financing
            });
            return sum.toFixed(2);
        },
        total_request_sum() {
            sum1 = 0
            this.filteredValues.forEach(value => {
                sum1 += value.cost * value.items_count
            });

            sum2 = 0
            this.filteredValues.forEach(value => {
                sum2 += 1 * value.co_financing
            });
            return (sum1 - sum2).toFixed(2);
        },
    },
    methods: {
        clearRow() {
            this.row = {
                name: '',
                cost: 0,
                items_count: 0,
                co_financing: 0,
                comment: '',
                type: this.type,
                status: 'new',
                guid: uuidv4()
            }
        },
        addRow() {
            if (this.row.name === '' || this.row.comment === '')  {
                window.confirm("Заполните все поля")
                return
            }
            if (this.row.comment.length < 100)  {
                window.confirm("Длина комментария не должна быть меньше 100 символов")
                return
            }
            if(this.addNew) {
                this.$root.project.generic_costs.push(Object.assign({}, this.row))
            }
            this.clearRow()
            this.$modal.hide(this.mtype)
        },
        deleteRow(item) {
            if (window.confirm("Вы действительно хотите удалить этот элемент?")) { 
                item.status = "delete"
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
        }
    }
});

Vue.component('totalmoney', {
    template: `
    <div>
    <table class="table">
        <thead>
            <tr>
                <th scope="col" rowspan="3"></th>
                <th scope="col"><b>Общая сумма расходов на реализацию проекта</b></th>
                <th scope="col"><b>Софинансирование</b></th>
                <th scope="col"><b>Запрашиваемая сумма гранта</b></th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><b>ИТОГО</b></td>
                <td>{{total_money.cost_sum}}</td>
                <td>{{total_money.co_financing_sum}}</td>
                <td>{{total_money.request_sum}}</td>
            </tr>
        </tbody>
    </table>
    </div>
    `,
    props: {
        value: { required: true },
    },
    data() {
        return { 
            values: [],
        };
    },
     computed: {
        filteredValues() {
            return this.$root.project.generic_costs.filter(v => (v.status !== "delete" ))
        },
        total_money() {
            cost_sum = 0
            co_financing_sum = 0

            this.filteredValues.forEach(value => {
                cost_sum += value.items_count * value.cost
                co_financing_sum +=  1 * value.co_financing
            });

            return {
                cost_sum: cost_sum.toFixed(2),
                co_financing_sum: co_financing_sum.toFixed(2),
                request_sum: (cost_sum - co_financing_sum).toFixed(2)
            }
        }
    },

});