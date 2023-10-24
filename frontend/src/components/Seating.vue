<template>
<div class="container my-2">
  <div v-if="msg.length != 0 && showAlert" class="alert alert-warning alert-dismissible fade show mt-5" role="alert">
   <strong>Please Login to Proceed</strong>
   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close" @click="closeAlert"></button>
    </div>
    <div class="row">
        <div class="col-md-4 my-4" style="text-align: center;">
          <!-- Movie details card -->
          <br><br><br><br><br><br><br>
          <div class="col" style="margin: 20px;">
            <div class="card"  v-for = "(v) in venue" :key="v.VenueID">
              <div class="card-body" style="border: 2px solid gray; border-radius: 10px;">
                <h3 class="card-title" style="font-weight: bold;"  v-for = "(s) in show" :key="s.ShowID">{{ s.ShowName }}</h3> <br>
                <div class="card-text" v-for = "(s) in show" :key="s.ShowID">
                  <h6 class="my-2">Venue: {{ v.VenueName }}, {{ v.VenuePlace }}, {{ v.CityName }}</h6>
                  <h6 class="my-2">Ticket Price: ₹ {{ s.ShowPrice }}</h6>
                  <h6 class="my-2">Language: {{ s.ShowLanguage }}</h6>
                  <h6 class="my-2">Time: {{ s.ShowTime }}</h6>
                  <h6>Rating: {{ s.ShowRating }} <img src="../assets/star.png" alt="star" style="height: 20px; width: 20px;"></h6>
                </div>
              </div>
            </div>
          </div>
        </div>
    <div class="col-md-1 my-4"></div>
    <div class="col-md-4 my-4">
      <ul class="showcase my-4" style="display: flex;">
        <div style="margin-right: 70px;">
          <button type="button" class="btn" disabled
            style="width: 50px; height: 25px; border-top-left-radius: 10px; border-top-right-radius: 10px; border: 2px solid darkorange"></button>
        </div>
        <div style="margin-right: 70px;">
          <input class="form-check-input" type="checkbox" id="inlineCheckbox1" value="1"
            style="width: 50px; height: 25px; border-top-left-radius: 10px; border-top-right-radius: 10px; border: 2px solid darkorange"
            checked disabled>
        </div>
        <div>
          <button type="button" class="btn btn-danger" disabled
            style="width: 50px; height: 25px; border-top-left-radius: 10px; border-top-right-radius: 10px; border: 2px solid darkorange"></button>
        </div>
      </ul>
      <ul style="display: flex;">
        <div style="margin-right: 60px; font-weight: bold;"><small>Available</small></div>
        <div style="margin-right: 65px; font-weight: bold;"><small>Selected</small></div>
        <div style="margin-right: 70px; font-weight: bold;"><small>Booked</small></div>
      </ul>


      <div class="container">
        <div class="screen my-4"
          style=" height: 30px; width: 330px; border-top: 50px solid rgb(55, 55, 60); border-left: 20px solid transparent; border-right: 20px solid transparent;">
        </div>
        <form @submit.prevent="bookedseats">
          <table style="width: 330px; text-align: center;">
            <div class="row" v-for="r in row[0]" :key="r">
              <tr v-for="a in tickets" :key="a">
                <td v-for="seat in a.slice(r,r+5)" :key="seat.tno">
                  <div class="form-check form-check-inline" v-if="seat.Booked==0">
                    <input class="form-check-input" type="checkbox" id="inlineCheckbox1" name="seatno"
                      :value='seat.tno' title="click to select" v-model="selected"
                      style="width: 50px; height: 25px; border-top-left-radius: 10px; border-top-right-radius: 10px; border: 2px solid darkorange;">
                      <div>
                        {{ seat.tno }}
                      </div>
                    </div>
                    
                    <div class="form-check form-check-inline" v-else>
                    <input class="form-check-input" type="checkbox" id="inlineCheckbox1" name="seatno" disabled
                      :value='seat.tno'
                      style="width: 50px; height: 25px; border-top-left-radius: 10px; border-top-right-radius: 10px; border: 2px solid darkorange; background-color: red;">
                      <div>{{ seat.tno }}</div>
                  </div>
                </td>
            </tr>
            </div>
          </table>
          <br>
      <button type="submit" class="btn btn-warning">Book</button>
        </form>
