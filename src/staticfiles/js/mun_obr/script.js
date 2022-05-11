
new Vue({
    el:'#vue_app',
 
    data: {

      // Для выборки 
      statements:"",
        //Словарь для создания письма
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
          short_name_grantee:"",
          d_f_name:"",
          d_s_name:"",
          d_m_name:"",
          d_position:"",
          d_phone:"",
          d_mail:"",
          d_amount_of_overdue_debt:"",
          


        },

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
          c_pdf_file_name:"",
          c_statement:2




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

        // Для появления/скрытия кнопки отправки
        styleObject: {
          display: 'none',
        },

        // Параметр для отображения списка или одного проекта
        projects_tab_views:"list",

        // Переменная профиль
        profile_json:"",
        // Переменная проект
        projects_json:"",

        projects_list:"",

        contract_json:"",
          
        errors:"",
        
        
        // Проценты заполненности
        perc:"",
        perc_contract:""

    },
 


    methods: {

      
      uploadFile(e) {
            //get id
            var z = e.srcElement.id
            //get file
            var file = e.target.files[0]
    
            console.log(file)
            console.log(z)
            //Валидация по размеру файла 2621440
            if (file.size > 10*1024*1024) {
              e.preventDefault();
              
              this.create_st_contract[z] = null
              
              // Показать modal
          
              document.getElementById(z).value= null;
             
            }
            
            else{
              //Прикрепить файл
              this.create_st_contract[z] = file
    
            } 

            
      },

      //Атвозаполнение из профиля
      get_inn: function(){
        document.getElementById("input8").value = this.profile_json.ogrn
        document.getElementById("input10").value = this.profile_json.inn
        console.log(this.profile_json)
      },
  
      projects(){

        this.projects_tab_views = "list"
      },


      open_project:function(event, project_id){
        const vm = this
        // var d = this.projects_json
        this.projects_tab_views= "one"
        
        axios.get('/mun_obr/api/get_contracts/'+ project_id).then(function(response){

          vm.contract_json = response.data
          console.log(vm.contract_json)          
        });
  



        // this.projects_list = d.filter(function(val) {
        // return val.ID == project_id;})[0]

      },


      // Меню
      test11: function(event,project_id){
        var n = event.srcElement.innerText
       
        // Меню создать писмо
        if(n=="Создать письмо"){

     
            this.selected_dict = this.create_post
            this.styleObject = ""
            this.post_button_status = "create_st"
            this.errors = ""
        


        }
        else if(n=="Мой профиль"){

          this.selected_dict = this.profile_json
          this.styleObject = {display: 'none'}
          this.post_button_status = "get_profiles"
          this.errors = ""
        }


        else if (n=="Мои проекты"){

        this.selected_dict = this.projects_json
        
        this.styleObject = {display: 'none'}
        this.post_button_status = "projects_list"
        this.errors = ""
        }
        else{

          var d = this.projects_json
          this.post_button_status = "open_project"
        
         
          this.selected_dict = d.filter(function(val) {
          return val.ID == project_id;})[0]
          this.errors = ""
         
          

        }
      },



    

      onSubmit (event) {
        

      //  this.post_request = {

      //   title:document.getElementById('input0').value,
      //   requested_sum:document.getElementById('input1').value,
      //   sum_expenses:document.getElementById('input2').value,
      //   source:document.getElementById('input3').value,
      //   link:document.getElementById('input4').value,
      //   recipient_type:document.getElementById('input5').value,
      //   ogrn:document.getElementById('input6').value,
      //   egryl_info:document.getElementById('input7').value,
      //   inn:document.getElementById('input8').value,
      //   kpp:document.getElementById('input9').value,
      //   full_name_grantee :document.getElementById('input10').value,
      //   short_name_grantee:document.getElementById('input11').value,
      //   author: this.profile_json.id
      //   // director:document.getElementById('input12').value,
      //   // director_position:document.getElementById('input13').value
       

      //  }

        //Simple POST request with a JSON body using fetch
        // const requestOptions = {
        //   method: "POST",
        //   headers: { "Content-Type": "application/json",
        //           "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
        // },
        //   body: JSON.stringify(this.post_request)
        // };
        // fetch('/mun_obr/api/create_statement', requestOptions)
        //   .then(response => response.json())
        //   .then(data => (this.postId = data.id));
       

        var form_data = new FormData();

        for ( var key in this.create_st_contract ) {
            form_data.append(key, this.create_st_contract[key]);
          }

        

          const headers = {
            "Content-Type": "multipart/form-data",
            "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
            }
          
        
          
          // axios.post('/mun_obr/api/create_statement', form_data, {
          //     headers: headers
          //   })
          //   .then(response => { 
          //     console.log(response);
          //   })
          //   .catch(e => {
              
          //     this.errors = e.response.data
            
          //   })
            
      // function extend(obj, src) {
      //     for (var key in src) {
      //         if (src.hasOwnProperty(key)) obj[key] = src[key];
      //     }
      //     return obj;
      // }
        
      // var u = extend(this.create_st, this.create_st_contract)
      //console.log(u)
        
          axios.post('/mun_obr/api/create_contract', form_data, {
              headers: headers
            })
            .then(response => { 
              console.log(response);
            })
            .catch(e => {
              
              this.errors = e.response.data
            
            })


      }

          },


    computed: {

      //Процент заполненности зявки 100/на кол-во полей
            percent() {
              
             
              var z = Object.keys(this.create_st).filter(v => this.create_st[v]).length * 7.692307692307692

              var val = Math.round(z)
              this.perc = val.toString() + "%"
              
              return Math.round(z)



            },
            percent_contract() {
              
             
              var z = Object.keys(this.create_st_contract).filter(v => this.create_st_contract[v]).length * 7.692307692307692

              var val = Math.round(z)
              this.perc_contract = val.toString() + "%"
              
              return Math.round(z)



            }




          },
     // Get для получения профилья 
    created: function() {

      const vm = this;
      axios.get('/mun_obr/api/get_profile').then(function(response){

          vm.profile_json = response.data[0]
          
        });

      // Получение проектов
      axios.get('/mun_obr/api/get_projects').then(function(response){

        vm.projects_json = response.data
        
      });

     
      axios.get('/mun_obr/api/get_statements').then(function(response){

          vm.statements = response.data
        });

     
     
          
    },
        
    
})




