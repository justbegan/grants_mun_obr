
new Vue({
    el:'#vue_app',
 
    data: {

      // Для выборки 
      statements:"",
        //модель для statements
        create_st:{
          title:"",
          requested_sum:"",
          sum_expenses:"",
          source:"",
          tab_1_file_1:"",
          link:"",
          recipient_type:"",
          ogrn:"",
          egryl_info:"",
          inn:"",
          kpp:"",
          full_name_grantee:"",
          short_name_grantee:"",
          d_f_name:"",
          d_s_name:"",
          d_m_name:"",
          d_position:"",
          d_phone:"",
          d_mail:"",
          d_amount_of_overdue_debt:"",
          author:""
          


        },
        //модель для contract
        create_st_contract:{

          c_checking_account:"",
          c_bik:"",
          c_bank_name:"",
          c_correspondent_account:"",
          c_recipient_type:"",
          c_ogrn:"",
          c_full_org_name:"",
          c_short_org_name:"",
          c_jur_adress:"",
          c_fact_adress:"",
          c_inn:"",
          c_kpp:"",
          c_tel:"",
          c_mail:"",
          c_f_name:"",
          c_s_name:"",
          c_m_name:"",
          c_position:"",
          c_operates_on_the_basis:"",
          c_pdf_file:"",
          c_pdf_file_name:""




        },

        create_st_off_letter:{

          o_l_mr_go:"",
          o_l_funding_amount:"",
          o_l_req_amount:"",
          o_l_co_financing_ext_sources:"",
          o_l_recipient_OGRN:"",
          o_l_grants_operator:"",
          o_l_posision:"",
          o_l_sec_name:"",
          o_l_name:"",
          o_l_mid_name:"",
          o_l_phone:"",
          o_l_mail:"",
          o_l_phone_2:"",
          o_l_mail_2:"",
          o_l_outgoing_num:"",
          o_l_outgoing_date:"",
          o_l_copy:"",

        },




        // Из прошлого прокта
        isHidden: true,
      
        // Выбранный дикт попадает сюда и показывается
        selected_dict: this.profile_json,


        // Параметр для отображения списка или одного проекта
        projects_tab_views:"list",

        // Переменная профиль
        profile_json:"",



        // Раздел просмотра своих проектов
        // Переменная проект
        projects_json:"",
        // Для просмотра проектов
        // Для показа контрактов пользователю
        contract_json:"",
        // Для показа заявок пользователю
        statement_json:"",
        // Кон

        //Для отображения ошибок
        errors:"",
        
        
        // Проценты заполненности
        perc:"",
        perc_contract:"",
        // Кон



        // Для окна модератора
        moderator_projects:"",
        moderator_tab_views_list:true,
        moderator_statement:"",
        //Кон
        //modal
        modаl_messege:"",
        //end modal

        //header json
        headers_json:{
          "Content-Type": "application/json",
          "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
          },
        //header form_data
        headers_form:{
            "Content-Type": "multipart/form-data",
            "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
        },

        //Chat varible
        chat_messeges:"",
        create_messege_json:{
          messege:"",
          //author:541,
          statement_id: ""
        }
    },
 


    methods: {
      
      update_profile:function(){

        const vm = this
        
        vm.profile_json.author = vm.profile_json.author_id
        console.log(vm.profile_json)
        axios.post('/mun_obr/api/mun_obr_profile', vm.profile_json, {
          headers: vm.headers_json
        })
        .then(response => { 

          if(response.status >= 200 && response.status <= 226){

          vm.get_modal("authModal","Профиль обновлен")
          }
          else{

            vm.get_modal("auth_eModal","Ошибка")

          }

        })
        .catch(e => {
          
          this.errors = e.response.data
          vm.get_modal("auth_eModal","Ошибка")
        
        })


      },

      //Обрабатывает загружаемые файлы
      uploadFile(e,name) {

            console.log(name)
            //get id
            var z = e.srcElement.id
            //get file
            var file = e.target.files[0]
            var model 

            if(z=='tab_1_file_1'){

              model = this.create_st

            }
            else{
              model = this.create_st_contract
            }


            //Валидация по размеру файла 2621440
            if (file.size > 10*1024*1024) {
              e.preventDefault();
              
              model[z] = null
              
              // Показать modal
          
              document.getElementById(z).value= null;
             
            }
            
            else{
              //Прикрепить файл
              model[z] = file
    
            } 
            

            
      },


      // При открывании списка проектов
      projects(){

        const vm = this
        vm.projects_tab_views = "list"
        vm.get_projects()

      },



      // Для открытия проекта
      open_project:function(event, project_id){
        const vm = this
       
        this.projects_tab_views= "one"
        
        // axios.get('/mun_obr/api/get_contracts/'+ project_id).then(function(response){

        //   vm.contract_json = response.data
        //   console.log(vm.contract_json)          
        // });
  

        var d = vm.projects_json
        vm.statement_json = d.filter(function(val) {
        return val.id == project_id;})[0]
        
      },

      for_test(){
        const vm = this
        console.log(vm.profile_json)

      },

      onSubmit (event) {
        
        const vm = this
        var form_data = new FormData();

        var form_type = event.srcElement.id
       
          //для создания заявки
          if(form_type == "form_statement"){

            for ( var key in vm.create_st ) {
              form_data.append(key, vm.create_st[key]);
            }
            //Добавление id автора
            form_data.append('author',vm.profile_json.author_id)


            axios.post('/mun_obr/api/create_statement', form_data, {
              headers: vm.headers_form
            })
            .then(response => { 
              

              if(response.status >= 200 && response.status <= 226){

             
                vm.get_modal("authModal","Заявка успешно добавлена")
       
              
            } 

            else{

              vm.get_modal("auth_eModal","Ошибка, повторите попытку")

            }


            })
            .catch(e => {
              
              vm.errors = e.response.data
            
            })

          }

          //  Для создания контракта 
          else if(form_type = "form_contract"){


            for ( var key in this.create_st_contract ) {
              form_data.append(key, this.create_st_contract[key]);
            }
            axios.post('/mun_obr/api/create_contract', form_data, {
              headers: this.headers_form
            })
            .then(response => { 
              if(response.status >= 200 && response.status <= 226){

             
                vm.get_modal("authModal","Контракт успешно добавлен")
       
              
            } 

            else{

              vm.get_modal("auth_eModal","Ошибка, повторите попытку")

            }
            })
            .catch(e => {
              
              vm.get_modal("auth_eModal","Ошибка, повторите попытку")
            
            })


          }
      
            
      // function extend(obj, src) {
      //     for (var key in src) {
      //         if (src.hasOwnProperty(key)) obj[key] = src[key];
      //     }
      //     return obj;
      // }
        
      // var u = extend(this.create_st, this.create_st_contract)
      //console.log(u)
        
      
      },
      //Атвозаполнение из профиля
      get_data_from_profile:function(e){

              
        document.getElementById("id_ogrn").value = this.profile_json.ogrn
        document.getElementById("id_inn").value = this.profile_json.inn
 


      },

      get_projects:function(e){

        const vm = this

        axios.get('/mun_obr/api/get_projects').then(function(response){

          vm.projects_json = response.data
          
        });


      },
      // Методы модератора
      moderator_update:function(event){

        const vm = this
        var statement_id = vm.moderator_statement.id
        var data = {

          status: vm.moderator_statement.status,
          comment: vm.moderator_statement.comment

        }
    
   
        axios.put('/mun_obr/api/statement_update/'+ statement_id, data, {
          headers: vm.headers_json
        })
        .then(response => { 
          

          if(response.status >= 200 && response.status <= 226){

         
            vm.get_modal("authModal","Заявка обновлена")
   
          
        } 


        })
        .catch(e => {
          
          this.errors = e.response.data
          console.log(this.errors)
        
        })



      },

      open_moderator_project:function(event,project_id){
        const vm = this
        this.moderator_tab_views_list = false
        var d = vm.moderator_projects
        vm.moderator_statement = d.filter(function(val) {
        return val.id == project_id;})[0]


      },


      moderator_view:function(event){
        this.moderator_tab_views_list = true
        //get projecs with status = На модерации
        const vm = this
         
        axios.get('/mun_obr/api/get_all_projects').then(function(response){

          vm.moderator_projects = response.data
             
        });


      },

      user_statemen_update:function(event){
        const vm = this
        var statement_id = vm.statement_json.id

        vm.statement_json.status = "На модерации"

        var form_data = new FormData();



        for ( var key in this.statement_json) {

          form_data.append(key, this.statement_json[key]);

        }

        axios.put('/mun_obr/api/statement_update/'+ statement_id, form_data, {
          headers: vm.headers_form
        })
        .then(response => { 
          

          if(response.status >= 200 && response.status <= 226){

         
            vm.get_modal("authModal","Заявка обновлена")
   
          
        } 


        })
        .catch(e => {
          
          this.errors = e.response.data
          console.log(this.errors)
        
        })

      },


      get_messeges:function(event){
        
        
        const vm = this
       
        const tab = event.srcElement.id
  
        if(tab == "moder_chat_tab"){
          var statement_id = vm.moderator_statement.id
        }
        else{
          var statement_id = vm.statement_json.id
        }
        
        console.log(statement_id)
       
        axios.get('/mun_obr/api/get_messeges/'+ statement_id).then(function(response){

          vm.chat_messeges = response.data

             
        });


      },
      create_messege:function(event){
        const vm = this
        var statement_id 
        const el = event.srcElement.id

     
        if(el == "moder_send_msg"){
          statement_id = vm.moderator_statement.id
        }
        else{
          statement_id = vm.statement_json.id
        }
        
        vm.create_messege_json.author = vm.profile_json.author_id
        vm.create_messege_json.statement_id = statement_id



        var form_data = new FormData();

        for ( var key in this.create_messege_json ) {
          form_data.append(key, this.create_messege_json[key]);
        }

        form_data.append("author_id",vm.profile_json.author_id)
        
        axios.post('/mun_obr/api/create_messege', form_data, {
          headers: vm.headers_form
        })
        .then(response => { 

          vm.chat_messeges.unshift(response.data.success)
       

        })
        .catch(e => {
          
          this.errors = e.response.data
        
        })

      },
      // Только для загрузки файлов в диалоге
      upload_dialog_file:function(event){
        const vm = this
        var file = event.target.files[0]
        vm.create_messege_json.user_file = file
      
      },


      // Метод вызова модального окна
      get_modal:function(type,text){
            const vm = this
            vm.modаl_messege = text
            var myModal = new bootstrap.Modal(document.getElementById(type), {
              keyboard: false
            })
            myModal.show()
    
    
          }

      
          },

    


    computed: {

      //Процент заполненности зявки 100/на кол-во полей
            percent() {
              
             
              var z = Object.keys(this.create_st).filter(v => this.create_st[v]).length * 5

              var val = Math.round(z)
              this.perc = val.toString() + "%"
              
              return Math.round(z)



            },
            percent_contract() {
              
             
              var z = Object.keys(this.create_st_contract).filter(v => this.create_st_contract[v]).length * 7.692307692307692

              var val = Math.round(z)
              this.perc_contract = val.toString() + "%"
              
              return Math.round(z)



            },
         



          },
     // Get для получения профилья 
    created: function() {

      const vm = this;
      axios.get('/mun_obr/api/get_profile').then(function(response){

          vm.profile_json = response.data[0]
 
          
        });

      // Получение проектов
      // axios.get('/mun_obr/api/get_projects').then(function(response){

      //   vm.projects_json = response.data
        
      // });
      vm.get_projects()

     
      axios.get('/mun_obr/api/get_statements').then(function(response){

          vm.statements = response.data
        });

     
     
          
    },
        
    
})




