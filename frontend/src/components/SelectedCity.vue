<template>
    <div>
        <br>
    <div class="container my-2" style="text-align: center;">
      <h1>Welcome! Book Your Tickets with Films <img src="../assets/movies.png" alt="BookMyTicket" width="80"
          height="80"> ForYou</h1>
    </div>
    
    <div style="text-align: center;">
      <h5 class="my-4">Venues in {{CityName}}</h5>
      <div v-for="venue in venues" :key="venue" style="display: inline; padding: 0.5%;"> 
        <router-link class="btn btn-danger btn-sm" :to="{name:'venueshow', params:{VenueID:venue.VenueID}}">
            <strong>{{ venue.VenueName }}</strong>
         </router-link> </div>
    </div>
    
    <div class="container my-4" style="text-align: center; display: flex;">
      <div class="col" style="margin: 20px;" v-for="show in shows.slice(0,4)" :key="show">
        <div class="card">
          <div class="card-body">
            <h3 class="card-title" style="font-weight: bold;">{{show.ShowName}}</h3>
            <div class="card-text">
            <h6 class="my-2">Ticket Price: ₹ {{show.ShowPrice}}</h6>
            <h6 class="my-2">Language: {{show.ShowLanguage}}</h6>
            <h6 class="my-2">Time: {{show.ShowTime}}</h6>
            <h6>Rating: {{show.ShowRating}} <img src="../assets/star.png" alt="star"
              style="height: 20px; width: 20px;"></h6>
            </div>
            <br>
            <router-link class="btn btn-warning btn-sm" :to="{name:'seating', params:{ShowID:show.ShowID, VenueID:show.VenueID}}">Book Tickets</router-link>
          </div>
        </div>
      </div>
    </div>
    </div>
    </template>
    
    <script>
    export default {
      name: 'Index',
          
          data(){
              return {
                venues:[],
                shows:[],
                CityName: this.$route.params.CityName
              }
          },
      methods:{
        getVenue(){
                  const CityName =this.$route.params.CityName;
                  fetch('http://127.0.0.1:5000/'+CityName,{
                  method:"POST",
                  headers:{
                      "Content-Type":"application/json",
                      "Authorization": "Bearer " + localStorage.getItem('user'),
                      "UserAuth" : localStorage.getItem('auth')
                  }
                  })
                  .then(resp => resp.json())
                  .then(data =>{
                      this.venues.push(...data[0])
                      this.shows.push(...data[1])
                  })
                  .catch(error => {
                      console.log(error)
                  })
              },
          },
          created(){
              this.getVenue()
      }
     }
    </script>
    
    <style>
    
    </style>