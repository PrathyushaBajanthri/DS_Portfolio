#!/usr/bin/env python

# This is a simple web server for a traffic counting application.
# It's your job to extend it by adding the backend functionality to support
# recording the traffic in a SQL database. You will also need to support
# some predefined users and access/session control. You should only
# need to extend this file. The client side code (html, javascript and css)
# is complete and does not require editing or detailed understanding.

# import the various libraries needed
import http.cookies as Cookie # some cookie handling support
from http.server import BaseHTTPRequestHandler, HTTPServer # the heavy lifting of the web server
import urllib # some url parsing support
import base64 # some encoding support
import hashlib
import binascii
from random import randint
from datetime import datetime
from setup_database import access_database
from setup_database import access_database_with_result

def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

def random_n_digits(n):
    """Provides n digit random number based on the value of n"""
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

# This function builds a refill action that allows part of the
# currently loaded page to be replaced.
def build_response_refill(where, what):
    text = "<action>\n"
    text += "<type>refill</type>\n"
    text += "<where>"+where+"</where>\n"
    m = base64.b64encode(bytes(what, 'ascii'))
    text += "<what>"+str(m, 'ascii')+"</what>\n"
    text += "</action>\n"
    return text


# This function builds the page redirection action
# It indicates which page the client should fetch.
# If this action is used, only one instance of it should
# contained in the response and there should be no refill action.
def build_response_redirect(where):
    text = "<action>\n"
    text += "<type>redirect</type>\n"
    text += "<where>"+where+"</where>\n"
    text += "</action>\n"
    return text

## Decide if the combination of user and magic is valid
def handle_validate(iuser, imagic):
    #check if the user and the respective magic exists in the table
    if access_database_with_result("SELECT * FROM session_details where user='%s' and magic='%s'"%(iuser, imagic)):
        return True
    if (iuser == 'test') and (imagic == '1234567890'):
        return True
    else:
        return False

## remove the combination of user and magic from the data base, ending the login
def handle_delete_session(iuser, imagic):
    access_database("DELETE FROM session_details where user='%s' AND magic ='%s'"%(iuser, imagic))

## A user has supplied a username (parameters['usernameinput'][0])
## and password (parameters['passwordinput'][0]) check if these are
## valid and if so, create a suitable session record in the database
## with a random magic identifier that is returned.
## Return the username, magic identifier and the response action set.
def handle_login_request(iuser, imagic, parameters):
    if handle_validate(iuser, imagic):
        # the user is already logged in, so end the existing session.
        handle_delete_session(iuser, imagic)

    if 'usernameinput' in parameters and 'passwordinput' in parameters:
        user = parameters['usernameinput'][0]
        password = parameters['passwordinput'][0]
        hashed_stored_password = access_database_with_result("SELECT password FROM user_details where user='%s'"%(user,))[0][0].strip().replace("'", "")
        text = "<response>\n"
        if verify_password(hashed_stored_password, password):
            text += build_response_refill('message', 'Valid Credentials, Logging in')
            text += build_response_redirect('/page.html')
            time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            magic = str(random_n_digits(10))
            access_database("INSERT INTO session_details(user, magic, session_start, session_end) VALUES('%s','%s','%s','%s')"%(user, magic, time_now, ''))
        elif parameters['usernameinput'][0] == 'test': ## The user is valid
            text += build_response_refill('message', 'Valid Credentials, Logging in')
            text += build_response_redirect('/page.html')
            time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            access_database("INSERT INTO session_details(user, magic, session_start, session_end) VALUES('%s','%s','%s','%s')"%('user', 1234567890, time_now, ''))
        else: ## The user is not valid
            text += build_response_refill('message', 'Invalid password')
            user = '!'
            magic = ''
        text += "</response>\n"
    else:
        text = "<response>\n"
        text += build_response_refill('message', 'Invalid username/password')
        user = '!'
        magic = ''
        text += "</response>\n"
    return [user, magic, text]

## The user has requested a vehicle be added to the count
## parameters['locationinput'][0] the location to be recorded
## parameters['occupancyinput'][0] the occupant count to be recorded
## parameters['typeinput'][0] the type to be recorded
## Return the username, magic identifier (these can be empty  strings) and the response action set.
def handle_add_request(iuser, imagic, parameters):
    text = "<response>\n"
    if handle_validate(iuser, imagic) != True:
        #Invalid sessions redirect to login
        text += build_response_redirect('/index.html')
        user = ''
        magic = ''
    else: ## a valid session so process the addition of the entry.
        user = iuser
        magic = imagic
        if 'locationinput' in parameters:
            location = parameters['locationinput'][0]
            if location.isspace():
                text += build_response_refill('message', 'Must Specify Location.')
                text += build_response_refill('total', '0')
            else:
                occupancy = parameters['occupancyinput'][0]
                vtype = parameters['typeinput'][0]
                time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                access_database("INSERT INTO traffic_details VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')"%(user, magic, location, vtype, occupancy, time_now, '', ''))
                entries_made = access_database_with_result("SELECT COUNT(type) FROM traffic_details WHERE user='%s' AND magic='%s'"%(user, magic))[0][0]
                text += build_response_refill('message', 'Entry added.')
                text += build_response_refill('total', str(entries_made))
        else:
            text += build_response_refill('message', 'Missing Location.')
            text += build_response_refill('total', '0')
    text += "</response>\n"
    return [user, magic, text]

