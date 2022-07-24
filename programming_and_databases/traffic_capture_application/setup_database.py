import sqlite3
import hashlib, os, binascii

dbfile = "initial_database.db"

def access_database(query, *args):
    data = ()
    if len(args) != 0:
        data = args[0]
    connect = sqlite3.connect(dbfile)
    cursor = connect.cursor()
    cursor.execute(query, data)
    connect.commit()
    connect.close()
    
def access_database_with_result(query, *args):
    data = ()
    if len(args) != 0:
        data = args[0]
    connect = sqlite3.connect(dbfile)
    cursor = connect.cursor()
    rows = cursor.execute(query, data).fetchall()
    connect.commit()
    connect.close()
    return rows

def setup_tables(droptables = 'False'):
    if droptables == 'True':
        access_database("DROP TABLE IF EXISTS user_details")
        access_database("DROP TABLE IF EXISTS session_details")
        access_database("DROP TABLE IF EXISTS traffic_details")
    access_database("CREATE TABLE user_details (user TEXT, password TEXT)")
    access_database("CREATE TABLE session_details (user TEXT, magic INT, session_start DATETIME, session_end DATETIME)")
    access_database("CREATE TABLE traffic_details (user TEXT, magic INT, location TEXT, type TEXT, occupancy INT, traffic_recorded DATETIME, traffic_undo DATETIME, undo_flag INT)")

def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def populate_users():
    for i in range(1,11):
        user = 'test' + str(i)
        pass_string = 'password' + str(i)
        hashed_pass = hash_password(pass_string)
        access_database("INSERT INTO user_details VALUES ('%s','%s')"%(user, hashed_pass))

def setup_database():
    setup_tables('False')
    populate_users()

#setup_database()