# ------------------------------------- imports -----------------------------------------------
import calendar
import csv
from datetime import datetime, timedelta
import os
from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt
from celery import Celery, Task
from celery.schedules import crontab
from jinja2 import Template
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import *
from weasyprint import HTML
from flask_caching import Cache
from time import perf_counter_ns
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# ---------------------------------------------------------------------------------

app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)
CORS(app)

app.config['JWT_SECRET_KEY'] = 'Nandini'
app.config['SECRET_KEY'] = 'Nandini'

current_dir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + \
    os.path.join(current_dir, "database2.sqlite3")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()

# -----------------------------------------CELERY INSTANCE---------------------------------------------------------

def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app

app.config.from_mapping(
    CELERY=dict(
        broker_url="redis://localhost:6379/1",
        result_backend="redis://localhost:6379/2",
        enable_utc=False,
        timezone="Asia/Kolkata"
    ),
)
celery_app = celery_init_app(app)

#  --------------------------------------CACHING INSTANCE------------------------------------------------

def make_cache():
    cache_mapping = {
        "CACHE_TYPE": "RedisCache",
        "CACHE_REDIS_HOST": "localhost",
        "CACHE_REDIS_PORT": 6379
    }

    app.config.from_mapping(cache_mapping) 

    cache = Cache(app) 
    app.app_context().push()

    return cache


current_cache_inst = make_cache()

# --------------------------------------JWT Tokenization funtions for Logout Functionality------------------------------------------

blocked_tokens = set()

@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return str(jti) in blocked_tokens

@jwt.revoked_token_loader
def token_logout(jwt_header, jwt_payload):
    return ({"description": "User Logged out"}), 401  

#  -------------------------------------SMTP server and mailhog setup -----------------------------------

SMTP_SERVER_HOST = "localhost"
SMTP_SERVER_PORT =1025
SENDER_ADDRESS ="no-reply@ticketsforyou.com"
SENDER_PASSWORD = ""

