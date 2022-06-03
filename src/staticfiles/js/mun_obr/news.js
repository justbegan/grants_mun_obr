new Vue({
    el:'#vue_app',
 
    data: { 
        base_url: "",
        news_json:[],
        selected_news:"",
    

    },

    methods: {

        open_news:function(e,news_id){
        const  vm = this
        var d = vm.news_json
        vm.selected_news = d.filter(function(val) {
        return val.id == news_id;})[0]
        console.log(vm.selected_news)
        vm.get_modal("main_Modal")

        },
        get_modal:function(type){
            const vm = this
         
            var myModal = new bootstrap.Modal(document.getElementById(type), {
              keyboard: false
            })
            myModal.show()
    
    
          },

        padTo2Digits:function(num) {
            return String(num).padStart(2, '0');
          }
        

    },

    created:function(){

  

            const vm = this;
            axios.get('/mun_obr/api/get_news').then(function(response){
      
                vm.news_json = response.data
       
                
              });

            
            vm.base_url =  window.location.origin

    },
    computed:{

      create_time:function(){

        const vm = this
        var date = vm.selected_news.create_time
       
   
        var d = new Date(date),
  
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();
        const hoursAndMinutes =
        vm.padTo2Digits(d.getHours()) + ':' + vm.padTo2Digits(d.getMinutes());

    if (month.length < 2) 
        month = '0' + month;
    if (day.length < 2) 
        day = '0' + day;

      resp = [year, month, day].join('-');
      return resp + " " + hoursAndMinutes

      }

    }

})