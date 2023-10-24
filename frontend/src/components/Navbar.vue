<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary" data-bs-theme="dark">
    <div class="container-fluid">
          <router-link class="navbar-brand" to ="/" > <strong> Films </strong> <img src="../assets/movies.png" alt="BookMyTicket" width="50" height="50"> <strong>ForYou</strong></router-link>
     
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item"  v-if="this.$route.params.CityName">
            <button type="button" class="btn btn-link" @click="openModal(1)" style="text-decoration: none; color: white;" title="select your city"><strong>{{ this.$route.params.CityName}}</strong></button>
          </li>
          <li class="nav-item"  v-else>
            <button type="button" class="btn btn-link" @click="openModal(1)" style="text-decoration: none; color: white;" title="select your city"><strong>Gwalior</strong></button>
          </li>
        </ul>
        <div @click="openModal(5)" class="form-control me-2 search-bar-placeholder" style="width: 400px;" title="tap to search">
    Search movie tickets, cinemas
  </div>
      </div>
    </div>
    <div class="mx-2" v-if="!User" >
        <button type="button" class="btn btn-warning btn-sm" @click="openModal(2)" title="user's login"><strong>Login</strong></button>
      </div>
      <div v-else style="display: flex;">
        <button  type="button" class="btn btn-warning btn-sm" @click="logoutuser(token)" title="logout"><strong>logout</strong></button>&nbsp;
      </div>
    <div class="mx-2" id="SignUp">
      <button type="button" class="btn btn-warning btn-sm" @click="openModal(3)" title="Not registered? SignUp now"><strong>Signup</strong></button>
    </div>
    <div class="mx-2" id="AdminLogin" title="admin's login">
      <button type="button" class="btn btn-sm" @click="openModal(4)"> <img src="../assets/admin.png" alt="BookMyTicket" width="30" height="30"></button>
    </div>
  </nav>

 <!-- Modal 1 -->
 <div class="modal fade modal-lg" :class="{ 'show': activeModal === 1 }" id="exampleModal1" tabindex="-1" aria-labelledby="exampleModalLabel1" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h1 class="modal-title fs-5" id="exampleModalLabel1">Select City</h1>
              <button type="button" class="btn-close" @click="closeModal(1)" aria-label="Close"></button>
            </div>
        <div class="modal-body">
          <h5 align="center">Popular Cities</h5>
          <ul style="overflow:hidden;">
            <router-link to="/FilmsForYou/Mumbai" @click="city('Mumbai')" style="color: black;">
              <li style="display:inline-block;
                    padding: 35px;" align="center"><img src="../assets/gate-of-india.png" alt="Mumbai" width="70"
                  height="70"><br>Mumbai</li>
            </router-link>
            <router-link to="/FilmsForYou/Gwalior" @click="city('Gwalior')"  style="color: black;">
              <li style="display:inline-block;
                    padding: 35px;" align="center"><img src="../assets/gateway.png" alt="Gwalior" width="70"
                  height="70"><br>Gwalior</li>
            </router-link>
            <router-link to="/FilmsForYou/Delhi-NCR" @click="city('Delhi-NCR')" style="color: black;">
              <li style="display:inline-block;
                    padding: 35px;" align="center"><img src="../assets//hyderabad-charminar.png" alt="Delhi"
                  width="70" height="70"><br>Delhi</li>
            </router-link>
            <router-link to="/FilmsForYou/Agra" @click="city('Agra')" style="color: black;">
              <li style="display:inline-block;
                    padding: 35px;" align="center"><img src="../assets/taj-mahal.png" alt="Agra" width="70"
                  height="70"><br>Agra
              </li>
            </router-link>
            <router-link to="/FilmsForYou/Chennai" @click="city('Chennai')" style="color: black;">
              <li style="display:inline-block;
                    padding: 35px;" align="center"><img src="../assets/temple.png" alt="Chennai" width="70"
                  height="70"><br>Chennai
              </li>
            </router-link>
          </ul>
          <form @submit.prevent="searchCity" class="d-flex" role="search">
            <input class="form-control me-2" type="search" v-model="CityName" placeholder="search for your city" aria-label="Search"
              name="cityname" id="cityname" style="width: 700px; margin: 0 auto;">
            <button type="submit" class="btn btn-danger">Search</button>
          </form>
        </div>
            </div>
          </div>
        </div>
  
      <!-- Modal 2 -->
      <div class="modal fade" :class="{ 'show': activeModal === 2 }" id="exampleModal2" tabindex="-1" aria-labelledby="exampleModalLabel2" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h1 class="modal-title fs-5" id="exampleModalLabel2">Login</h1>
              <button type="button" class="btn-close" @click="closeModal(2)" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <form @submit.prevent="getuser">
            <div class="mb-3">
              <label for="exampleInputEmail1" class="form-label">Username</label>
              <input type="name" class="form-control" name="username" id="username" aria-describedby="emailHelp" v-model="UserName">
            </div>
            <div class="mb-3">
              <label for="exampleInputPassword1" class="form-label">Password</label>
              <input type="password" class="form-control" name="password" id="password" v-model="Password">
            </div>
            <button type="submit" class="btn btn-danger">Submit</button>
          </form>
            </div>
          </div>
        </div>
      </div>
      
  
      <!-- Modal 3 -->
      <div class="modal fade" :class="{ 'show': activeModal === 3 }" id="exampleModal3" tabindex="-1" aria-labelledby="exampleModalLabel3" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h1 class="modal-title fs-5" id="exampleModalLabel3">SignUp</h1>
              <button type="button" class="btn-close" @click="closeModal(3)" aria-label="Close"></button>
            </div>
            <div class="modal-body">
            <form @submit.prevent="setuser" >
            <div class="mb-3">
              <label for="exampleInputEmail1" class="form-label">Email address</label>
              <input type="email" class="form-control" name="email" id="email" aria-describedby="emailHelp" v-model="Email">
              <div id="emailHelp" class="form-text">We'll never share your email with anyone else.</div>
            </div>
            <div class="mb-3">
              <label for="exampleInputEmail1" class="form-label">Username</label>
              <input type="name" class="form-control" name="username" id="username" aria-describedby="emailHelp" v-model="UserName">
            </div>
            <div class="mb-3">
              <label for="exampleInputPassword1" class="form-label">Password</label>
              <input type="password" class="form-control" name="password" id="password" v-model="Password">
            </div>
            <button type="submit" class="btn btn-danger">Submit</button>
          </form>
            </div>
          </div>
        </div>
      </div>


       <!-- Modal 4 -->
       <div class="modal fade" :class="{ 'show': activeModal === 4 }" id="AdminLogin" tabindex="-1" aria-labelledby="exampleModalLabel2" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h1 class="modal-title fs-5" id="exampleModalLabel2">Admin Login</h1>
              <button type="button" class="btn-close" @click="closeModal(4)" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <form @submit.prevent="adminlogin">
            <div class="mb-3">
              <label for="exampleInputEmail1" class="form-label">Username</label>
              <input type="name" class="form-control" name="username" id="username" aria-describedby="emailHelp" v-model="UserName">
            </div>
            <div class="mb-3">
              <label for="exampleInputPassword1" class="form-label">Password</label>
              <input type="password" class="form-control" name="password" id="password" v-model="Password">
            </div>
            <button type="submit" class="btn btn-danger">Submit</button>
          </form>
            </div>
          </div>
        </div>
      </div>

      <!-- Modal 5 -->
      <div class="modal fade modal-lg" :class="{ 'show': activeModal === 5 }" id="exampleModal1" tabindex="-1" aria-labelledby="exampleModalLabel1" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h1 class="modal-title fs-5" id="exampleModalLabel1">Search by filters</h1>
        <button type="button" class="btn-close" @click="closeModal(5)" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        <form @submit.prevent="searchbar" class="d-flex flex-column" role="search">
         <div class="container" style="display: flex;">

          <div class="form-group" style="width: 30%; margin: 0;">
            <label for="dropdown1" style="padding-bottom: 10px; ">Select Time:</label>
            <select id="dropdown1" v-model="selectedOption1" class="form-control">
              <option disabled value="">Please select an option</option>
              <option v-for="option in Time[0]" :value="option" :key="option">{{ option }}</option>
            </select>
            <p v-if="selectedOption1">You selected: {{ selectedOption1 }}</p>
          </div>&nbsp;&nbsp;&nbsp;&nbsp;

          <div class="form-group" style="width: 30%;">
            <label for="dropdown2" style="padding-bottom: 10px; ">Select Tag:</label>
            <select id="dropdown2" v-model="selectedOption2" class="form-control">
              <option disabled value="">Please select an option</option>
              <option v-for="option in Tags[0]" :value="option" :key="option">{{ option }}</option>
            </select>
            <p v-if="selectedOption2">You selected: {{ selectedOption2 }}</p>
          </div>&nbsp;&nbsp;&nbsp;&nbsp;

          <div class="form-group" style="width: 30%;">
            <label for="dropdown3" style="padding-bottom: 10px; ">Select Language:</label>
            <select id="dropdown3" v-model="selectedOption3" class="form-control" >
              <option disabled value="">Please select an option</option>
              <option v-for="option in Language" :value="option" :key="option">{{ option }}</option>
            </select>
            <p v-if="selectedOption3">You selected: {{ selectedOption3 }}</p>
          </div>&nbsp;&nbsp;&nbsp;&nbsp;

          <div class="form-group" style="width: 30%;">
            <label for="dropdown4" style="padding-bottom: 10px; ">Select City:</label>
            <select id="dropdown4" v-model="selectedOption4" class="form-control">
              <option disabled value="">Please select an option</option>
              <option v-for="option in Cities[0]" :value="option" :key="option">{{ option }}</option>
            </select>
            <p v-if="selectedOption4">You selected: {{ selectedOption4 }}</p>
          </div>

         </div>
         <br>

        <div style="padding-left: 1%; padding-right: 1%;">
          <div class="form-group">
            <label for="cityname" style="padding-bottom: 10px; ">Search for venues and shows:</label>
            <input class="form-control" type="search" v-model="searchfield" placeholder="Search movie tickets, cinemas" aria-label="Search" name="cityname" id="cityname">
          </div>
          <br>
          <button type="submit" class="btn btn-danger" style="width: 12%; ">Search</button>
        </div>
        </form>
      </div>
    </div>
  </div>