def send_email(to_address, subject, message, content = "text", attachment_file =None):
    mail = MIMEMultipart()
    mail["From"] = SENDER_ADDRESS
    mail["To"] = to_address
    mail["Subject"] = subject
    

    if content == "html":
        mail.attach(MIMEText(message, "html"))
    else:
        mail.attach(MIMEText(message, "plain"))

    if attachment_file:
        with open(attachment_file, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encode_base64(part)

        part.add_header(
            "Content-Disposition", f"attachment; filename={attachment_file}")
        mail.attach(part)

    s = smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(mail)
    s.quit()

    return True   


# ------------------------- Dtatabase Models of the application -----------------------------

class Login(db.Model):
    __tablename__ = 'login'
    Email = db.Column(db.String(200), nullable=False)
    UserName = db.Column(db.String(500), primary_key=True)
    Password = db.Column(db.String(500), nullable=False)
    LastVisited =db.Column(db.String(100), nullable =True)
    Admin = db.Column(db.Integer) 
    TicketR = db.relationship('Ticket', backref='login', lazy=True)


class City(db.Model):
    __tablename__ = 'city'
    StateName = db.Column(db.String(100), nullable=False)
    CityName = db.Column(db.String(100), primary_key=True)
    VenueR = db.relationship('Venue', backref='city', lazy=True)


class Venue(db.Model):
    __tablename__ = 'venue'
    VenueID = db.Column(db.String(50), primary_key=True)
    VenueName = db.Column(db.String(200), nullable=False)
    VenuePlace = db.Column(db.String(200), nullable=False)
    VenueCapacity = db.Column(db.Integer, nullable=False)
    ShowR = db.relationship('Show', backref='venue', lazy=True)
    TicketR = db.relationship('Ticket', backref='venue', lazy=True)
    CityName = db.Column(db.String(100), db.ForeignKey(
        'city.CityName'), nullable=False)


class Show(db.Model):
    __tablename__ = 'show'
    ShowID = db.Column(db.String(50), primary_key=True)
    ShowName = db.Column(db.String(200), nullable=False)
    ShowRating = db.Column(db.Integer, nullable=True)
    ShowTag = db.Column(db.String(50), nullable=False)
    ShowLanguage = db.Column(db.String(50), nullable=False)
    ShowTime = db.Column(db.String(50), nullable=False)
    ShowPrice = db.Column(db.Integer, nullable=False)
    TicketR = db.relationship('Ticket', backref='show', lazy=True)
    VenueID = db.Column(db.String(50), db.ForeignKey(
        'venue.VenueID'), nullable=False)


class Ticket(db.Model):
    __tablename__ = 'ticket'
    sno = db.Column(db.Integer, primary_key=True)
    tno = db.Column(db.Integer)
    Booked = db.Column(db.Integer, default=0)
    ShowID = db.Column(db.String(50), db.ForeignKey('show.ShowID'))
    Rate = db.Column(db.Integer, default=0)
    UserName = db.Column(db.String(500), db.ForeignKey(
        'login.UserName'), nullable=True)
    VenueID = db.Column(db.String(50), db.ForeignKey('venue.VenueID'))

# -------------------------------------Request Parser----------------------------------

city_post_args = reqparse.RequestParser()
city_post_args.add_argument("CityName", type=str, help="City Name required", required=True)
city_post_args.add_argument("StateName", type=str,help="State Name required", required=True)

city_update_args = reqparse.RequestParser()
city_update_args.add_argument("CityName", type=str, required=False)
city_update_args.add_argument("StateName", type=str, required=False)

venue_post_args = reqparse.RequestParser()
venue_post_args.add_argument("VenueID", type=str, help="Venue ID required", required=True)
venue_post_args.add_argument("VenueName", type=str, help="Venue Name required", required=True)
venue_post_args.add_argument("VenuePlace", type=str, help="Venue Palce required", required=True)
venue_post_args.add_argument("VenueCapacity", type=int, help="Venue Capacity required", required=True)
venue_post_args.add_argument("CityName", type=str, help="City Name required", required=True)

venue_update_args = reqparse.RequestParser()
venue_update_args.add_argument("VenueID", type=str, required=False)
venue_update_args.add_argument("VenueName", type=str, required=False)
venue_update_args.add_argument("VenuePlace", type=str, required=False)
venue_update_args.add_argument("VenueCapacity", type=int,required=False)

show_post_args = reqparse.RequestParser()
show_post_args.add_argument("ShowID", type=str, help="Show ID required", required=True)
show_post_args.add_argument("ShowName", type=str, help="Show Name required", required=True)
show_post_args.add_argument("ShowRating", type=int, help="Show Rating required", required=True)
show_post_args.add_argument("ShowTag", type=str, help="Show Tag required", required=True)
show_post_args.add_argument("ShowLanguage", type=str, help="Show Language required", required=True)
show_post_args.add_argument("ShowTime", type=str, help="Show Time required", required=True)
show_post_args.add_argument("ShowPrice", type=int, help="Show Price required", required=True)
show_post_args.add_argument("VenueID", type=str, help="Venue ID required", required=True)


show_update_args = reqparse.RequestParser()
show_update_args.add_argument("ShowID", type=str, required=False)
show_update_args.add_argument("ShowName", type=str,required=False)
show_update_args.add_argument("ShowRating", type=int,required=False)
show_update_args.add_argument("ShowTag", type=str, required=False)
show_update_args.add_argument("ShowLanguage", type=str,required=False)
show_update_args.add_argument("ShowTime", type=str, required=False)
show_update_args.add_argument("ShowPrice", type=int,required=False)

ticket_args = reqparse.RequestParser()
ticket_args.add_argument("List", type=str, help="list required", required=True)
ticket_args.add_argument("ShowID", type=str, help="ShowID required", required=True)

user_post_args = reqparse.RequestParser()
user_post_args.add_argument("UserName", type=str, help="Show ID required", required=True)
user_post_args.add_argument("Email", type=str, help="Show Name required")
user_post_args.add_argument("Password", type=str, help="Show Rating required", required=True)

user_login_args = reqparse.RequestParser()
user_login_args.add_argument("UserName", type=str, help="Show ID required", required=True)
user_login_args.add_argument("Password", type=str, help="Show Rating required", required=True)

search = reqparse.RequestParser()
search.add_argument("selectedOption1", type=str, help="Show ID required")
search.add_argument("selectedOption2", type=str, help="Show Rating required")
search.add_argument("selectedOption3", type=str, help="Show Rating required")
search.add_argument("selectedOption4", type=str, help="Show Rating required")
search.add_argument("searchfield", type=str, help="Show Rating required")

# ----------------------------------- Recource Fields ---------------------------------------------

resourse_fields_city = {
    "CityName": fields.String,
    "StateName": fields.String,
}
resourse_fields_venue = {
    "VenueID": fields.String,
    "VenueName": fields.String,
    "VenuePlace": fields.String,
    "VenueCapacity": fields.Integer,
    "CityName": fields.String,
}
resourse_fields_show = {
    "ShowID": fields.String,
    "ShowName": fields.String,
    "ShowRating": fields.Float,
    "ShowTag": fields.String,
    "ShowLanguage": fields.String,
    "ShowTime": fields.String,
    "ShowPrice": fields.Integer,
    "VenueID": fields.String,
}

resourse_fields_ticket = {
    "tno": fields.Integer,
    "Booked": fields.Integer,
    "ShowID": fields.String,
    "UserName": fields.String,
    "VenueID": fields.String,
    "Rate": fields.Integer,
}

resourse_fields_index = {
    "CityName": fields.String,
    "StateName": fields.String,
    "VenueID": fields.String,
    "VenueName": fields.String,
    "VenuePlace": fields.String,
    "VenueCapacity": fields.Integer,
    "ShowID": fields.String,
    "ShowName": fields.String,
    "ShowRating": fields.Float,
    "ShowTag": fields.String,
    "ShowLanguage": fields.String,
    "ShowTime": fields.String,
    "ShowPrice": fields.Integer
}

resourse_fields_user = {
    "UserName": fields.String,
    "Email": fields.String,
    "Password": fields.String,
    "Admin":fields.Integer,
}



#  ----------------------------------------RestFul APIs -------------------------------------

class Cities(Resource):  
    @jwt_required()
    @marshal_with(resourse_fields_city)  
    def get(self):     #Gives all the cities in the data
        if request.headers.get('UserAuth') == 'Admin':  #Only admins can access all the cities
            cities = City.query.all()
            return cities


class Venues(Resource):  
    @marshal_with(resourse_fields_venue)
    def get(self, CityName): #Gives all the venues of a perticular city
        venue = Venue.query.filter_by(CityName=CityName).all()
        return venue
   
class Shows(Resource):  
    @marshal_with(resourse_fields_show)
    def get(self, VenueID): #Gives all the shows of a perticular venue
        shows = Show.query.filter_by(VenueID=VenueID).all()
        return shows
       

#---------------------------- CRUD For Cities -------------------------------

class CityApi(Resource): #Only Admin can access these APIs 
    @jwt_required()
    @marshal_with(resourse_fields_city)
    def get(self,CityName):  #To get the city data for the update page of city
        if request.headers.get('UserAuth') == 'Admin': 
            city = City.query.filter_by(CityName=CityName).first()
            return city
        else:
            return 401

    @jwt_required()  
    @marshal_with(resourse_fields_city)
    def post(self, CityName):  #Add the city in the database
        if request.headers.get('UserAuth') == 'Admin':
            args = city_post_args.parse_args()
            cities = City.query.all()
            c = City.query.filter_by(CityName=CityName).first()
            if c in cities:
                abort(409)

            c1 = City(CityName=args['CityName'], StateName=args['StateName'])
            db.session.add(c1)
            db.session.commit()
            return c1, 201
    
    @jwt_required()
    @marshal_with(resourse_fields_city)
    def put(self, CityName): #Update the fields of City in the database
        if request.headers.get('UserAuth') == 'Admin':
            args = city_update_args.parse_args()
            c = City.query.filter_by(CityName=CityName).first()
            if not c:
                abort(404)
            if args['CityName']:
                c.CityName = args['CityName']
            if args['StateName']:
                c.StateName = args['StateName']
            db.session.commit()
            return c
    
    @jwt_required()
    def delete(self, CityName):   #Delete the City
        if request.headers.get('UserAuth') == 'Admin':
            city = City.query.filter_by(CityName=CityName).first()
            venue = Venue.query.filter_by(CityName= CityName).all()
            shows = Show.query.all()
            tickets = Ticket.query.all()
            show = []
            ticket =[]
            for v in venue:
                for s in shows:
                    if v.VenueID == s.VenueID:
                        show.append(s)

            for i in venue:
                for t in tickets:
                    if i.VenueID == t.VenueID:
                        ticket.append(t)
    
            for d3 in ticket:
                db.session.delete(d3) 
                db.session.commit()    

            for d2 in show:
                db.session.delete(d2)
                db.session.commit()  
            
            for d1 in venue:
                db.session.delete(d1)
                db.session.commit()  

            db.session.delete(city)
            db.session.commit()
            return 'City Deleted', 204

#---------------------------- CRUD For Venues ------------------------------

class VenueApi(Resource): #Only Admin can access these APIs 
    @marshal_with(resourse_fields_venue)
    def get(self, VenueID):  #To get the venue data for the update page of venue
        v = Venue.query.filter_by(VenueID = VenueID).first()
        return v
         
    @jwt_required()
    @marshal_with(resourse_fields_venue)
    def post(self, VenueID):  #Adding a venue in a city
         if request.headers.get('UserAuth') == 'Admin':
                args = venue_post_args.parse_args()
                venues = Venue.query.all()
                v = Venue.query.filter_by(VenueID=VenueID).first()
                if v in venues:
                    abort(409)

                venue =Venue(VenueID=args['VenueID'], 
                            VenueName=args['VenueName'], 
                            VenuePlace = args['VenuePlace'], 
                            VenueCapacity = args['VenueCapacity'],
                            CityName = args['CityName']
                            )
                db.session.add(venue)
                db.session.commit()
                return venue, 201
    
    @jwt_required()
    @marshal_with(resourse_fields_venue)
    def put(self, VenueID):   #Updating the venue
         if request.headers.get('UserAuth') == 'Admin':
                args = venue_update_args.parse_args()
                venue = Venue.query.filter_by(VenueID=VenueID).first()
                if not venue:
                    abort(404)
                if args['VenueID']:
                    venue.VenueID = args['VenueID']
                if args['VenueName']:
                    venue.VenueName = args['VenueName']
                if args['VenuePlace']:
                    venue.VenuePlace = args['VenuePlace']
                if args['VenueCapacity']:
                    venue.VenueCapacity = args['VenueCapacity']
                db.session.commit()
                return venue
    
    @jwt_required()
    def delete(self, VenueID): #Delete Venue
         if request.headers.get('UserAuth') == 'Admin':
                venue = Venue.query.filter_by(VenueID = VenueID).first()
                shows = Show.query.filter_by(VenueID = VenueID).all()
                ticket = Ticket.query.filter_by(VenueID = VenueID).all()

                for t in ticket:
                    db.session.delete(t) 
                    db.session.commit()    

                for s in shows:
                    db.session.delete(s)
                    db.session.commit()  

                db.session.delete(venue)
                db.session.commit()
                return 'Venue Deleted', 204

#---------------------------- CRUD For Shows --------------------------------

class ShowApi(Resource): #Only Admin can access these APIs 
    @marshal_with(resourse_fields_show)
    def get(self, ShowID): #To get the show data for the update page of show
        show = Show.query.filter_by(ShowID=ShowID).first()
        return show
         
    @jwt_required()
    @marshal_with(resourse_fields_show)
    def post(self, ShowID): #Add a show in a venue
         if request.headers.get('UserAuth') == 'Admin':
                args = show_post_args.parse_args()
                shows = Show.query.all()
                s = Show.query.filter_by(ShowID= ShowID).first()
                if s in shows:
                    abort(409)

                show = Show(ShowID=args['ShowID'], 
                            ShowName=args['ShowName'], 
                            ShowRating=args['ShowRating'],
                            ShowTag=args['ShowTag'],
                            ShowLanguage=args['ShowLanguage'],
                            ShowTime=args['ShowTime'],
                            ShowPrice=args['ShowPrice'],
                            VenueID = args['VenueID'])
                db.session.add(show)
                db.session.commit()

                VenueID = show.VenueID
                venue = Venue.query.filter_by(VenueID=VenueID).first()
                capacity = int(venue.VenueCapacity)
                for i in range(capacity):
                    tno=i+1
                    ShowID=ShowID
                    VenueID=VenueID
                    t= Ticket(tno=tno, ShowID= ShowID, VenueID=VenueID,  Booked = 0, UserName= None)
                    db.session.add(t)
                    db.session.commit()
                
                return show, 201

    @jwt_required()
    @marshal_with(resourse_fields_show)
    def put(self, ShowID):  #Update the Show
         if request.headers.get('UserAuth') == 'Admin':
                args = show_update_args.parse_args()
                show = Show.query.filter_by(ShowID = ShowID).first()
                
                if not show:
                    abort(404)
                if args['ShowID']:
                    show.ShowID = args['ShowID'] 
                if args['ShowName']:
                    show.ShowName = args['ShowName']
                if args['ShowRating']:
                    show.ShowRating = args['ShowRating']
                if args['ShowTag']:
                    show.ShowTag = args['ShowTag']
                if args['ShowLanguage']:
                    show.ShowLanguage = args['ShowLanguage']
                if args['ShowTime']:
                    show.ShowTime = args['ShowTime']
                if args['ShowPrice']:
                    show.ShowPrice = args['ShowPrice']
                db.session.commit()
                return show
    
    @jwt_required()
    def delete(self, ShowID):  #Delete  the Show
         if request.headers.get('UserAuth') == 'Admin':
                show = Show.query.filter_by(ShowID = ShowID).first()
                ticket = Ticket.query.filter_by(ShowID = ShowID).all()
                for t in ticket:
                    db.session.delete(t) 
                    db.session.commit()      

                db.session.delete(show)
                db.session.commit()
                return 'City Deleted', 204
    
#---------------------------- GET For Tickets ---------------------

class Tickets(Resource):
    @marshal_with(resourse_fields_ticket)
    def get(self, ShowID): #For getting the list of tickets of a perticular Show
        ticket = Ticket.query.filter_by(ShowID=ShowID).all()
        return ticket

#---------------------------- API For Index ---------------------
class IndexApi(Resource):
    @marshal_with(resourse_fields_index)
    def post(self, CityName):  #For getting the shows and venue of a city in one go for the Index pages
        if City.query.filter_by(CityName=CityName).first():
            venues = Venues.get(self,CityName)
            shows=[]
            result=[]
            for i in venues:
                s= Shows.get(self,i['VenueID'])
                for j in s:
                    shows.append(j)
            result.append(venues)
            result.append(shows)
            return result
        else:
            return 401

#---------------------------- API for Signup -------------------------------------
class UserSignupApi(Resource):  
    def post(self):        #signup for user
        args = user_post_args.parse_args()
        UserName=args['UserName']
        user = Login.query.filter_by(UserName=UserName).first()
        if user:
            abort(409)
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        user =Login(UserName=args['UserName'], 
                    Email=args['Email'], 
                    Password = args['Password'],
                    LastVisited = dt_string,
                    Admin = 0
                     )
        db.session.add(user)
        db.session.commit()
        access_token = create_access_token(identity=args['UserName'])
        return {'access_token': access_token, 'UserName':args['UserName'] , 'User': 'User'}, 200
    
#---------------------------- API for Login ---------------------

class UserLoginApi(Resource):  
      def post(self,UserName,Password): #seperate login for user
        user = Login.query.filter_by(UserName=UserName, Password=Password).first()
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        if user != None and user.Admin == 0:
            access_token = create_access_token(identity=UserName)
            user.LastVisited = dt_string
            db.session.commit()
            return {'access_token': access_token, 'UserName':UserName, 'User': 'User'}, 200
        elif user != None and user.Admin == 1:
            return 201
        else:
            return 401
        
#---------------------------- API for Login ---------------------

class AdminLoginApi(Resource):  
      def post(self,UserName,Password,Admin):   #seperate login for admin
        user = Login.query.filter_by(UserName=UserName, Password=Password, Admin=Admin).first()
        if user != None and user.Admin == 1:
            access_token = create_access_token(identity=UserName)
            return {'access_token': access_token, 'UserName':UserName, 'User': 'Admin'}, 200
        else:
            return 401

#---------------------------- API for Logout ---------------------

class UserLogoutApi(Resource):
    @jwt_required()
    def post(self):   #For logout
        jti = str(get_jwt()["jti"])
        UserName = str(get_jwt()["sub"])
        user = Login.query.filter_by(UserName=UserName).first()
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        user.LastVisited = dt_string
        db.session.commit()
        blocked_tokens.add(jti)
        return {"msg": "Succesfully logged out"}
    

#---------------------------- API for Booking ---------------------
class Booked(Resource):
    @jwt_required()
    def put(self):  #Booking multiple tickets
        user = str(get_jwt()["sub"])
        if user:
            args = ticket_args.parse_args()
            ShowID = args['ShowID']
            tickets = Ticket.query.filter_by(ShowID=ShowID).all()
            selectedtickets = args['List'].split(',')
            for i in selectedtickets:
                for j in tickets:
                    if int(i) == j.tno:
                        j.Booked = 1
                        j.UserName = user
                    db.session.commit()
            download_ticket.delay(ShowID, selectedtickets,user)
            return "done"
        else:
            return 401

#---------------------------- API for Rating ---------------------

class Rating(Resource):
    @jwt_required()
    def put(self, Rating): #Rating the movie for which user has booked the tickets
        user = str(get_jwt()["sub"])
        if user:
            args = ticket_args.parse_args()
            ShowID = args['ShowID']
            Rating = Rating
            tickets = Ticket.query.filter_by(ShowID=ShowID).all()
            selectedtickets = args['List'].split(',')
            for i in selectedtickets:
                for j in tickets:
                    if int(i) == j.tno:
                        j.Rate = int(Rating)
                    db.session.commit()

            show = Show.query.filter_by(ShowID=ShowID).first()
            sum = 0
            count =0
            for k in tickets:
                sum+= k.Rate
                if k.Rate > 0:
                    count+=1
            avg= sum/count
            average= round(avg,2)
            show.ShowRating = average
            db.session.commit()
        else:
            return 401
        

# ----------------------------------API for Searching the details for search bar ----------------------

class SearchDetails(Resource):
    def get(self):   #Getting data for the serchbar of venues and shows for drop down menues
        result = searchdetails()
        return result
        
    
    def post(self):  #Searching the request of the user for venue or show
        args = search.parse_args()
        time = args['selectedOption1']
        city = args['selectedOption4']
        tag = args['selectedOption2']
        language = args['selectedOption3']
        field = args['searchfield']
        result = searching(time, city, tag, language,field)
        return result

@current_cache_inst.memoize(timeout=120)   #cahing is used  for above API 'SearchDetails'
@marshal_with(resourse_fields_show)
def searching(time, city, tag, language,field):
        if Venue.query.filter_by(VenueName= field, CityName=city).first() and city != None:
             venue = Venue.query.filter_by(VenueName= field, CityName = city).first()
             VenueID = venue.VenueID
             if time !=None and tag!= None and language != None:
                shows = Show.query.filter_by(VenueID=VenueID, ShowTag=tag, ShowTime= time, ShowLanguage=language).all()
                return shows
             
             elif time == None and tag== None and language== None:
                shows = Show.query.filter_by(VenueID=VenueID).all()
                return shows
             else:
                 return 404
             

        elif Show.query.filter_by(ShowName= field).first() and time !=None and tag!= None and language != None:
            shows = Show.query.filter_by(ShowName = field , ShowTime = time, ShowTag = tag, ShowLanguage=language).all()
            if len(shows)==0:
                    return 404
            return shows
        
        else:
            return 401

@current_cache_inst.memoize(timeout=120)  #cahing is used  for above API 'SearchDetails'
def searchdetails():
        Time= db.session.query(Show.ShowTime).group_by(Show.ShowTime).all()
        Tags = db.session.query(Show.ShowTag).group_by(Show.ShowTag).all()
        Ci = db.session.query(City.CityName).group_by(City.CityName).all()
        time = [str(t) for t in Time]
        tag = [str(tag) for tag in Tags]
        city = [str(c) for c in Ci]

        times = []
        tags =[]
        cities =[]

        for tuple_string in time:
            content = tuple_string.strip("(),'")  
            times.append(content)

        for tuple_string in tag:
            content = tuple_string.strip("(),'")  
            tags.append(content)

        for tuple_string in city:
            content = tuple_string.strip("(),'")  
            cities.append(content)

        response_data = {"Time": times, "Tags": tags, "Cities":cities}
        return response_data    
      
#  -------------------------------------------- Routers ------------------------------------------


@app.route('/export/<VenueID>', methods = ['GET'])
@jwt_required()
def export_venue(VenueID):  #Router for exporting csv file to the admin
        if request.method == 'GET':
            username = str(get_jwt()["sub"])
            user = Login.query.filter_by(UserName=username).first()
            data = {
                "Email":user.Email,
                "UserName":user.UserName,
            }
            venue_export.delay(VenueID, data)
            return {"message": "Done"}


@app.route('/chart/<ShowID>', methods=['GET'])
def get_pie_chart_data(ShowID):   #This is for creating the bar chart of booked and unbooked tickets
    categories = ['Booked', 'Unbooked']
    booked_tickets = Ticket.query.filter_by(ShowID=ShowID, Booked=1).count()
    unbooked_tickets = Ticket.query.filter_by(ShowID=ShowID, Booked=0).count()

    plt.figure(figsize=(8, 6))
    bars = plt.bar(categories, [booked_tickets, unbooked_tickets], color=['#FFA07A', '#FFD700'])
    plt.xlabel('Ticket Status')
    plt.ylabel('Number of Tickets')
    plt.title('Ticket Booking Status Bar Chart')

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval/2, f'({yval/sum([booked_tickets, unbooked_tickets])*100:.1f}%)', ha='center', va='center', color='#333333',fontsize=10, fontweight='bold')

    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()

    image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')

    return jsonify({'image': image_base64})



