Vue.component('upload', {
    template: `
    <div>
        <ul>
            <li v-for="file in files">
                <a :href="downloadUrl(file)" target="_blank">{{file.name}}</a>
                <button v-if="canDelete(file)" class="btn btn-link btn-sm" v-on:click="deleteFile(file)">
                    <i class="fas fa-trash"></i>
                </button>
            </li>
        </ul>
        <div v-show="canUpload">
            <file-upload :size="max_size" :headers="csrfToken" class="btn btn-primary btn-sm"
                @input="updateValue"
                ref="upload"
                v-model="uploadFiles"
                name="file"
                :extensions="extensions"
                :maximum="1"
                :input-id="type"
                :post-action="uploadUrl">
            Выбрать файл
            </file-upload>
            <button v-show="!$refs.upload || !$refs.upload.active" @click.prevent="$refs.upload.active = true" type="button">
                Загрузить
            </button>
            
            <ul>
                <li v-for="file in uploadFiles">
                    {{file.name}} 
                    <span v-if="file.active" class="text-info">- Файл загружается ({{file.speed / 1024 / 1024}} Mb/s)</span>
                    <div v-if="file.active" class="progress">
                        <div class="progress-bar" role="progressbar" :style="'width: ' + file.progress + '%'" :aria-valuenow="file.progress" aria-valuemin="0" aria-valuemax="100">{{file.progress}}%</div>
                    </div>
                    <span v-if="file.error" class="text-danger">{{error[file.error]}}</span>
                </li>
            </ul>
        </div>
    </div>
    `,
    props: {
        csrf_token: { required: true },
        type: { required: true },
        project_id: { required: true },
        max_size: { default: 1024 * 1024 * 50 },
        extensions: { default: 'pdf' },
        maxItems: {
            default: 15
        },
    },
    data() {
        return {
            uploadFiles: [],
            error: {
                'size': 'слишком большой размер файла (максимальный размер 50мб)',
                'extension': 'не правильный формат', 
                'timeout': 'истекло время ожидания', 
                'abort': 'отменено', 
                'network': 'проблема с сетью', 
                'server': 'ошибка сервера', 
                'denied': 'доступ запрещен'
            }
        }
    },
    components: {
        FileUpload: VueUploadComponent,
    },
    computed: {
        uploadUrl() {
            return '/user/upload-file/' + this.type + "/" + this.project_id
        },
        deleteUrl() {
            return '/user/delete-file'
        },
        csrfToken() {
            return {'X-CSRFToken': this.csrf_token}
        },
        files() {
            return this.$root.project["project_files"].filter(v => (v.type === this.type))
        },
        canUpload() {
            if(this.type === 'organization_egrul') {
                return false
            }
            return this.maxItems > this.files.length;
        }
    },
    
    methods: {
        downloadUrl(file) {
            return file.url || '/media/' + file.name;
        },
        updateValue(values) {
            for (const [i, value] of values.entries()) {
                if (value.success) {
                    this.$root.project["project_files"].push(value.response.file);
                    this.uploadFiles.splice(i, 1);
                }
            }
        },
        canDelete(file) {
            return !(file.type === "organization_egrul" && file.name.includes('contur/', 0) && this.files.length <= 1);
        },
        async deleteFile(file) {
            if (window.confirm("Вы действительно хотите удалить этот файл?")) { 
                if(file.id){
                    const response = await fetch(this.deleteUrl + "/" +file.id)
                    res = await response.json();
                    if (res.status === "ok") {
                        this.$root.project["project_files"].splice(this.$root.project["project_files"].indexOf(file), 1);
                    }
                } else {
                    this.$root.project["project_files"].splice(this.$root.project["project_files"].indexOf(file), 1);
                }
                //console.log(res);
            }
        }
    }
});