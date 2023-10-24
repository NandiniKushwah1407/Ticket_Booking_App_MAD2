# Ticket_Booking_App_MAD2

# Ticket Booking App : MAD2 Project (Term 2,2023)

Name: Nandini Kushwah
Roll no.: 22f1001148
This is my submission for the final project for the course Modern Application Development II

# Technonlogy used for the Application
 - VueJs single page application build on vue-cli
 - Bootstrap for Styling
 - Flask Apis are used for backend
 - SQlite for database
 - JWT tokenization for authorization
 - Celey and Redis for backend jobs
 - Redis for Caching
 - MailHog for sending mails

 # Features of the Application

 - Seperate User and Admin Login

   **For Admin**

 - CRUD application for cities, venues and shows
 - Dashboard for show's perfornmance
 - Export the csv file for the venue

   **For User**
 - Basic view of a index page with venues and show
 - User can book multiple tickets
 - User can rate movie
 - Search feature for venues and shows
 - Daily reminder for user if not logged in for more than 24hr
 - Send Booked tickets to the mail of the user
 - Monthly report sent through mail on 1st day of the month
 - User can select city in which he/she want to book ticket
 - User can register/SignUp


# Software specifications for the web app 

To run these files we need a IDE(or text editor), python3, WSL or Linux system and a GUI for SQLite3 to see the changes in Database.

## How to use

There are two folders in the project -

1. backend
2. frontend

###### For setting up backend --------------------------------------------------------------------------------------------------------

1. first go to backend directory by running the below command in wsl

#         cd backend

2. make a virtual environment in backend folder

#         virtualenv env

3. write the below command to activate the virtual environment,

#          .\env\Scripts\activate.ps1

4. install redis

#         curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
    
#         echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" |  sudo tee /etc/apt/sources.list.d/redis.list

#         sudo apt-get update

#         sudo apt-get install redis

5. install MailHog 
 
#         sudo apt-get update

#         sudo apt-get upgrade

#         sudo apt-get -y install golang-go

#         sudo apt get install git

#         go install github.com/mailhog/MailHog@latest

6. install weasyprint

#         sudo apt-get install python3-dev python3-pip python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info

#         pip install weasyprint


7. install the requirement.txt file in the env

#         pip install -r requirement.txt

8. run redis server (in backend directory)
    
    run below commands in another terminal one by one

#         sudo service redis-server start

#         redis-cli

9. run celery (in backend directory)

    run below commands in another terminal

#         celery -A api.celery_app worker -l info
       
10. run celery-beat (in backend directory)

#         celery -A api.celery_app beat --max-interval 1 -l info   

11. run MailHog
    
    run below commands in another terminal one by one (Note: Don't open the terminal in IDE, open a seperate WSL terminal from the device)

#         cd go

#         cd bin

#         ./MailHog

12. At last run below command (in backend directory)

#          python3 api.py


# --------------------------------Note: Run all the above commands in WSL----------------------------



###### For setting up frontend -------------------------------------------------------------------------------------------------------

1. first go to frontend directory by running the below command in powershell

#         cd frontend

2. node_modules folder are not there in the frontend folder so run the below command to make the it

#         npm install

   (Note: Above command only work if Vue 3 cli setup is done)

3. run the vue app

#         npm run serve


# Using the App

**SERVERS**

backend :  **locahost:5000**
frontend :  **localhost:8080**
MailHog: **localhost:8025**


**For admin login use the credentials given below:**

username: admin
password: admin@123

**For user you can signup first and then login, if don't want to go this way use below details:**

username: user1
password: user1@123