#  -------------------------------------------------------Backend Jobs---------------------------------------------------

@celery_app.on_after_finalize.connect
def setup_intervalTASK(sender, **kwargs): #schedule jobs
    sender.add_periodic_task(
        crontab(minute=00, hour=14),  #send reminder at 12 PM daily, if user is not logged in for more than 24hr
        send_reminder.s(), name="send_reminder"
    ),
    sender.add_periodic_task(
        crontab(minute=00, hour=14, day_of_month=8), #send monthly report at 12 PM on 1st day of the month
        monthly_report.s(), name="Monthly Report"
    )

@celery_app.task()
def send_reminder():
    users = Login.query.filter_by(Admin=0).all() #sending reminders mail only to the users
    now =  datetime.now()
    date_format = "%d/%m/%Y %H:%M:%S"
    send_reminder_to = []
    for user in users:
        lastvisit = datetime.strptime(user.LastVisited, date_format)
        if (now - lastvisit).total_seconds() >= 86400:
            send_reminder_to.append(user)
            

    with open(r"templates/reminder_mail.html") as file:  
        temp = Template(file.read())

    for user in send_reminder_to:
        message = temp.render(user=user)
        sub = f"[REMINDER] Films-Ticket-ForYou"
        send_email(to_address=user.Email, subject=sub, message=message, content="html")

    return {"msg": "send_reminder Complete"}

