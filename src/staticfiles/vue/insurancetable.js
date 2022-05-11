Vue.component('insurancetable', {
    template: `
    <div>
        <modal :name="mtype" height='400' width="650">
            <div class="mdialog" style="padding: 16px">
                <div class="form-group">
                    <label>Страховой взнос</label>
                    <textarea v-model="row.name" class="form-control" rows="2"></textarea>
                </div>
                <div class="row">
                    <div class="form-group col-sm-6">
                        <label>Общая сумма (в рублях)</label>
                        <input v-model="row.cost" class="form-control" type="number"></input>
                    </div>
                    <div class="form-group col-sm-6">
                        <label>Софинансирование в рублях</label>
                        <input v-model="row.co_financing" class="form-control" type="number"></input>
                    </div>
                </div>
                
                <div class="form-group">
                    <label>Комментарий</label>
                    <textarea v-model="row.comment" class="form-control" rows="3"></textarea>
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
                    <th scope="col"></th>
                    <th scope="col">Общая стоимость</th>
                    <th scope="col">Софинансирование</th>
                    <th scope="col">Запрашиваемая сумма</th>
                    <th width="100px"></th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="item in filteredValues">
                    <td>{{item.name}}</td>
                    <td>{{item.cost * item.items_count}}</td>
                    <td>{{item.co_financing}}</td>
                    <td>{{item.cost * item.items_count - item.co_financing}}</td>
                    <td>
                        <a class="btn btn-primary btn-sm" v-on:click="showUpdateModal(item)"><i class="fas fa-pen fa-inverse"></i></a>
                        <a class="btn btn-danger btn-sm" v-on:click="deleteRow(item)"><i class="fas fa-trash fa-inverse"></i></a>
                    </td>
                </tr>
                <tr>
                    <td><b>Итого</b></td>
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
                items_count: 1,
                co_financing: 0,
                comment: '',
                type: this.mtype,
                status: 'new'
            },
            mtype: 'insurance',
            addNew: true,
        };
    },
    computed: {
        filteredValues() {
            return this.$root.project.generic_costs.filter(v => (v.status !== "delete" && v.type === this.mtype))
        },
        fot_cost() {
            fots = this.$root.project.generic_costs.filter(v => (v.status !== "delete" && (v.type === 'salary' || v.type === 'payouts')));
            sum = 0;
            fots.forEach(value => {
                sum += value.cost * value.items_count
            });
            return sum
        },
        total_cost() {
            sum = 0
            this.filteredValues.forEach(value => {
                sum += value.cost * value.items_count
            });
            return sum
        },
        total_co_financing() {
            sum = 0
            this.filteredValues.forEach(value => {
                sum += 1 * value.co_financing
            });
            return sum
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
            return sum1 - sum2
        },
    },
    methods: {
        clearRow() {
            this.row = {
                name: '',
                cost: 0,
                items_count: 1,
                co_financing: 0,
                comment: '',
                type: this.mtype,
                status: 'new',
                guid: uuidv4()
            }
        },
        addRow() {
            let sum = parseFloat(this.total_cost)
            if(this.addNew) sum += parseFloat(this.row.cost);
            if(sum > (this.fot_cost * 0.302)) {
                this.row.cost = 0;
                window.confirm("Сумма страховых взносов " + sum + " не должна превышать 30.2% от ФОТ (" + this.fot_cost + ")");
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