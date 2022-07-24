# Traffic Capture Application

The goal of this Python3 project is to implement and develop an application to capture traffic. This is a light-weight web application with functionalities like:
- user login
- session management
- application integration with database to create, update and delete entries
- show the summary of the relevant user

I have used SQLite as the database and designed database, tables to hold user information, session management and vehicle details.

*** NOTE: Please make sure the python version is 3.8.3 and SQLite is installed on your local. This application is dependent on both of these packages.

## Initial Database Setup

Please follow the below instructions to run the script setup_database.py in this repo.

Command to run: python3 setup_database.py

This python script will create the intial_databse.db and set up all the tables: user_details, session_details and traffic_details which are necessary for the application script server.py.

The "initial_database.db" file has been provided in the zip file, so it is not necessary to run this script unless there is a problem with provided DB file.

## Running this application

Command to run: python3 server.py

To start the application run the server.py using the above command example. 

If you have visual studio code available in your local, running the application using visual studio code is an easier way. Open this folder into your visual studio code and run it.

Application URL: http://127.0.0.1:8081






Programming Language: Python3