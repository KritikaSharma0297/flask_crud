from flask import Flask, jsonify, request
import mysql.connector 
import jwt
import datetime


# Configuration details to connect to our local database
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Kritika@1997",
    "database": "emp",
    "port": 3306
}

# Connect to database
def get_db_connection():
    connection = mysql.connector.connect(**db_config) # use mysql.conector to connect to our database using the details stored in db_config variable above
    return connection


app = Flask(__name__)

# Secret key to encode and decode JWT
app.config['SECRET_KEY'] = 'MY_KEY'


@app.route('/login', methods=['POST']) 
def login():
    auth = request.json
    if auth: # if auth is not None and has data, then extract username and password
        username = auth['username']
        password = auth['password']
    
    connection = get_db_connection() # Connect to database
    cursor = connection.cursor(dictionary=True)  # Return rows as dictionaries
    cursor.execute(f"SELECT * FROM users where user_name='{username}'") # run sql query
    user = cursor.fetchone() # fetch data from database using above query
    cursor.close()
    connection.close()

    if not user: # if user exists in database (fetched using above query)
        return jsonify({"error": "User does not exist"}), 401 # return 401 error if user with given username doesn't exist in database
    
    if isinstance(user, dict): # if user exists in database and is in dictionary format
        token = jwt.encode({
            'username': user['user_name'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, app.config['SECRET_KEY'], algorithm='HS256') # create JWT using our secret key with expiry of 1 hour
    
    return jsonify({"token": token}) # return the generated token

if __name__ == '__main__':
    app.run() # run the app using Flask
