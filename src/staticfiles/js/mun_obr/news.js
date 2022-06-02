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
    
    
          }
        

    },

    created:function(){

  

            const vm = this;
            axios.get('/mun_obr/api/get_news').then(function(response){
      
                vm.news_json = response.data
       
                
              });

            
            vm.base_url =  window.location.origin

    }

})