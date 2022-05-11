Vue.component('smetatable', {
    template: `
    <div>
        <modal :name="mtype" height='700'>
            <div class="mdialog" style="padding: 16px">
                <div class="form-group">
                    <label>Наименование расходов</label>
                    <textarea v-model="row.name" class="form-control" rows="5"></textarea>
                </div>
                <div class="form-group">
                    <label>Количество единиц</label>
                    <input type="number" lang="en" v-model="row.items_count" class="form-control"></input>
                </div>
                <div class="form-group">
                    <label>Стоимость единицы (руб.)</label>
                    <input type="number" v-model="row.cost" class="form-control"></input>
                </div>
                <div class="form-group">
                    <label>Софинансирование (руб.)</label>
                    <input type="number" v-model="row.co_financing" class="form-control"></input>
                </div>
                <div class="form-group">
                    <label>Комментарий</label>
                    <textarea v-model="row.comment" class="form-control" rows="5"></textarea>
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
                    <th scope="col">Наименование расходов</th>
                    <th scope="col">Количество единиц</th>
                    <th scope="col">Стоимость единицы (руб.)</th>
                    <th scope="col">Общая стоимость (руб.)</th>
                    <th scope="col">Софинансирование (руб.)</th>
                    <th scope="col">Запрашиваемая сумма (руб.)</th>
                    <th width="100px"></th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="item in filteredValues">
                    <td>{{item.name}}</td>
                    <td>{{item.items_count}}</td>
                    <td>{{item.cost}}</td>
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
        label: { required: true },
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
            },
            addNew: true,
            mtype: 'smeta'
        };
    },
    computed: {
        filteredValues() {
            return this.$root.report.smeta
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
            }
        },
        addRow() {
            if(this.addNew) {
                this.$root.report.smeta.push(Object.assign({}, this.row))
            }
            this.clearRow()
            this.$modal.hide(this.mtype)
        },
        deleteRow(item) {
            if (window.confirm("Вы действительно хотите удалить этот элемент?")) {
                this.$root.report.smeta.splice(this.$root.report.smeta.indexOf(item), 1)
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