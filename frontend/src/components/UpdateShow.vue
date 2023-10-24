<template>
    <div class="container my-4 col-4">
      <h2>Update Show</h2>
      <br>
      <form @submit.prevent="updateShow">
        <div class="mb-3">
          <label for="showid" class="form-label">Show ID</label>
          <input type="text" class="form-control" name="showid" id="showid" v-model="ShowID" readonly>
        </div>
        <div class="mb-3">
          <label for="showname" class="form-label">Show Name</label>
          <input type="text" class="form-control" name="showname" id="showname" v-model="ShowName">
        </div>
        <div class="mb-3">
          <label for="showtag" class="form-label">Show Tag</label>
          <input type="text" class="form-control" name="showtag" id="showtag" v-model="ShowTag">
        </div>
        <div class="mb-3">
          <label for="showlanguage" class="form-label">Show Language</label>
          <input type="text" class="form-control" name="showlanguage" id="showlanguage" v-model="ShowLanguage">
        </div>
        <div class="mb-3">
          <label for="showtime" class="form-label">Show Time</label>
          <input type="text" class="form-control" name="showtime" id="showtime" v-model="ShowTime">
        </div>
        <div class="mb-3">
          <label for="showprice" class="form-label"> Show Price</label>
          <input type="text" class="form-control" name="showprice" id="showprice" v-model="ShowPrice">
        </div>
        <button type="submit" class="btn btn-dark">Submit</button>
      </form>
      <div v-if="error" class="alert alert-warning alert-dismissible fade show mt-5" role="alert">
   <strong>{{ error }}</strong>
    </div>
</div>
  </template>
  
  <script>
  import { useRoute } from 'vue-router';
const route = useRoute();
  export default {
      name:'updateshow',
  
      props:{
          ShowID:{
              type: [String],
              required:true,
          }
      },
  
      data(){
          return {
            ShowID:null,
            ShowName:null,
            ShowTag: null,
            ShowLanguage: null,
            ShowTime: null,
            ShowPrice: null,
          }
      },
  
      methods:{
        updateShow(){
            if(!this.ShowID || !this.ShowName || !this.ShowTag || !this.ShowLanguage || !this.ShowTime || !this.ShowPrice){
                this.error = "Please fill all the fields"
            }else{
                fetch(`http://127.0.0.1:5000/show/update/${this.ShowID}`,{
                method:"PUT",
                headers:{
                    "Content-Type":"application/json",
                    "Authorization": "Bearer " + localStorage.getItem('user'),
                    "UserAuth" : localStorage.getItem('auth')
                },
                body: JSON.stringify({ShowID: this.ShowID,
                                      ShowName: this.ShowName,
                                      ShowTag: this.ShowTag,
                                      ShowLanguage: this.ShowLanguage,
                                      ShowTime: this.ShowTime,
                                      ShowPrice: this.ShowPrice})
                })
                .then(resp => resp.json())
                .then(() =>{
                    const VenueID=this.$route.params.VenueID
                    this.$router.push('/show/'+VenueID)
                })
                .catch(error => {
                    console.log(error)
                })
            }
        },
    },
  
      beforeRouteEnter(to, from, next){
           if(to.params.ShowID !== undefined){
            fetch(`http://127.0.0.1:5000/show/${to.params.ShowID}`,{
            method:"GET",
            headers:{"Content-Type":"application/json",
                     "Authorization": "Bearer " + localStorage.getItem('user'),
                     "UserAuth" : localStorage.getItem('auth')
            },
          })
          .then(resp => resp.json())
          .then(data =>{
            return next(vm=>(vm.ShowID=data.ShowID,
                            vm.ShowName=data.ShowName,
                            vm.ShowTag=data.ShowTag,
                            vm.ShowLanguage=data.ShowLanguage,
                            vm.ShowTime=data.ShowTime,
                            vm.ShowPrice=data.ShowPrice))
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