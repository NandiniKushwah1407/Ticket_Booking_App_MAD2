<template>
  <div>
    <div class="container">
  <div v-if="msg.length != 0 && showAlert" class="alert alert-warning alert-dismissible fade show mt-5" role="alert">
   <strong>{{ msg[0] }}</strong>
   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close" @click="closeAlert"></button>
    </div>
</div>
    <div class="container my-4" style="text-align: center; font-size: large;">
  <img src="../assets/congrats.png" alt="congrats" style="width: 200px;">
  <h1 style="color: #ffc107;">{{ User }} !!</h1>
  <h3 style="font-weight: bolder;">Your Tickets are Booked</h3>
</div>
<div class="col" style="margin: 20px; text-align: center; padding-left: 300px; padding-right: 300px;">
  <div class="card">
    <div class="card-body" style="border: 3px solid #000; border-radius: 10px; ">
      <h3 class="card-title" style="font-weight: bold;">Your Ticket</h3>
      <div class="card-text" v-for="s in show" :key="s">
      <h6 class="my-2">Show: {{ s.ShowName }} </h6>
      <h6 class="my-2">Name: {{ User }} </h6>
      <h6 class="my-2" v-for="v in venue" :key="v">Venue: {{ v.VenueName }},{{ v.VenuePlace }},{{ v.CityName }}</h6>
      <h6 class="my-2">Language: {{ s.ShowLanguage }} </h6>
      <h6 class="my-2">Show Time:  {{ s.ShowTime }}</h6>
      <h6 class="my-2">Total: ₹ {{ tickets.length*s.ShowPrice }}</h6>
      </div>

      <h3>Rate Now</h3>
      <div>
        <form @submit.prevent="rate">
          <div style="display: flex; text-align: center;">
            <div class="star">
              <input type="radio" id="five" name="rate" value="5" v-model="rating">
              <label for="five"></label>
              <input type="radio" id="four" name="rate" value="4" v-model="rating">
              <label for="four"></label>
              <input type="radio" id="three" name="rate" value="3" v-model="rating">
              <label for="three"></label>
              <input type="radio" id="two" name="rate" value="2" v-model="rating">
              <label for="two"></label>
              <input type="radio" id="one" name="rate" value="1" v-model="rating">
              <label for="one"></label>
            </div>
          </div>
          <div>
            <button type="submit" class="btn btn-danger">Rate</button>
          </div>
        </form>
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
    name: 'booked',

    data(){
          return {
           show:[],
           venue:[],
           tickets: this.$route.params.tickets.split(','),
           User: localStorage.getItem('username'),
           rating:[],
           msg: [],
           showAlert: true,
          }
      },
    methods:{
      closeAlert() {
              this.showAlert = false;
              window.location.reload();
              },
        getshow(){
            const ShowID=this.$route.params.ShowID
            fetch('http://127.0.0.1:5000/show/'+ShowID,{
            method:"GET",
            headers:{
                "Content-Type":"application/json",
                "Authorization": "Bearer " + localStorage.getItem('user'),
                "UserAuth" : localStorage.getItem('auth')
            },
            })
            .then(resp => resp.json())
            .then(data =>{
                this.show.push(data)
                const VenueID = data.VenueID 
                fetch('http://127.0.0.1:5000/venue/'+VenueID,{
                method:"GET",
                headers:{
                "Content-Type":"application/json",
                "Authorization": "Bearer " + localStorage.getItem('user'),
                "UserAuth" : localStorage.getItem('auth')
            },
            })
            .then(resp => resp.json())
            .then(data =>{
                this.venue.push(data)
            })
            .catch(error => {
                console.log(error)
            });
            })
            .catch(error => {
                console.log(error)
            });
           
        },
        rate(){
                if (!localStorage.getItem('user')){
                  this.msg.push('Please Login to Proceed')
                }
                else{
                fetch('http://127.0.0.1:5000/rating/'+this.rating,{
                method:"PUT",
                headers:{
                    "Content-Type":"application/json",
                    "Authorization": "Bearer " + localStorage.getItem('user'),
                    "UserAuth" : localStorage.getItem('auth')
                },
                body: JSON.stringify({List: this.tickets.toString(), ShowID: this.$route.params.ShowID})
                })
                .then(resp => resp.json())
                .then(data => {
                  this.msg.push('Rated Successfuly')
                });
              }
              },
    },
    created(){
        this.getshow()

}}
</script>

<style>
.star{
    width: 520px;
    text-align: center;
  }
  .star input{
    display: none;
  }
  .star label{
    float: right;
    font-size: 50px;
    color: lightgray;
    margin: 0 5px;
    text-shadow: 1px 1px #bbb;
  }
  .star label:before{
    content: "★";
  }
  .star input:checked ~ label{
    color: gold;
    text-shadow: 1px 1px #c60;
  }
  .star:not(:checked)> label:hover, .star:not(:checked)> label:hover ~ label{
    color: gold;
  }
  .star input:checked > label:hover, .star input:checked > label:hover ~ label {
    color: gold;
    text-shadow: 1px 1px goldenrod ;
  }
</style>