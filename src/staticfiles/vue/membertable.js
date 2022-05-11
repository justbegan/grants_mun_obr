Vue.component('membertable', {
    template: `
    <div>
        <div v-for="member in filteredValues">
            <oneinput :required="true" label="1. Должность или роль участника в заявленном проекте" v-model="member.position"
                max=300 description="">
            </oneinput>
            <div class="form-group row">
                <label class="col-sm-4 col-form-label">
                    2. ФИО члена команды*
                </label>
                <div class="col-sm-8">
                    <div class="row">
                        <div class="col">
                            <input required placeholder="Фамилия" class="form-control" v-model="member.last_name">
                        </div>
                        <div class="col">
                            <input required placeholder="Имя" class="form-control" v-model="member.first_name">
                        </div>
                        <div class="col">
                            <input required placeholder="Отчество" class="form-control" v-model="member.middle_name">
                        </div>
                    </div>
                </div>
            </div> 
            <div class="form-group row">
                <label for="education" class="col-sm-4 col-form-label">
                    3. Образование
                </label>
                <div class="col-sm-8">
                    <select v-model="member.education" class="form-control" id="education">
                        <option value="" selected disabled>Выбрать образование</option>
                        <option v-for="item in educations" :value="item[0]">
                            {{ item[1] }}
                        </option>
                    </select>
                    <small>Данное поле обязательно для заполнения</small>
                </div>
            </div>

            <div v-if="member.status=='update'">
                <institution label="4. Образовательные организации и специальности" :member_id="member.id" type="education"></institution>
                <institution label="5. Опыт работы" :member_id="member.id" type="work"></institution>
            </div>

            <onetext label="6. Дополнительные сведения" v-model="member.info" max=600 description="">
            </onetext>
        
            <div class="form-group row">
                <div class="col-sm-10"></div>
                <div class="col-sm-2"> 
                    <a class="btn btn-danger btn-sm" style="color: #ffffff" v-on:click="deleteRow(member)">Удалить участника</a>
                </div>       
            </div> 
                 
            <hr><hr style=" border-top: 10px solid black;"> <hr> 
        </div>
        <button class="btn btn-primary" v-on:click="addMember">Добавить участника</button>
    </div>
    `,
    props: {
        value: { required: true },
    },
    data() {
        return { 
            members: [],
            pjobs: [],
            member: {
                position: '',
                last_name: '',
                first_name: '',
                middle_name: '',
                education: '',
                info: '',
                status: 'new',
            },
        };
    },
    computed: {
        filteredValues() {
            return this.$root.project.members.filter(v => (v.status !== "delete"))
        },
        educations() {
            return this.$root.educations
        },
    },
    created: function () {
        this.members = this.value
    },
    methods: {
        addMember() {
            return this.$root.project.members.push({
                position: '',
                last_name: '',
                first_name: '',
                middle_name: '',
                education: '',
                info: '',
                guid: uuidv4(),
                status: 'new',
            })
        },
        deleteRow(member) {
            if (window.confirm("Вы действительно хотите удалить этот элемент?")) { 
                member.status = "delete"
            }
        }
    }
});