@celery_app.task()
def monthly_report():  #sending mail and pdf formatted file to the user redarding their monthly booking
    users = Login.query.all()
    current_date = datetime.now()
    last_month = current_date.replace(day=1) - timedelta(days=1)
    year = last_month.year
    previous_month = last_month.month
    month = calendar.month_name[previous_month]

    for user in users:
        UserName = user.UserName
        data = db.session.query(Ticket.tno, Ticket.UserName, Show.ShowTime, Show.ShowName, Venue.VenueName, Venue.VenuePlace,Venue.CityName, Show.ShowPrice, Show.ShowLanguage).join(Show, Ticket.ShowID == Show.ShowID).join(Venue, Ticket.VenueID == Venue.VenueID).filter(Ticket.UserName == UserName).distinct().all()       
        data = [{'Ticket': row[0], 'User': row[1], 'Time': row[2], 'Show': row[3], 'Venue': row[4], 'Place': row[5],'City': row[6], 'Price': row[7], 'Language': row[8]} for row in data]
        

        with open(r"templates/monthly_report_mail.html") as file:
            temp = Template(file.read())
        
        u = {
            "UserName": UserName,
            "Year": year,
            "Month": month
        }
        message = temp.render(user=u)
        sub = f"[MONTHLY REPORT] FilmsTicketForYou"
        if len(data)!=0:
            create_pdf_report("templates/monthly_report_pdf.html",data)
            file = str(data[0]['User'])+ ".pdf"
            send_email(to_address=user.Email, subject=sub, message=message, content="html", attachment_file=file)
            
    os.remove(file)
    
    return {"msg": "monthly_report Complete"}


