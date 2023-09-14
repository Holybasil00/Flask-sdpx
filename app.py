# # make simple flask api with hello world
# # run with: python app.py

# import mysql.connector
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flaskext.mysql import MySQL


load_dotenv()

app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = os.getenv('MYSQL_DB_USER')
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_DB_PASSWORD')
app.config['MYSQL_DATABASE_DB'] = os.getenv('MYSQL_DB_DB')
app.config['MYSQL_DATABASE_HOST'] = os.getenv('MYSQL_DB_HOST')


mysql = MySQL()
mysql.init_app(app)


@app.route('/test')
def hello_world():
    return "test"


@app.route('/users', methods=['GET'])
def getAllUsers():
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM Users")

    row_headers = [x[0] for x in cursor.description]
    myresult = cursor.fetchall()

    json_data = []
    for result in myresult:
        json_data.append(dict(zip(row_headers, result)))
    return jsonify(json_data)


@app.route('/users/<int:id>', methods=['GET'])
def getUsers(id):

    if checkUser(id) == False:
        return {"message": "User not found"}, 404

    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM Users WHERE uid = %s", (id,))
    row_headers = [x[0] for x in cursor.description]
    myresult = cursor.fetchall()
    json_data = []
    for result in myresult:
        json_data.append(dict(zip(row_headers, result)))
    return jsonify(json_data)


@app.route('/users/new', methods=['POST'])
def createUser():
    if (request.method == 'POST'):
        body = request.get_json()
        name = body['name']
        age = body['age']
        cursor = mysql.get_db().cursor()
        cursor.execute(
            "INSERT INTO Users (name, age) VALUES (%s, %s)", (name, age))
        mysql.get_db().commit()
        return {'id': cursor.lastrowid, 'name': name, 'age': age}
    else:
        return "error"


@app.route('/users/<int:id>', methods=['PUT'])
def updateUser(id):
    if (request.method == 'PUT'):
        body = request.get_json()
        name = body.get('name', None)
        age = body.get('age', None)
        cursor = mysql.get_db().cursor()

        if checkUser(id) == False:
            return {"message": "User not found"}, 404

        query = "UPDATE Users SET "
        query_params = []
        if name != None:
            query += "name = %s, "
            query_params.append(name)
        if age != None:
            query += "age = %s, "
            query_params.append(age)

        query = query.strip(", ")
        query += " WHERE uid = %s"
        query_params.append(id)

        cursor.execute(query, query_params)
        mysql.get_db().commit()
        return {"message": "success"}, 200
    else:
        return "error"


@app.route('/users/<int:id>', methods=['DELETE'])
def deleteUser(id):
    if (request.method == 'DELETE'):

        if checkUser(id) == False:
            return {"message": "User not found"}, 404
        try:
            cursor.execute(
                "DELETE FROM Users WHERE uid = %s", (id,))
            mysql.get_db().commit()
            return {'message': "deleted" + str(id)}, 200
        except:
            return {"message": "error"}, 500


def checkUser(id):
    cursor = mysql.get_db().cursor()
    qur_check = "SELECT * FROM Users WHERE uid = %s"
    cursor.execute(qur_check, (id,))
    user = cursor.fetchone()
    return True if user else False


if __name__ == '__main__':
    app.run(debug=True, port=5050)

# from flask import Flask, request, jsonify
# app = Flask(__name__)

# mydb = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="",
#     database="Sdpxdb"
# )


# @app.route('/')
# def hello_world():
#     return 'Hello, World!'


# @app.route('/users')
# def get_users():
#     mydb = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="",
#         database="Sdpxdb"
#     )

#     mycursor = mydb.cursor()

#     mycursor.execute("SELECT * FROM Users")

#     myresult = mycursor.fetchall()

#     return jsonify(myresult)


# @app.route('/users/<int:id>', methods=['GET'])
# def getUsers():
#     print(id)
#     q = request.args.get('id')
#     print(q)
#     if (id == None):
#         return "Please enter id"
#     else:
#         mycursor = mydb.cursor()
#         mycursor.execute("SELECT * FROM Users WHERE id = %s", (id,))
#         row_headers = [x[0] for x in mycursor.description]
#         myresult = mycursor.fetchall()
#         json_data = []
#         for result in myresult:
#             json_data.append(dict(zip(row_headers, result)))
#         return jsonify(json_data)


# if __name__ == '__main__':
#     app.run(debug=True)