</div>
<div class="container">
  <div v-if="msg.length != 0 && showAlert" class="alert alert-warning alert-dismissible fade show mt-5" role="alert">
   <strong>{{ msg[0] }}</strong>
   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close" @click="closeAlert"></button>
    </div>
</div>
</template>


<script>
import { useRoute } from 'vue-router';
const route = useRoute();

  export default {
    data() {
      return {
        activeModal: null,
        token : localStorage.getItem('user'),
        User : localStorage.getItem('auth'),
        Time: [],
        Tags:[],
        Cities:[],
        Language: ["Hindi", "English"],
        msg: [],
        showAlert: true,
      };
    },
    methods: {
      closeAlert() {
              this.showAlert = false;
              window.location.reload();
              },
      openModal(modalNumber) {
        this.activeModal = modalNumber;
      },
      closeModal(modalNumber) {
        this.activeModal = null;
      },
      searchCity(){
        if(!this.CityName){
            this.msg.push("Please fill CityName")
          }
        if(this.CityName in this.Cities){
          const CityName =this.CityName
          this.$router.push('/FilmsForYou/'+CityName)
        }
        else{
          this.msg.push("City Not Found")
          this.closeModal(1)
            }
      },
      city(c){
        const CityName = c
        this.closeModal(1)
        this.$router.push('/FilmsForYou/'+CityName).then(() => {
                  window.location.reload();
  });
      },
      getuser(){
        if(!this.Password || !this.UserName){
                this.msg.push("Please fill all the fields")
                this.closeModal(2)
            }else{
              fetch('http://127.0.0.1:5000/login/'+this.UserName+'/'+this.Password,{
              method:"POST",
              headers:{
                  "Content-Type":"application/json"
              }
              })
              .then(resp => resp.json())
              .then(data =>{
                if (data === 401){
                  this.msg.push("Please login with correct username and password.")
                  this.closeModal(2)
                  console.log(data)
                }
                else if(data===201){
                  this.msg.push("Please login with Admin's Login.")
                  this.closeModal(2)
                  console.log(data)
                }
                else{
                localStorage.setItem('user',data.access_token);
                localStorage.setItem('auth',data.User);
                localStorage.setItem('username',data.UserName);
                this.closeModal(2)
                window.location.reload();}},
                )
                .catch(error => {
                  console.log(error)
              })
             
            }
      },
      setuser(){
        if(!this.UserName || !this.Email || !this.Password){
          this.msg.push("Please fill all the fields")
          this.closeModal(3)
            }else{
                fetch('http://127.0.0.1:5000/signup',{
                method:"POST",
                headers:{
                    "Content-Type":"application/json"
                },
                body: JSON.stringify({UserName:this.UserName, Email:this.Email, Password: this.Password})
                })
                .then(resp => resp.json())
                this.closeModal(3)
                this.getuser()
                this.$router.push('/').then(() => {
                window.location.reload();});
                
            }
            
      },
      logoutuser(token){
                fetch('http://127.0.0.1:5000/logout',{
                method:"POST",
                headers:{
                    "Content-Type":"application/json",
                    "Authorization": "Bearer " + token
                },
                })
                .then(resp => resp.json())
                .then(data =>{
                  console.log(data)
                  this.$router.push('/').then(() => {
                  window.location.reload();
                  localStorage.clear()
                  
  });
              })
                
            
      },
      adminlogin(){
        if(!this.Password || !this.UserName){
                this.msg.push("Please fill all the fields")
            }else{
              fetch('http://127.0.0.1:5000/login/'+this.UserName+'/'+this.Password+'/'+1,{
              method:"POST",
              headers:{
                  "Content-Type":"application/json"
              }
              })
              .then(resp => resp.json())
              .then(data =>{
                if (data === 401){
                  this.msg.push("Please login with correct username and password.")
                  this.closeModal(4)
                  console.log(data.User)
                }
                else{localStorage.setItem('user',data.access_token);
                localStorage.setItem('auth',data.User);
                this.closeModal(4)
                this.$router.push('/cities').then(() => {
                  window.location.reload();
  });
                }},
                )
                .catch(error => {
                  console.log(error)
              })
             
            }},
            getsearchdetails(){
              fetch('http://127.0.0.1:5000/searchdetails',{
              method:"GET",
              headers:{
                  "Content-Type":"application/json"
              }
              })
              .then(resp => resp.json())
              .then(data =>{
                this.Time.push(data['Time'])
                this.Tags.push(data['Tags'])
                this.Cities.push(data['Cities'])
              },
                )
                .catch(error => {
                  console.log(error)
              })
      },
            searchbar(){
              fetch('http://127.0.0.1:5000/search',{
                method:"POST",
                headers:{
                    "Content-Type":"application/json"
                },
                body: JSON.stringify({selectedOption1:this.selectedOption1,
                                      selectedOption2:this.selectedOption2,
                                      selectedOption3:this.selectedOption3,
                                      searchfield: this.searchfield,
                                      selectedOption4:this.selectedOption4})
                })
                .then(resp => resp.json())
                .then(data =>{
                  this.$router.push({ path: '/search', query: { data: JSON.stringify(data) } }).then(() => {
                  window.location.reload();
  }
                )},
                )
                .catch(error => {
                  console.log(error)
              }) 
            }
    },
    created(){
      this.getsearchdetails()
    }
  };
  </script>
  
  <style scoped>
  .modal {
    display: none;
    background: rgba(0, 0, 0, 0.5);
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
  }
  
  .modal.show {
    display: block;
  }
  </style>
