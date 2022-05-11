Vue.component('oneinput', {
    template: `
    <div class="form-group row">
        <label class="col-sm-4 col-form-label">
            {{ label }}
        </label>
        <div class="col-sm-8">
            <input v-if="!mask" :type="type" 
                    :required="required" 
                    :readonly="readonly" 
                    :maxlength="max"
                    v-model="content" 
                    class="form-control" 
                    @input="handleInput"></input>
            <input v-if="mask" :type="type" 
                    :required="required" 
                    :readonly="readonly" 
                    v-mask="mask" 
                    v-model="content" 
                    class="form-control" 
                    @input="handleInput"></input>
            <small class="text-danger">{{error}}</small>
            <small v-if="content && type == 'text' && !mask">
                Осталось символов: <span v-text="(max - content.length)"> </span>
            </small>
            <small>
                <div v-if="required">Данное поле обязательно для заполнения.</div>
                {{ description }}
            </small>
        </div>
    </div>
    `,
    props: {
        label: { required: true },
        value: { required: true },
        description: { required: true },
        max: { default: 500 },
        required: {default: false},
        type: { default: 'text' },
        validator: { default: 'no' },
        mask: { default: false },
        max2: { default: false },
        readonly: { default: false },
    },
    data() {
        return {
            content: this.value,
            error: '',
        }
    },
    watch: {
        value(v){
            return this.content = v
        }
    },
    methods: {
        lengthValidator() {
            if(this.max2) {
                if (this.content.length == this.max || this.content.length == this.max2) {
                    this.error = ""
                    return true
                }
                this.error = "количество символов должно быть " + this.max + ", либо " + this.max2
                return  false
            } else {
                if (this.content.length < this.max) {
                    this.error = "количество символов должно быть " + this.max
                    return false
                }
            }
            this.error = ""
            return true
        },
        handleInput(e) {
            if(this.validator === 'length') {
                if(this.lengthValidator()){
                    this.$emit('input', this.content)
                }
            } else {
                this.$emit('input', this.content)
            }
        }
    }
});

Vue.component('onetext', {
    template: `
    <div class="form-group row">
        <label class="col-sm-4 col-form-label">
            {{ label }}
        </label>
        <div class="col-sm-8">
            <textarea :required="required" :readonly="readonly"  :maxlength="max" v-model="content" class="form-control" rows="5" @input="handleInput"></textarea>
            <small v-if="content">
                Осталось символов: <span v-text="(max - content.length)"> </span>
            </small>
            <small>
                <div v-if="required">Данное поле обязательно для заполнения.</div>
                {{ description }}
            </small>
        </div>
    </div>
    `,
    props: {
        label: { required: true },
        value: { required: true },
        description: { required: true },
        max: { default: 500 },
        required: { default: false },
        readonly: { default: false },
    },
    data() {
        return {
            content: this.value
        }
    },
    watch: {
        value(v){
            return this.content = v
        }
    },
    computed: {
        charactersLeft() {
            if(typeof comment !== 'undefined' && this.content) {
                charCount = content.length
            } else {
                charCount = 0
            }
            return this.max - charCount
        }
    },
    methods: {
        handleInput(e) {
            this.$emit('input', this.content)
        }
    }
});

Vue.component('multitext', {
    template: `
    <div class="form-group row">
        <label class="col-sm-4 col-form-label">
            {{ label }}
        </label>
        <div class="col-sm-8">
            <div v-for="item in filteredValues">
                <textarea :required="required"  :maxlength="max" v-model="item.content" class="form-control" :rows="rows"></textarea>
                <div class="row"> 
                    <div class="col-sm-11">
                        <small>Осталось символов: <span v-text="(max - item.content.length)"></span> <br>
                        <div v-if="required">Данное поле обязательно для заполнения.</div>
                        {{ description }}</small>
                    </div>
                    <div class="col-sm-1">
                        <button class="btn btn-danger btn-sm pull-right" v-on:click="deleteValue(item)">
                            <i class="fas fa-trash fa-inverse"></i>
                        </button>
                    </div>
                </div>
               
                
            </div>
            <button class="btn btn-primary btn-sm" v-on:click="addValue">Добавить</button>
        </div>
    </div>
    `,
    props: {
        label: { required: true },
        value: { required: true },
        description: { required: true },
        max: { default: 500 },
        required: { default: false },
        maxItems: {
            default: 5
        },
        rows: { default: 5 },
        forceDelete: {default: false}
    },
    data() {
        return { values: [] };
    },
    computed: {
        filteredValues() {
            return this.values.filter(v => v.status !== "delete")
        }
    },
    created: function () {
        this.values = this.value
    },
    methods: {
        addValue() {
            if (this.filteredValues.length < this.maxItems) {
                this.values.push({
                    "content": "",
                    "status": "new",
                    "guid": uuidv4()
                })
            }
        },
        deleteValue(item) {
            if (window.confirm("Вы действительно хотите удалить этот элемент?")) { 
                if(this.forceDelete) {
                    this.values.splice(this.values.indexOf(item), 1)
                } else {
                    item.status = "delete"
                }
            }
        }
    }
});