</div>
</div>
<div class="col-md-3 my-4" style="text-align: center; font-weight: bold; font-size: 20px; color: #333333;">
  <br><br><h2>Book Now</h2><br><br>
      <img src="../assets/excited.png" alt="image" style="width: 200px;">
      <br><br><br>
     <div>Selected Seats: {{ selected.toString() }}</div>
     <div v-for=" s in show" :key="s.ShowID">Total: {{ selected.length*s.ShowPrice }}</div>
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
               venue:[],
               show:[],
               tickets:[],
               row:[],
               selected:[],
               total:0,
               msg :[],
               showAlert: true,
             }
         },
         methods:{
          closeAlert() {
              this.showAlert = false;
              window.location.reload();
              },
             getvenue(){
                 const VenueID =this.$route.params.VenueID;
                 fetch('http://127.0.0.1:5000/venue/'+VenueID,{
                 method:"GET",
                 headers:{
                     "Content-Type":"application/json", 
                     "Authorization": "Bearer " + localStorage.getItem('user'),
                     "UserAuth" : localStorage.getItem('auth')
                 }
                 })
                 .then(resp => resp.json())
                 .then(data =>{
                    this.venue.push(data)
                 })
                 .catch(error => {
                     console.log(error)
                 })
             },
             getshow(){
                 const ShowID =this.$route.params.ShowID;
                 fetch('http://127.0.0.1:5000/show/'+ShowID,{
                 method:"GET",
                 headers:{
                     "Content-Type":"application/json",
                     "Authorization": "Bearer " + localStorage.getItem('user'),
                     "UserAuth" : localStorage.getItem('auth')
                 }
                 })
                 .then(resp => resp.json())
                 .then(data =>{
                    this.show.push(data)
                    console.log(data)
                 })
                 .catch(error => {
                     console.log(error)
                 })
             },
             gettickets(){
                 const ShowID =this.$route.params.ShowID;
                 fetch('http://127.0.0.1:5000/ticket/'+ShowID,{
                 method:"GET",
                 headers:{
                     "Content-Type":"application/json",
                     "Authorization": "Bearer " + localStorage.getItem('user'),
                     "UserAuth" : localStorage.getItem('auth')
                 }
                 })
                 .then(resp => resp.json())
                 .then(data =>{
                    this.tickets.push(data)
                 })
                 .catch(error => {
                     console.log(error)
                 })
             },
              array() {
                const VenueID = this.$route.params.VenueID;
                fetch('http://127.0.0.1:5000/venue/' + VenueID, {
                  method: "GET",
                  headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + localStorage.getItem('user'),
                    "UserAuth" : localStorage.getItem('auth')
                  }
                })
                .then(resp => resp.json())
                .then(data => {
                  const a = data.VenueCapacity;
                  const arr = [];
                  for (let i = 0; i < a; i += 5) {
                    arr.push(i);
                  }
                  this.row.push(arr)
                });
              },
              bookedseats(){
                const arr2 =[]
                for (let i in this.selected){
                  arr2.push(this.selected[i])
                }
                if (!localStorage.getItem('user')){
                  this.msg.push('Please Login to Proceed')
                }
                else{
                fetch('http://127.0.0.1:5000/booked',{
                method:"PUT",
                headers:{
                    "Content-Type":"application/json",
                    "Authorization": "Bearer " + localStorage.getItem('user'),
                    "UserAuth" : localStorage.getItem('auth')
                },
                body: JSON.stringify({List: arr2.toString(), ShowID: this.$route.params.ShowID})
                })
                .then(resp => resp.json())
                .then(data => {
                  console.log(data)
                });
                const ShowID =this.$route.params.ShowID;
                this.$router.push({name:'booked', params: { ShowID: ShowID, tickets: arr2.toString() }}) 
              }
              },
          },
          created(){
              this.getvenue(),
              this.getshow(),
              this.gettickets(),
              this.array()
          },
     }
     </script>
     
     <style>
     
     </style>

     