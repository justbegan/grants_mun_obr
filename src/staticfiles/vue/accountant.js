Vue.component('accountant', {
    template: `
    <div class="form-group">
        <div class="row">
            <label class="col-sm-4 col-form-label">
                17.1. Главный бухгалтер:
            </label>
            <div class="col-sm-8">
                <select class="form-control" v-model="content.type">
                    <option>ведение бухгалтерского учёта возложено на руководителя</option>
                    <option>ведение бухгалтерского учёта возложено на другого работника организации</option>
                    <option>ведение бухгалтерского учёта передано по договору индивидуальному предпринимателю</option>
                </select>
            </div>
        </div>
        <div class="row">
            <label class="col-sm-4 col-form-label">
                17.2. ФИО главного бухгалтера:
            </label>
            <div class="col-sm-8">
                <input required="required" v-model="content.fio" class="form-control" rows="5" @input="handleInput"></input>
            </div>
        </div>
    </div>
    `,
    props: {
        value: { required: true },
    },
    
    computed: {
        content() {
            if(this.value) {
                return this.value
            } else {
                return {
                    type: '',
                    name: ''
                }
            }
        }
    },
    methods: {
        handleInput(e) {
            this.$emit('input', this.content)
        }
    }
});