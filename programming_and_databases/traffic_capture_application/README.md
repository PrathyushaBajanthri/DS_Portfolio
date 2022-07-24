# Traffic Capture Application

The goal of this Python3 project is to implement and develop an application to capture traffic. This is a light-weight web application with functionalities like:
- user login
- password hashing
- session management
- application integration with database to create, update and delete entries
- show the summary of the relevant user

I have used SQLite as the database and designed database, tables to hold user information, session management and vehicle details.

*** NOTE: Please make sure the python version is 3.8.3 and SQLite is installed on your local. This application is dependent on both of these packages.

## Initial Database Setup

Please follow the below instructions to run the script setup_database.py in this repo.

Command to run: `python3 setup_database.py`

This python script will create the intial_databse.db and set up all the tables: `user_details`, `session_details` and `traffic_details` which are necessary for the application script server.py.

The `initial_database.db` file has been provided in the repo, so it is not necessary to run this script unless there is a problem with provided DB file.

## Running this application
To start the application run the `server.py` using the below command example.

Command to run: `python3 server.py`

If you have visual studio code available in your local, running the application using visual studio code is an easier way. Open this folder into your visual studio code and run it.

Application URL: `http://127.0.0.1:8081`

## Database Specifications:
The application uses an SQLite3 database named `initial_database.db` with the below tables:
- user_details:

| column   | user | password |
|----------|------|----------|
| datatype | TEXT | TEXT     |

This table has two columns – user and password both with a data type set to TEXT to store the username and hashed password of the users who access the application.

- session_details:

| column   | user | magic (session_id) | session_start | session_end |
|----------|------|--------------------|---------------|-------------|
| datatype | TEXT | TEXT               | DATETIME      | DATETIME    |

This table has four columns – user, magic (session id), session_start and session_end with data types TEXT, INT, DATETIME and DATETIME, respectively. As the column names suggest themselves this table will hold the details of the current session once a user login to the application. It keeps track of the session id, start and end times of the current session.

- traffic_details:

| column   | user | magic (session_id) | location | type | occupancy | traffic_recorded | traffic_undo | undo_flag |
|----------|------|--------------------|----------|------|-----------|------------------|--------------|-----------|
| datatype | TEXT | TEXT               | TEXT     | TEXT | INT       | DATETIME         | DATETIME     | INT       |

This table has 8 columns to record the details of traffic details of a specific vehicle owned by a specific user. The columns are – user, magic, location, type, occupancy, traffic_recorder, traffic_undo and undo_flag with data types TEXT, INT, TEXT, TEXT, TEXT, DATETIME, DATETIME and INT, respectively. This table holds information about the type of vehicle and the occupancy, the location and the exact time where it was recorded. If the user wanted to undo the vehicle, the columns traffic_undo will be populated with the time when undo operation was performed and undo_flag will be set to ‘1’ so that undone records can be distinguished.

## Functionality of the application:
The functionality of the application like `login`, `logout`, `the addition of records`, `undo of records`, `summary` and `navigation` is handled through several functions in the `server.py` file. A brief description of each function and relevant checks that are being made by the function are given below.

- Login:
The user login is being handled by the function `handle_login_request()` which in turn calls the function `handle_validate()` to make sure if there is an existing session of the user which is trying to login, if so the existing session of the user will be terminated and user will be asked to do a fresh login. If in case the user trying to login does not have any existing session, the application will check will do the following checks in the below sequence:
	- checks if the user has provided both username and password, return a message on login page “Invalid username/password” in case any of these inputs are not provided
	- queries the password for the input username from user_details table and cross verify if it matches with the input password using the function `verify_password()`
	- the user is only allowed to login once the `verify_password()` successfully validates the input password with the password that was stored in the user_details table
	- once the user is logged into the application, a session id – magic will be assigned and recorded in the session_details table along with the start time of the session

- Recording a vehicle: 
This functionality is being handled by the function `handle_add_request()` which also checks if the current session for the user is valid through `handle_validate()` and records the vehicle to `traffic_details` table in steps of the below sequence:
	- checks if the location has been provided by the user in two scenarios:
	- if the location value is NULL
	- if the location value is blank (contains only whitespaces)
returns a message “Missing location” or “Must Specify Location” in case of any of the above scenarios fails.
	- once the checks on the location input are completed, the application will add an entry to `traffic_details` table with all the relevant information
	- for every entry into the table, the total number of entries made in the current session will also be displayed

- Undo record of a vehicle:
The application provides the user with the feasibility to revert the entry that has been made in the current session provided the vehicle type, location and occupancy. The function `handle_undo_request()` handles this functionality to undo the record of a vehicle in the below sequence:
	- checks if the values of location, vehicle type and occupancy are provided. If the values are found to be NULL, it returns a message prompting the user to provide necessary input.
	- If the above check is performed successfully, the function queries the database to check if the table `traffic_details` has the record matching the vehicle type, location and occupancy by the current user in the ongoing session. In case of empty results are found, the user will be displayed an appropriate message
	- Once the two checks mentioned above passed, the record for the vehicle as requested by the user will be undone by setting the value of undo_flag to 1 and the time when the undo operation was performed will be noted in session_undo column

- Summary of current session:
The user will be provided with a summary of the activity that took place as part of the session giving options to either add more traffic or logout from the current session. This is handled by the function `handle_summary_request()`. This function queries the traffic_details table and fetches the count of all the types of vehicles that are recorded in the current session into a dictionary, which is shown as a summary

- Logout:
The user logout is being handled by the function `handle_logout_request()` which records the session ending time to the session_end column, removing the session cooking (magic) from the session_detail table and redirecting the user to the login page
The below measures are taken to prevent errors/malicious input behaviour:
	- A robust login mechanism has been kept in place to make sure the access to the application is done in a controlled manner by implementing the below:
	- Hashed stored password – The passwords of the users are stored in the database in a secured manner by encoding them using hashlib
	- Assigning session id (magic) to the user to make sure the same user does not create a new session
	- Make sure the username and password as a mandatory requirement to perform login request
	- To prevent SQL injection attacks, the application has been made only to use parameterised SQL queries.
	- The session id (magic) of the user will always be monitored by the application so that the user will have access to the records that are created during the current session.


Programming Language: Python3

Database: SQLite3
