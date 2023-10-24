<template>
  <div class="container my-4 col-4">
    <h2>Update</h2>
    <br>
      <form @submit.prevent="updateCity">
        <div class="mb-3">
          <label for="cityname" class="form-label"><strong>City Name</strong></label>
          <input type="text" class="form-control" name="cityname" id="cityname" v-model="CityName" readonly>
        </div>
        <div class="mb-3">
          <label for="statename" class="form-label"><strong>State Name</strong></label>
          <input type="text" class="form-control" name="statename" id="statename" aria-describedby="emailHelp" v-model="StateName">
        </div>
        <button type="submit" class="btn btn-dark">Submit</button>
      </form>
  </div>
</template>

<script>
export default {
    name:'updatecity',

    props:{
        CityName:{
            type: [String],
            required:true,
        }
    },

    data(){
        return {
            CityName:null,
            StateName:null,
            error:null,
        }
    },

    methods:{
        updateCity(){
            if(!this.CityName || !this.StateName){
                this.error = "Please fill all the fields"
            }else{
                fetch(`http://127.0.0.1:5000/city/update/${this.CityName}`,{
                method:"PUT",
                headers:{
                    "Content-Type":"application/json",
                    "Authorization": "Bearer " + localStorage.getItem('user'),
                    "UserAuth" : localStorage.getItem('auth')
                },
                body: JSON.stringify({CityName:this.CityName,StateName: this.StateName})
                })
                .then(resp => resp.json())
                .then(() =>{
                    this.$router.push({
                        name:'cities'
                    })
                })
                .catch(error => {
                    console.log(error)
                })
            }
        },

    },

    beforeRouteEnter(to, from, next){
         if(to.params.CityName !== undefined){
          fetch(`http://127.0.0.1:5000/city/${to.params.CityName}`,{
          method:"GET",
          headers:{"Content-Type":"application/json",
                  "Authorization": "Bearer " + localStorage.getItem('user'),
                  "UserAuth" : localStorage.getItem('auth')
          
          },
        })
        .then(resp => resp.json())
        .then(data =>{
          return next(vm=>(vm.CityName=data.CityName, vm.StateName=data.StateName))
        })
        .catch(error =>{
          console.log(error)
        })
         }else{
          return next()
         }
    },
}
</script>

<style>

</style>