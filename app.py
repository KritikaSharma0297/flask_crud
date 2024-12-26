from flask import Flask, jsonify, request
from flaskext.mysql import MySQL
from flask_restful import Resource, Api
from flask_httpauth import HTTPBasicAuth

#Create an instance of Flask
app = Flask(__name__)

#Create an instance of MySQL
mysql = MySQL()

#Create an instance of Flask RESTful API
api = Api(app)

# Create an instance of HTTP Basic Auth 
auth = HTTPBasicAuth()

#Set database credentials in config.
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Kritika@1997'
app.config['MYSQL_DATABASE_DB'] = 'emp'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

#Initialize the MySQL extension
mysql.init_app(app)

users = {
    "ENCORA" : "encora",
    }

@auth.get_password
def get_pw(username):
    if username in users: 
        return users[username]
    return None


#Get All Users, or Create a new user
class UserList(Resource):
    def get(self):
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("select * from employee")
            rows = cursor.fetchall()
            return jsonify(rows)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    @auth.login_required
    def post(self):
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            _name = request.form['name']
            _email = request.form['email']
            _phone = request.form['phone']
            insert_user_cmd = """INSERT INTO employee(name, email, phone) 
                                VALUES(%s, %s, %s)"""
            
            cursor.execute(insert_user_cmd, (_name, _email, _phone))
            conn.commit()
            response = jsonify(message='User added successfully.', id=cursor.lastrowid)
            #response.data = cursor.lastrowid
            response.status_code = 200
        except Exception as e:
            print(e)
            response = jsonify('Failed to add user.')         
            response.status_code = 400 
        finally:
            cursor.close()
            conn.close()
            return(response)
            
#Get a user by id, update or delete user
class User(Resource):
    @auth.login_required
    def get(self, id):
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute('select * from employee where id = %s',id)
            rows = cursor.fetchall()
            return jsonify(rows)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    @auth.login_required
    def put(self, id): 
        try: 
            conn = mysql.connect() 
            cursor = conn.cursor() 
            name = request.form['name'] 
            email = request.form['email'] 
            phone = request.form['phone'] 
            update_user_cmd = """UPDATE employee SET name=%s, email=%s, phone=%s WHERE id=%s""" 
            cursor.execute(update_user_cmd, (name, email, phone, id)) 
            conn.commit() 
            response = jsonify('User updated successfully.') 
            response.status_code = 200 
        except Exception as e: 
            print(e) 
            response = jsonify('Failed to update user.') 
            response.status_code = 400 
        finally: 
            cursor.close() 
            conn.close() 
            return (response)    
           
    @auth.login_required
    def delete(self, id):
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute('delete from employee where id = %s',id)
            conn.commit()
            response = jsonify('User deleted successfully.')
            response.status_code = 200
        except Exception as e:
            print(e)

            response = jsonify('Failed to delete user.')         
            response.status_code = 400
        finally:
            cursor.close()
            conn.close()    
            return(response)       

#API resource routes
api.add_resource(UserList, '/users', endpoint='users')
api.add_resource(User, '/user/<int:id>', endpoint='user')

if __name__ == "__main__":
    app.run(debug=True)
