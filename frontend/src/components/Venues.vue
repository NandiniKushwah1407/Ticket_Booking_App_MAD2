<template>
<div class="container">
  <div v-if="error" class="alert alert-success alert-dismissible fade show" role="alert">
        <strong>{{error}}</strong>
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
      </div>
  <div class="row">
    <div class="col-3 my-4">
      <h2>Add a Venue</h2>
      <form @submit="addVenue">
        <div class="mb-3">
          <label for="cityname" class="form-label">City</label>
          <input type="text" class="form-control" name="cityname" id="cityname" aria-describedby="emailHelp"
          :value="$route.params.CityName" aria-label="readonly input example" readonly>
        </div>
        <div class="mb-3">
          <label for="venueid" class="form-label">Venue ID</label>
          <input type="text" class="form-control" name="venueid" id="venueid" aria-describedby="emailHelp" v-model="VenueID">
        </div>
        <div class="mb-3">
          <label for="venuename" class="form-label">Venue Name</label>
          <input type="text" class="form-control" name="venuename" id="venuename" aria-describedby="emailHelp" v-model="VenueName">
        </div>
        <div class="mb-3">
          <label for="venueplace" class="form-label">Address</label>
          <input type="text" class="form-control" name="venueplace" id="venueplace" v-model="VenuePlace">
        </div>
        <div class="mb-3">
          <label for="venuecapacity" class="form-label">Capacity</label>
          <input type="text" class="form-control" name="venuecapacity" id="venuecapacity" v-model="VenueCapacity">
        </div>
        <button type="submit" class="btn btn-dark">Submit</button>
      </form>
      <div v-if="error" class="alert alert-warning alert-dismissible fade show mt-5" role="alert">
   <strong>{{ error }}</strong>
    </div>
    </div>
    <div class="col-9 my-4">
      <table class="table table-striped">
  <thead>
    <tr>
      <th scope="col">SNo</th>
      <th scope="col">VenueID</th>
      <th scope="col">Name</th>
      <th scope="col">Place</th>
      <th scope="col">Capacity</th>
      <th scope="col"></th>
    </tr>
  </thead>
  <tbody>
     <tr v-for = "(venue,index) in venues" :key="venue.VeneuID">
      <th>{{ index+1 }}</th>
      <td>{{venue.VenueID}}</td>
      <td>{{venue.VenueName}}</td>
      <td>{{venue.VenuePlace}}</td>
      <td>{{venue.VenueCapacity}} seats</td>
      <td><router-link class="btn btn-success btn-sm" :to="{name:'updatevenue', params:{VenueID:venue.VenueID,CityName:venue.CityName}}">
        <img src="../assets/edit2.png" alt="Add" width="18" height="18"></router-link>&nbsp;
        <button class="btn btn-danger btn-sm" @click="deleteVenue(venue.VenueID)">
        <img src="../assets/recycle-bin.png" alt="Add" width="18" height="18"> </button>&nbsp;
    <router-link class="btn btn-warning btn-sm" :to="{name:'show', params:{VenueID:venue.VenueID}}">
        <img src="../assets/add.png" alt="Add" width="18" height="18"> Shows
     </router-link>&nbsp;
     <button class="btn btn-info btn-sm"  @click="exportVenue(venue.VenueID)">
        <img src="../assets/download.png" alt="Add" width="18" height="18"> </button>&nbsp;
    </td>
     
    </tr>
  </tbody>
</table>
</div>
</div>
</div>
  </template>
  
<script>
import { useRoute } from 'vue-router';
const route = useRoute();

  export default {
    name: 'Venues',
      
      data(){
          return {
            venues:[],
            CityName: this.$route.params.CityName,
            VenueID:null,
            VenueName:null,
            VenuePlace:null,
            VenueCapacity: null
          }
      },
  
      methods:{
        addVenue(){
            if(!this.CityName || !this.VenueID || !this.VenueName || !this.VenuePlace || !this.VenueCapacity){
                this.error = "Please fill all the fields"
            }else{
                fetch('http://127.0.0.1:5000/venue/add/'+this.VenueID,{
                method:"POST",
                headers:{
                    "Content-Type":"application/json",
                    "Authorization": "Bearer " + localStorage.getItem('user'),
                    "UserAuth" : localStorage.getItem('auth')
                },
                body: JSON.stringify({CityName:this.CityName, VenueID:this.VenueID, VenueName: this.VenueName, VenuePlace: this.VenuePlace, VenueCapacity: this.VenueCapacity})
                })
                .then(resp => resp.json())
                .then(() =>{
                    this.$router.push({
                        name:'Venues'
                    })
                })
                .catch(error => {
                    console.log(error)
                })
            }
        },
        deleteVenue(VenueID){
        fetch(`http://127.0.0.1:5000/venue/delete/${VenueID}`,{
            method:"DELETE",
            headers:{
                "Content-Type":"application/json",
                "Authorization": "Bearer " + localStorage.getItem('user'),
                "UserAuth" : localStorage.getItem('auth')
            },
        })
          .then(() =>{

                    this.$router.push(`/venue/${VenueID}`)
                    window.location.reload();
                })
            .catch(error => {
                console.log(error);
            });
      },
          getVenue(){
              const CityName =this.$route.params.CityName;
              fetch('http://127.0.0.1:5000/venues/'+CityName,{
              method:"GET",
              headers:{
                  "Content-Type":"application/json",
                  "Authorization": "Bearer " + localStorage.getItem('user'),
                  "UserAuth" : localStorage.getItem('auth')
              }
              })
              .then(resp => resp.json())
              .then(data =>{
                  this.venues.push(...data)
                  console.log(data)
              })
              .catch(error => {
                  console.log(error)
              })
          },
          exportVenue(VenueID){
              fetch(`http://127.0.0.1:5000/export/${VenueID}`,{
              method:"GET",
              headers:{
                  "Content-Type":"application/json",
                  "Authorization": "Bearer " + localStorage.getItem('user'),
                  "UserAuth" : localStorage.getItem('auth')
              }
              })
              .then(resp => resp.json())
              .then(data =>{
                  console.log(data)
              })
              .catch(error => {
                  console.log(error)
              })
          }
        },
      created(){
          this.getVenue()
      },
    }
  </script>
  
  <style>
  
  </style>