@celery_app.task()
def venue_export(VenueID, user):  #exporting csv file with a mail on a request
        data = []
        show = Show.query.filter_by(VenueID=VenueID).all()
        for s in show:
            booked_tickets_count = Ticket.query.filter_by(ShowID=s.ShowID, Booked=1).count()
            not_booked_tickets_count = Ticket.query.filter_by(ShowID=s.ShowID, Booked=0).count()
            d = {
                "ShowID": s.ShowID,
                "ShowName": s.ShowName,
                "ShowRating": s.ShowRating,
                "No. Booked Tickets": booked_tickets_count,
                "No. Unbooked Tickets": not_booked_tickets_count
            }
            data.append(d)

        file_path = str(VenueID) + ".csv"
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file, delimiter=',')

            writer.writerow(["ShowID", "ShowName", "ShowRating", "No. Booked Tickets", "No. Unbooked Tickets"])  # Write header row (column names)

            for row in data:
                writer.writerow([row["ShowID"], row["ShowName"], row["ShowRating"], row["No. Booked Tickets"], row["No. Unbooked Tickets"]])

        with open(r"templates/venue_export_mail.html") as file:
            temp = Template(file.read())

        message = temp.render(user=user)
        sub = f"[VENUE DETAILS] Films-Ticket-ForYou"
        file_path = str(VenueID) + ".csv"
        send_email(to_address=user["Email"], subject=sub, message=message, content="html", attachment_file=file_path)

        return {"msg": "venue_export Complete"}


