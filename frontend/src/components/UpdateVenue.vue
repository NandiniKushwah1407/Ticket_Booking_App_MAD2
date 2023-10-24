<template>
    <div class="container my-4 col-4">
      <h2>Update</h2>
      <br>
      <form @submit.prevent="updateVenue">
        <div class="mb-3">
          <label for="venueid" class="form-label">Venue ID</label>
          <input type="text" class="form-control" name="venueid" id="venueid" aria-describedby="emailHelp" v-model="VenueID" readonly>
        </div>
        <div class="mb-3">
          <label for="venuename" class="form-label">Venue Name</label>
          <input type="text" class="form-control" name="venuename" id="venuename" aria-describedby="emailHelp" v-model="VenueName">
        </div>
        <div class="mb-3">
          <label for="venueplace" class="form-label">Address</label>
          <input type="text" class="form-control" name="venueplace" id="venueplace" v-model="VenuePlace">
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
      name:'updatecity',
  
      props:{
          VenueID:{
              type: [String],
              required:true,
          }
      },
  
      data(){
          return {
              VenueID:null,
              VenueName:null,
              VenuePlace:null,
              error:null
          }
      },
  
      methods:{
          updateVenue(){
            if(!this.VenueID || !this.VenueName || !this.VenuePlace){
                this.error = "Please fill all the fields"
            }else{
                fetch(`http://127.0.0.1:5000/venue/update/${this.VenueID}`,{
                method:"PUT",
                headers:{
                    "Content-Type":"application/json",
                    "Authorization": "Bearer " + localStorage.getItem('user'),
                    "UserAuth" : localStorage.getItem('auth')
                },
                body: JSON.stringify({ VenueID:this.VenueID, VenueName: this.VenueName, VenuePlace: this.VenuePlace})
                })
                .then(resp => resp.json())
                .then(() =>{
                    const CityName = this.$route.params.CityName
                    this.$router.push('/venue/'+CityName)
                })
                .catch(error => {
                    console.log(error)
                })
            }
        },
  
      },
  
      beforeRouteEnter(to, from, next){
           if(to.params.VenueID !== undefined){
            fetch(`http://127.0.0.1:5000/venue/${to.params.VenueID}`,{
            method:"GET",
            headers:{"Content-Type":"application/json",
                     "Authorization": "Bearer " + localStorage.getItem('user'),
                     "UserAuth" : localStorage.getItem('auth')
            },
          })
          .then(resp => resp.json())
          .then(data =>{
            return next(vm=>(vm.VenueID=data.VenueID, vm.VenueName=data.VenueName, vm.VenuePlace=data.VenuePlace))
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