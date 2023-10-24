import { createRouter, createWebHistory } from "vue-router";
import Cities from './components/Cities'
import Venues from './components/Venues'
import Shows from './components/Shows'
import UpdateCity from './components/UpdateCity'
import UpdateVenue from './components/UpdateVenue'
import UpdateShow from './components/UpdateShow'
import Seating from './components/Seating'
import Index from './components/Index'
import Venueshow from './components/Venueshow'
import SelectedCity from './components/SelectedCity'
import Booked from './components/Booked'
import Search from './components/Search'
import DashBoard from './components/DashBoard'

const routes = [
    {
        path : '/cities',
        name:'cities',
        component : Cities
    },
    {
        path : '/venue/:CityName',
        name:'venue',
        component : Venues,
        props: true

    },
    {
        path : '/show/:VenueID',
        name:'show',
        component : Shows,
        props: true

    },
    {
        path : '/updatecity/:CityName',
        name:'updatecity',
        component : UpdateCity,
        props: true

    },
    {
        path : '/updatevenue/:CityName/:VenueID',
        name:'updatevenue',
        component : UpdateVenue,
        props: true

    },
    {
        path : '/updateshow/:VenueID/:ShowID',
        name:'updateshow',
        component : UpdateShow,
        props: true

    },
    {
        path : '/seating/:VenueID/:ShowID',
        name:'seating',
        component : Seating,
        props: true
    },
    {
        path : '/dashboard/:VenueID/:ShowID',
        name:'dashboard',
        component : DashBoard,
        props: true
    },
    {
        path : '/',
        name:'index',
        component : Index,
    },
    {
        path : '/VenueShows/:VenueID',
        name:'venueshow',
        component : Venueshow,
        props: true
    },
    {
        path : '/FilmsForYou/:CityName',
        name:'selectedcity',
        component : SelectedCity,
        props: true
    },
    {
        path : '/booked/:ShowID/:tickets',
        name:'booked',
        component : Booked,
        props:true
    },
    {
        path : '/search',
        name:'search',
        component : Search,
    },
 
]


const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router;