@celery_app.task()
def download_ticket(ShowID, selectedtickets, user):  #this is additional feature when user book tickets the tickets will be sent to teir mail in a pdf format
    show = Show.query.filter_by(ShowID=ShowID).first()
    venue = Venue.query.filter_by(VenueID=show.VenueID).first()
    u = Login.query.filter_by(UserName = user).first()
    s ={"User": u.UserName,
        "ShowName":show.ShowName,
          "ShowTime":show.ShowTime,
          "ShowLanguage":show.ShowLanguage,
          "ShowPrice": show.ShowPrice}
    v ={"CityName":venue.CityName,
        "VenuePlace": venue.VenuePlace,
        "VenueName":venue.VenueName}
    t = {"tickets": selectedtickets}
    data = [s,v,t]


    with open(r"templates/download_ticket_mail.html") as file:
        temp = Template(file.read())

        message = temp.render(user=user)
        sub = f"[TICKETS BOOKED] Films-Ticket-ForYou"
        create_pdf_report("templates/download_ticket_pdf.html",data)
        file = str(user)+"_booked_tickets.pdf"
        send_email(to_address=u.Email, subject=sub, message=message, content="html", attachment_file=file)
    
    os.remove(file)

    return {"msg": "download_ticket Complete"}

def format_report(template_file, data={}): #this function is used in above backend jobs for formating mail templates
    with open(template_file) as file:
        template = Template(file.read())
        return template.render(data=data)
    
