<template>
<div>
<br>
  <div class="container my-2" style="text-align: center;">
  <h1  v-for="v in venue" :key="v">Welcome to {{v.VenueName}} !!</h1>
</div>

<div class="container my-4" style="text-align: center; display: flex;">
    <div class="col" style="margin: 20px;" v-for="s in shows" :key="s.ShowID">
      <div class="card">
        <div class="card-body">
          <h3 class="card-title">{{s.ShowName}}</h3>
          <div class="card-text">
            <h6 class="my-2">Ticket Price: ₹ {{s.ShowPrice}}</h6>
            <h6 class="my-2">Language: {{s.ShowLanguage}}</h6>
            <h6 class="my-2">Time: {{s.ShowTime}}</h6>
            <h6>Rating: {{s.ShowRating}} <img src="../assets/star.png" alt="star" style="height: 20px; width: 20px;"></h6>
          </div>
          <router-link class="btn btn-warning btn-sm" :to="{name:'seating', params:{ShowID:s.ShowID, VenueID:s.VenueID}}">Book Tickets</router-link>
        </div>
      </div>
    </div>
</div>
</div>
</template>

<script>
import { useRoute } from 'vue-router';
const route = useRoute();
export default {
name: 'venueshows',
data(){
  return{ 
    shows:[],
    venue:[]
  }
},
methods:{
  getShow(){
              const VenueID =this.$route.params.VenueID;
              fetch('http://127.0.0.1:5000/shows/'+VenueID,{
              method:"GET",
              headers:{
                  "Content-Type":"application/json"
              }
              })
              .then(resp => resp.json())
              .then(data =>{
                  this.shows.push(...data)
              })
              .catch(error => {
                  console.log(error)
              })
          },
          getVenue(){
              const VenueID =this.$route.params.VenueID;
              fetch('http://127.0.0.1:5000/venue/'+VenueID,{
              method:"GET",
              headers:{
                  "Content-Type":"application/json"
              }
              })
              .then(resp => resp.json())
              .then(data =>{
                  this.venue.push(data)
              })
              .catch(error => {
                  console.log(error)
              })
          }
      },
      created(){
          this.getShow(),
          this.getVenue()

}
}
</script>

<style>

</style>