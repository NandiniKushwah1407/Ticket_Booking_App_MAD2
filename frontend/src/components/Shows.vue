<template>
 <div class="container">
  <div class="row">
    <div class="col-3 my-4">
      <h2>Add a Show</h2>
      <form @submit="addShow">
        <div class="mb-3">
          <label for="venueid" class="form-label">Venue ID</label>
          <input type="text" class="form-control" name="venueid" id="venueid" :value="$route.params.VenueID" aria-label="readonly input example" readonly>
        </div>
        <div class="mb-3">
          <label for="showid" class="form-label">Show ID</label>
          <input type="text" class="form-control" name="showid" id="showid" v-model="ShowID">
        </div>
        <div class="mb-3">
          <label for="showname" class="form-label">Show Name</label>
          <input type="text" class="form-control" name="showname" id="showname" v-model="ShowName">
        </div>
        <div class="mb-3">
          <label for="showrating" class="form-label">Show Rating</label>
          <input type="text" class="form-control" name="showrating" id="showrating" v-model="ShowRating">
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
    </div>
    <div class="col-9 my-4">
      <table class="table table-striped">
        <thead>
          <tr>
            <th scope="col">SNo</th>
            <th scope="col">Show ID</th>
            <th scope="col">Show Name</th>
            <th scope="col">Rating</th>
            <th scope="col">Tag</th>
            <th scope="col">Language</th>
            <th scope="col">Time</th>
            <th scope="col">Price</th>
            <th scope="col"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for = "(show,index) in shows" :key="show.ShowID">
            <th>{{index+1}}</th>
            <td>{{show.ShowID}}</td>
            <td>{{show.ShowName}}</td>
            <td>{{show.ShowRating}}</td>
            <td>{{show.ShowTag}}</td>
            <td>{{show.ShowLanguage}}</td>
            <td>{{show.ShowTime}}</td>
            <td>₹ {{show.ShowPrice}}</td>
            <td><router-link class="btn btn-success btn-sm"  :to="{name:'updateshow', params:{ShowID:show.ShowID, VenueID:show.VenueID}}">
        <img src="../assets/edit2.png" alt="Add" width="18" height="18"></router-link>&nbsp;
        <button class="btn btn-danger btn-sm" v-on:click="deleteShow(show.ShowID)">
        <img src="../assets/recycle-bin.png" alt="Add" width="18" height="18"> </button>&nbsp;
    <router-link class="btn btn-warning btn-sm" :to="{name:'dashboard', params:{ShowID:show.ShowID, VenueID:show.VenueID}}"><strong>Dashboard</strong></router-link></td>
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
    name:'Shows',

      data(){
          return {
            shows:[],
            VenueID: this.$route.params.VenueID,
            ShowID:null,
            ShowName:null,
            ShowRating:null,
            ShowTag: null,
            ShowLanguage: null,
            ShowTime: null,
            ShowPrice: null,
          }
      },
  
      methods:{
        addShow(){
            if(!this.VenueID || !this.ShowID || !this.ShowName || !this.ShowRating || !this.ShowTag || !this.ShowLanguage || !this.ShowTime || !this.ShowPrice){
                this.error = "Please fill all the fields"
            }else{
                fetch('http://127.0.0.1:5000/show/add/'+this.ShowID,{
                method:"POST",
                headers:{
                    "Content-Type":"application/json",
                    "Authorization": "Bearer " + localStorage.getItem('user'),
                    "UserAuth" : localStorage.getItem('auth')
                },
                body: JSON.stringify({VenueID: this.VenueID,
                                      ShowID: this.ShowID,
                                      ShowName: this.ShowName,
                                      ShowRating: this.ShowRating,
                                      ShowTag: this.ShowTag,
                                      ShowLanguage: this.ShowLanguage,
                                      ShowTime: this.ShowTime,
                                      ShowPrice: this.ShowPrice})
                })
                .then(resp => resp.json())
                .then(() =>{
                    this.$router.push({
                        name:'Shows'
                    })
                })
                .catch(error => {
                    console.log(error)
                })
            }
        },
        deleteShow(ShowID){
        fetch(`http://127.0.0.1:5000/show/delete/${ShowID}`,{
            method:"DELETE",
            headers:{
                "Content-Type":"application/json",
                "Authorization": "Bearer " + localStorage.getItem('user'),
                "UserAuth" : localStorage.getItem('auth')
            },
        })
          .then(() =>{
                    this.$router.push({
                        name:'show'
                    })
                    window.location.reload();
                })
            .catch(error => {
                console.log(error);
            });
      },

          getShow(){
              const VenueID =this.$route.params.VenueID;
              fetch('http://127.0.0.1:5000/shows/'+VenueID,{
              method:"GET",
              headers:{
                  "Content-Type":"application/json",
                  "Authorization": "Bearer " + localStorage.getItem('user'),
                  "UserAuth" : localStorage.getItem('auth')
              }
              })
              .then(resp => resp.json())
              .then(data =>{
                  this.shows.push(...data)
              })
              .catch(error => {
                  console.log(error)
              })
          }
      },
      created(){
          this.getShow()
      }
  
  }
  </script>
  
  <style>
  
  </style>