def create_pdf_report(template, data): #this function is used for creating pdf reports
    template = template
    message = format_report(template, data=data)
    html = HTML(string=message)
    if len(data[0]) == 5:
        a = data[0]["User"]
        file_name = str(a) + "_booked_tickets.pdf"
    else:
        a = data[0]["User"]
        file_name = str(a) + ".pdf"
    print(file_name)
    return  html.write_pdf(target=file_name)


#--------------------------- Resources -----------------------------

api.add_resource(CityApi,'/city/<string:CityName>', '/city/update/<string:CityName>',
                 '/city/delete/<string:CityName>', '/city/add/<string:CityName>')
api.add_resource(VenueApi, '/venue/<string:VenueID>', '/venue/update/<string:VenueID>',
                 '/venue/delete/<string:VenueID>', '/venue/add/<string:VenueID>')
api.add_resource(ShowApi, '/show/<string:ShowID>', '/show/update/<string:ShowID>',
                 '/show/delete/<string:ShowID>', '/show/add/<string:ShowID>')
api.add_resource(Tickets, '/ticket/<string:ShowID>')
api.add_resource(Cities, '/city')
api.add_resource(Venues,'/venues/<string:CityName>')
api.add_resource(Shows,'/shows/<string:VenueID>')
api.add_resource(IndexApi,'/<string:CityName>')
api.add_resource(UserSignupApi,'/signup')
api.add_resource(UserLoginApi,'/login/<string:UserName>/<string:Password>')
api.add_resource(AdminLoginApi,'/login/<string:UserName>/<string:Password>/<int:Admin>')
api.add_resource(UserLogoutApi,'/logout')
api.add_resource(Booked,'/booked')
api.add_resource(Rating,'/rating/<string:Rating>')
api.add_resource(SearchDetails,'/searchdetails', '/search')

if __name__ == '__main__':
    app.run(debug=True)
