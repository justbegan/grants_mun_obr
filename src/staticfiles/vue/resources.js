Vue.component('resources', {
    template: `
    <div class="form-group">
        <div class="row">
            <label class="col-sm-4 col-form-label">
            23. Имеющиеся в распоряжении организации материально-технические ресурсы:
            </label>
            <div class="col-sm-8">
                <textarea required="required" v-model="content.resource" class="form-control" rows="5" @input="handleInput"></textarea>
                <small>Назначение, площадь, вид права использования (аренда, в собственности)</small><br><br>
            </div>
        </div>
        <div class="row">
            <label class="col-sm-4 col-form-label">
                Оборудование:
            </label>
            <div class="col-sm-8">
                <textarea v-model="content.equipment" class="form-control" rows="5" @input="handleInput"></textarea>
                <small>Оборудование - количество единиц</small><br><br>
            </div>
        </div>
        <div class="row">
            <label class="col-sm-4 col-form-label">
            Другое:
            </label>
            <div class="col-sm-8">
                <textarea v-model="content.other" class="form-control" rows="5" @input="handleInput"></textarea>
                <small></small><br><br>
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
                    resource: '',
                    equipment: '',
                    other: '',
                    resources: []
                }
            }
        }
    },
    methods: {
        handleInput(e) {
            this.$emit('input', this.content)
        },
    }
});