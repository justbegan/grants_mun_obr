new Vue({
    el:'#vue_app',
 
    data: { 
        base_url: "",
        news_json:[],
    

    },

    created:function(){

  

            const vm = this;
            axios.get('/mun_obr/api/get_news').then(function(response){
      
                vm.news_json = response.data
       
                
              });

            
            vm.base_url =  window.location.origin

    }

})