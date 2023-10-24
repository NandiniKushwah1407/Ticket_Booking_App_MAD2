<template>
<div class="container">
  <div v-if="cities.length === 0 ">
    Login Please
  </div>
  <div v-else>
  <div class="row">
    <div class="my-4 col-3">
      <h2>Add a City</h2>
      <br>
      <form @submit.prevent="addCity">
        <div class="mb-3">
          <label for="statename" class="form-label"><strong>State Name</strong></label>
          <input type="text" class="form-control" name="statename" id="statename" aria-describedby="emailHelp" v-model="StateName">
        </div>
        <div class="mb-3">
          <label for="cityname" class="form-label"><strong>City Name</strong></label>
          <input type="text" class="form-control" name="cityname" id="cityname" v-model="CityName">
        </div>
        <button type="submit" class="btn btn-dark">Submit</button>
      </form>
    </div>
    <div class="my-4 col-9">
      <table class="table table-striped">
  <thead>
    <tr>
      <th scope="col">SNo</th>
      <th scope="col">City</th>
      <th scope="col">State</th>
      <th scope="col"></th>
    </tr>
  </thead>
  <tbody>
    <tr v-for = "(city,index) in cities" :key="city.CityName">
      <th>{{ index+1 }}</th>
      <td>{{city.CityName}}</td>
      <td>{{city.StateName}}</td>
      <td><router-link class="btn btn-success btn-sm" :to="{name:'updatecity', params:{CityName:city.CityName}}">
        <img src="../assets/edit2.png" alt="Add" width="18" height="18"></router-link>&nbsp;
     <button class="btn btn-danger btn-sm" v-on:click="deleteCity(city.CityName)">
        <img src="../assets/recycle-bin.png" alt="Add" width="18" height="18"> </button>&nbsp;
    <router-link class="btn btn-warning btn-sm" :to="{name:'venue', params:{CityName:city.CityName}}">
        <img src="../assets/add.png" alt="Add" width="18" height="18">  Venue
     </router-link></td>
    </tr>
  </tbody>
</table>
    </div>
  </div>
</div>
</div>
</template>

<script>


export default {
  name: 'Cities',

    
    data(){
        return {
            cities:[],
            CityName:null,
            StateName:null,
            error:null,
            token : localStorage.getItem('user'),
            User : localStorage.getItem('auth'),
        }
    },

    methods:{
      closeAlert() {
              this.showAlert = false;
              window.location.reload();
              },
      addCity(){
            if(!this.CityName || !this.StateName){
                this.error = "Please fill all the fields"
            }else{
                fetch('http://127.0.0.1:5000/city/add/'+this.CityName,{
                method:"POST",
                headers:{
                    "Content-Type":"application/json",
                    "Authorization": "Bearer " + localStorage.getItem('user'),
                    "UserAuth" : localStorage.getItem('auth')
                },
                body: JSON.stringify({CityName:this.CityName,StateName: this.StateName})
                })
                .then(resp => resp.json())
                .then(() =>{
                    this.$router.push('/cities')
                    window.location.reload();
                
                })
                .catch(error => {
                    console.log(error)
                })
            }
        },
      deleteCity(CityName){
        fetch(`http://127.0.0.1:5000/city/delete/${CityName}`,{
            method:"DELETE",
            headers:{
                "Content-Type":"application/json",
                "Authorization": "Bearer " + localStorage.getItem('user'),
                "UserAuth" : localStorage.getItem('auth')
            },
        })
        this.$router.push('/cities').then(() => {
                  window.location.reload();
  })
            .catch(error => {
                console.log(error);
            });
      },
      
        getCity(){
            fetch('http://127.0.0.1:5000/city',{
            method:"GET",
            
            headers:{
                "Content-Type":"application/json",
                "Authorization": "Bearer " + localStorage.getItem('user'),
                "UserAuth" : localStorage.getItem('auth')
            },
            })
            .then(resp => resp.json())
            .then(data =>{
                this.cities.push(...data)
            })
            .catch(error => {
                console.log(error)
            });
        }
    },
    created(){
        this.getCity()
    }

}
</script>

<style>

</style>


