Vue.component('plantable', {
    template: `
    <div>
        <modal name="event-modal" height='610'>
            <div style="padding: 16px">                
                <div class="form-group row">
                <label class="col-sm-4 col-form-label">
                    Решаемая задача
                </label>
                <div class="col-sm-8">
                    <select required v-model="event.job_id" class="form-control">
                        <option value="" selected disabled>Выбрать задачу</option>
                        <option v-for="item in jobs" :key="item.id" :value="item.id">
                            {{item.content}}
                        </option>
                    </select>
                </div>
                </div>
                <onetext required label="Мероприятие, его содержание, место проведения" v-model="event.name" max=300 description=""></onetext>
                <div class="form-group row">
                <label class="col-sm-4 col-form-label">
                    Дата начала
                </label>
                <div class="col-sm-8">
                    <date-picker required value-type="YYYY-MM-DD" format="DD.MM.YYYY" v-model="event.start_date" 
                        :disabled-date="disabledDates" lang="ru">
                    </date-picker>
                </div>
                </div>
                <div class="form-group row">
                <label class="col-sm-4 col-form-label">
                    Дата окончания
                </label>
                <div class="col-sm-8">
                     <date-picker required value-type="YYYY-MM-DD" format="DD.MM.YYYY" v-model="event.finish_date" 
                        :disabled-date="disabledDates" lang="ru">
                    </date-picker>
                </div>
                </div>
                <onetext required label="Ожидаемые результаты" v-model="event.result" max=3000 description=""></onetext>
                <br>
                <button class="btn btn-primary" v-on:click="addRow">Сохранить</button>
            </div>
        </modal>

        <div class="row" style="background: #ebf6fe; padding: 8px">
            <div class="col-sm-10"></div>
            <div class="col-sm-2"><button class="btn btn-info btn-sm" v-on:click="showModal">Добавить строку</button><br></div>
        </div>
        <table class="table">
            <thead>
                <tr>
                    <th scope="col">№</th>
                    <th scope="col">Решаемая задача</th>
                    <th scope="col">Мероприятие, его содержание, место проведения</th>
                    <th scope="col" width="150px">Дата начала</th>
                    <th scope="col" width="150px">Дата окончания</th>
                    <th scope="col">Ожидаемые результаты</th>
                    <th width="90px"></th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(event, index)  in filteredValues">
                    <td>{{index+1}}</td>
                    <td>{{jobs.find(x => x.id === event.job_id).content }}</td>
                    <td>{{event.name}}</td>
                    <td>{{formatDate(event.start_date)}}</td>
                    <td>{{formatDate(event.finish_date)}}</td>
                    <td>{{event.result}}</td>
                    <td>
                    <a class="btn btn-primary btn-sm" v-on:click="showUpdateModal(event)"><i class="fas fa-pen fa-inverse"></i></a>
                    <a class="btn btn-danger btn-sm" v-on:click="deleteRow(event)"><i class="fas fa-trash fa-inverse"></i></a>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
    `,
    components: {
        vuejsDatepicker,
        DatePicker,
    },
    props: {
        value: {required: true},
        jobs: {required: true},
    },
    data() {
        return {
            events: [],
            pjobs: [],
            event: {
                job_id: '',
                start_date: '',
                finish_date: '',
                name: '',
                result: '',
                status: 'new',
            },
            ru: vdp_translation_ru.js,
            addNew: true,
        };
    },
    computed: {
        filteredValues() {
            return this.$root.project.events.filter(e => e.status !== "delete")
        },
    },
    created: function () {
        this.events = this.value
        this.pjobs = this.jobs
    },
    methods: {
        formatDate(date) {
            const d = new Date(date)
            const dtf = new Intl.DateTimeFormat('ru', {year: 'numeric', month: 'long', day: '2-digit'})
            const [{value: da}, , {value: mo}, , {value: ye}] = dtf.formatToParts(d)

            return `${da} ${mo} ${ye}`
        },
        addRow() {
            if (this.event.job_id === '' || this.event.name === ''
                || this.event.start_date === undefined || this.event.finish_date === undefined || this.event.result === '') {
                window.confirm("Заполните все поля")
                return
            }
            if (this.addNew) {
                this.events.push(Object.assign({}, this.event))
            }
            this.event = {
                job_id: '',
                start_date: undefined,
                finish_date: undefined,
                name: '',
                result: '',
                status: 'new',
                guid: uuidv4()
            }
            this.$emit('input', this.events)
            this.$modal.hide("event-modal")
        },
        showModal() {
            this.event = {
                job_id: '',
                start_date: '',
                finish_date: '',
                name: '',
                result: '',
                status: 'new',
                guid: uuidv4()
            }
            this.addNew = true
            this.$modal.show("event-modal")
        },
        showUpdateModal(value) {
            this.addNew = false
            this.event = value
            this.$modal.show("event-modal")
        },
        deleteRow(event) {
            if (window.confirm("Вы действительно хотите удалить этот элемент?")) {
                event.status = "delete"
            }
        },
        disabledDates(date) {
          const startDate = new Date(new Date().getFullYear(), 5, 1);
          const finishDate = new Date(new Date().getFullYear() + 1, 5, 1);

          return date < startDate || date > finishDate;
        },
    }
});