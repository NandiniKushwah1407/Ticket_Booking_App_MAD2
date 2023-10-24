<template>
    <div class="container">
      <div v-if="msg.length != 0 && showAlert" class="alert alert-warning alert-dismissible fade show mt-5" role="alert">
       <strong>Please Login to Proceed</strong>
       <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close" @click="closeAlert"></button>
        </div>
        <div style="text-align: center; padding: 2%; color: #333333;">
        <div class="card-body" style="border: 2px solid gray; border-radius: 10px;">
            <h2 style="padding: 1%;" >Dashboard <img src="../assets/dashboard.png" alt="dashboard" style="width: 40px; "></h2> 
        <table class="table table-striped">
        <thead>
          <tr>
            <th scope="col">SNo</th>
            <th scope="col">Show ID</th>
            <th scope="col">Show Name</th>
            <th scope="col">Address</th>
            <th scope="col">Rating</th>
            <th scope="col">Tag</th>
            <th scope="col">Language</th>
            <th scope="col">Time</th>
            <th scope="col">Price</th>
            <th scope="col"></th>
          </tr>
        </thead>
        <tbody v-for = "(v, index) in venue" :key="v.VenueID">
          <tr v-for = "(s) in show" :key="s.ShowID">
            <th>{{index+1}}</th>
            <td>{{s.ShowID}}</td>
            <td>{{s.ShowName}}</td>
            <td>  {{ v.VenueName }}, {{ v.VenuePlace }}, {{ v.CityName }}</td>
            <td>{{s.ShowRating}}</td>
            <td>{{s.ShowTag}}</td>
            <td>{{s.ShowLanguage}}</td>
            <td>{{s.ShowTime}}</td>
            <td>₹ {{s.ShowPrice}}</td>
        </tr>
        </tbody>
        </table>
        </div>
              </div>
            </div>

        <div class="row">
        <div class="col-md-1 my-4"></div>
        <div class="col-md-6 my-4" style="align-items: center;"> 
       <img :src="pieChartImage" alt="Pie Chart" style="width: 80%;" />
     </div>
        <div class="col-md-4 my-4">
          <ul class="showcase my-4" style="display: flex; padding-left: 20%;">
            <div style="margin-right: 70px;">
              <button type="button" class="btn" disabled
                style="width: 50px; height: 25px; border-top-left-radius: 10px; border-top-right-radius: 10px; border: 2px solid darkorange"></button>
            </div>
            <div>
              <button type="button" class="btn btn-danger" disabled
                style="width: 50px; height: 25px; border-top-left-radius: 10px; border-top-right-radius: 10px; border: 2px solid darkorange"></button>
            </div>
          </ul>
          <ul style="display: flex; padding-left: 20.5%;">
            <div style="margin-right: 60px; font-weight: bold;"><small>Available</small></div>
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
                          :value='seat.tno' title="click to select" v-model="selected" disabled
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
            </form>
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
                   pieChartImage: null
                 }
             },
             methods:{
              closeAlert() {
                  this.showAlert = false;
                  window.location.reload();
                  },
             fetchPieChartImage() {
                const ShowID =this.$route.params.ShowID;
                fetch('http://127.0.0.1:5000/chart/'+ShowID,{
                     method:"GET",
                     headers:{
                         "Content-Type":"application/json", 
                     }
                     })
                     .then(resp => resp.json())
                     .then(data =>{
                        console.log(data)
                        this.pieChartImage = `data:image/png;base64,${data.image}`
                     })
                     .catch(error => {
                         console.log(error)
                     })
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
                  this.array(),
                  this.fetchPieChartImage()
              },
         }
         </script>
         
         <style>
         
         </style>
    
         