## The user has requested a vehicle be removed from the count
## This is intended to allow counters to correct errors.
## parameters['locationinput'][0] the location to be recorded
## parameters['occupancyinput'][0] the occupant count to be recorded
## parameters['typeinput'][0] the type to be recorded
## Return the username, magic identifier (these can be empty  strings) and the response action set.
def handle_undo_request(iuser, imagic, parameters):
    text = "<response>\n"
    if handle_validate(iuser, imagic) != True:
        #Invalid sessions redirect to login
        text += build_response_redirect('/index.html')
        user = ''
        magic = ''
    else: ## a valid session so process the recording of the entry.
        user = iuser
        magic = imagic
        if 'typeinput' in parameters and 'occupancyinput' in parameters and 'locationinput' in parameters:
            vtype = parameters['typeinput'][0]
            occupancy = parameters['occupancyinput'][0]
            location = parameters['locationinput'][0]
            if access_database_with_result("SELECT * from traffic_details where type='%s' AND user='%s' AND magic='%s' AND location='%s' AND occupancy='%s'"%(vtype, user, magic, location, occupancy)):
                time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                access_database("UPDATE traffic_details SET traffic_undo='%s',undo_flag = '1' WHERE type='%s' AND user='%s' AND magic='%s'"%(time_now, vtype, user, magic))
                entries_undone = access_database_with_result("SELECT COUNT(type) FROM traffic_details WHERE user='%s' AND magic='%s' AND undo_flag='1'"%(user, magic))[0][0]
                text += build_response_refill('message', 'Entry Un-done.')
                text += build_response_refill('total', str(entries_undone))
            else:
                text += build_response_refill('message', 'Unable to locate Vehicle: ' + str(vtype) + " with occupancy " + str(occupancy) + " at location: " + str(location) + " for the current session")
        else:
            text += build_response_refill('message', 'Please provide correct details of location, vehicle type and occupancy')
            text += build_response_refill('total', '0')
    text += "</response>\n"
    return [user, magic, text]

# This code handles the selection of the back button on the record form (page.html)
# You will only need to modify this code if you make changes elsewhere that break its behaviour
def handle_back_request(iuser, imagic, parameters):
    text = "<response>\n"
    if handle_validate(iuser, imagic) != True:
        text += build_response_redirect('/index.html')
    else:
        text += build_response_redirect('/summary.html')
    text += "</response>\n"
    user = ''
    magic = ''
    return [user, magic, text]

## This code handles the selection of the logout button on the summary page (summary.html)
## You will need to ensure the end of the session is recorded in the database
## And that the session magic is revoked.
def handle_logout_request(iuser, imagic, parameters):
    user = iuser
    magic = imagic
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    access_database("UPDATE session_details SET magic='%s',session_end='%s' WHERE user='%s'"%('', time_now, user))
    text = "<response>\n"
    text += build_response_redirect('/index.html')
    text += "</response>\n"
    return [user, magic, text]

## This code handles a request for update to the session summary values.
## You will need to extract this information from the database.
def handle_summary_request(iuser, imagic, parameters):
    print(parameters)
    text = "<response>\n"
    if handle_validate(iuser, imagic) != True:
        text += build_response_redirect('/index.html')
    else:
        user = iuser
        magic = imagic
        vehicle_types = ['car', 'bus', 'bicycle', 'motorbike', 'van', 'truck', 'taxi', 'other']
        summary_dict = {}
        for vehicle in vehicle_types:
            temp_sum = access_database_with_result("SELECT COUNT(type) FROM traffic_details WHERE type='%s' AND user='%s' AND magic='%s' AND undo_flag!='1'"%(vehicle, user, magic))[0][0]
            summary_dict[vehicle] = temp_sum
            temp_sum = 0
        text += build_response_refill('sum_car', str(summary_dict['car']))
        text += build_response_refill('sum_taxi', str(summary_dict['taxi']))
        text += build_response_refill('sum_bus', str(summary_dict['bus']))
        text += build_response_refill('sum_motorbike', str(summary_dict['motorbike']))
        text += build_response_refill('sum_bicycle', str(summary_dict['bicycle']))
        text += build_response_refill('sum_van', str(summary_dict['van']))
        text += build_response_refill('sum_truck', str(summary_dict['truck']))
        text += build_response_refill('sum_other', str(summary_dict['other']))
        text += build_response_refill('message', 'Traffic Summary')
        text += build_response_refill('total', str(sum(summary_dict.values())))
        text += "</response>\n"
    return [user, magic, text]


