<template>
    <div>
        <div v-if="this.$route.query.data === '401'"><br><br>
            <h2 style="text-align: center; color: #333333;">Please Fill more Fields in the Searchbar for Searching Results</h2>
            <br><h3 style="text-align: center; color: #333333;">"404 Result Not Found"</h3>
        </div>
        <div v-else-if="this.$route.query.data === '404'"><br><br>
            <h2 style="text-align: center; color: #333333;">Sorry No Movie Found</h2>
            <br><h3 style="text-align: center; color: #333333;">"404 Result Not Found"</h3>
        </div>
    <div class="container" v-else>
        <br><br>
        <h2 style="text-align: center; color: #333333;">Your Searched Results</h2>
        <br><br> 
    <div class="container">
   <table class="table table-striped">
        <thead>
          <tr>
            <th scope="col">SNo</th>
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
          <tr v-for = "(show,index) in JSON.parse(this.$route.query.data)" :key="show.ShowID">
            <th>{{index+1}}</th>
            <td>{{show["ShowName"]}}</td>
            <td>{{show["ShowRating"]}}</td>
            <td>{{show["ShowTag"]}}</td>
            <td>{{show["ShowLanguage"]}}</td>
            <td>{{show["ShowTime"]}}</td>
            <td>₹ {{show["ShowPrice"]}}</td>
            <td><router-link class="btn btn-warning btn-sm" :to="{name:'seating', params:{ShowID:show['ShowID'], VenueID:show['VenueID']}}">Book Now</router-link></td>
          </tr>
        </tbody>
      </table>
    </div>
</div>
</div>
</template>

<script>
export default {

}
</script>

<style>

</style>