# HTTPRequestHandler class
class myHTTPServer_RequestHandler(BaseHTTPRequestHandler):

    # GET This function responds to GET requests to the web server.
    def do_GET(self):

        # The set_cookies function adds/updates two cookies returned with a webpage.
        # These identify the user who is logged in. The first parameter identifies the user
        # and the second should be used to verify the login session.
        def set_cookies(x, user, magic):
            ucookie = Cookie.SimpleCookie()
            ucookie['u_cookie'] = user
            x.send_header("Set-Cookie", ucookie.output(header='', sep=''))
            mcookie = Cookie.SimpleCookie()
            mcookie['m_cookie'] = magic
            x.send_header("Set-Cookie", mcookie.output(header='', sep=''))

        # The get_cookies function returns the values of the user and magic cookies if they exist
        # it returns empty strings if they do not.
        def get_cookies(source):
            rcookies = Cookie.SimpleCookie(source.headers.get('Cookie'))
            user = ''
            magic = ''
            for keyc, valuec in rcookies.items():
                if keyc == 'u_cookie':
                    user = valuec.value
                if keyc == 'm_cookie':
                    magic = valuec.value
            return [user, magic]

        # Fetch the cookies that arrived with the GET request
        # The identify the user session.
        user_magic = get_cookies(self)

        print(user_magic)

        # Parse the GET request to identify the file requested and the GET parameters
        parsed_path = urllib.parse.urlparse(self.path)

        # Decided what to do based on the file requested.

        # Return a CSS (Cascading Style Sheet) file.
        # These tell the web client how the page should appear.
        if self.path.startswith('/css'):
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            with open('.'+self.path, 'rb') as file:
                self.wfile.write(file.read())
            file.close()

        # Return a Javascript file.
        # These tell contain code that the web client can execute.
        if self.path.startswith('/js'):
            self.send_response(200)
            self.send_header('Content-type', 'text/js')
            self.end_headers()
            with open('.'+self.path, 'rb') as file:
                self.wfile.write(file.read())
            file.close()

        # A special case of '/' means return the index.html (homepage)
        # of a website
        elif parsed_path.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('./index.html', 'rb') as file:
                self.wfile.write(file.read())
            file.close()

        # Return html pages.
        elif parsed_path.path.endswith('.html'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('.'+parsed_path.path, 'rb') as file:
                self.wfile.write(file.read())
            file.close()

        # The special file 'action' is not a real file, it indicates an action
        # we wish the server to execute.
        elif parsed_path.path == '/action':
            self.send_response(200) #respond that this is a valid page request
            # extract the parameters from the GET request.
            # These are passed to the handlers.
            parameters = urllib.parse.parse_qs(parsed_path.query)

            if 'command' in parameters:
                # check if one of the parameters was 'command'
                # If it is, identify which command and call the appropriate handler function.
                if parameters['command'][0] == 'login':
                    [user, magic, text] = handle_login_request(user_magic[0], user_magic[1], parameters)
                    #The result to a login attempt will be to set
                    #the cookies to identify the session.
                    set_cookies(self, user, magic)
                elif parameters['command'][0] == 'add':
                    [user, magic, text] = handle_add_request(user_magic[0], user_magic[1], parameters)
                    if user == '!': # Check if we've been tasked with discarding the cookies.
                        set_cookies(self, '', '')
                elif parameters['command'][0] == 'undo':
                    [user, magic, text] = handle_undo_request(user_magic[0], user_magic[1], parameters)
                    if user == '!': # Check if we've been tasked with discarding the cookies.
                        set_cookies(self, '', '')
                elif parameters['command'][0] == 'back':
                    [user, magic, text] = handle_back_request(user_magic[0], user_magic[1], parameters)
                    if user == '!': # Check if we've been tasked with discarding the cookies.
                        set_cookies(self, '', '')
                elif parameters['command'][0] == 'summary':
                    [user, magic, text] = handle_summary_request(user_magic[0], user_magic[1], parameters)
                    if user == '!': # Check if we've been tasked with discarding the cookies.
                        set_cookies(self, '', '')
                elif parameters['command'][0] == 'logout':
                    [user, magic, text] = handle_logout_request(user_magic[0], user_magic[1], parameters)
                    if user == '!': # Check if we've been tasked with discarding the cookies.
                        set_cookies(self, '', '')
                else:
                    # The command was not recognised, report that to the user.
                    text = "<response>\n"
                    text += build_response_refill('message', 'Internal Error: Command not recognised.')
                    text += "</response>\n"

            else:
                # There was no command present, report that to the user.
                text = "<response>\n"
                text += build_response_refill('message', 'Internal Error: Command not found.')
                text += "</response>\n"
            self.send_header('Content-type', 'application/xml')
            self.end_headers()
            self.wfile.write(bytes(text, 'utf-8'))
        else:
            # A file that does n't fit one of the patterns above was requested.
            self.send_response(404)
            self.end_headers()
        return

# This is the entry point function to this code.
def run():
    """ Main function to start the application """
    print('starting server...')
    ## You can add any extra start up code here
    # Server settings
    # Choose port 8081 over port 80, which is normally used for a http server
    server_address = ('127.0.0.1', 8081)
    httpd = HTTPServer(server_address, myHTTPServer_RequestHandler)
    print('running server...')
    httpd.serve_forever() # This function will not return till the server is aborted.

run()
