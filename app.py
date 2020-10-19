from flask import Flask, request, jsonify
import json
from lib.dataHandler import DataHandler
from lib.helpers import Helpers

# Init app
app = Flask(__name__)
_data = DataHandler()
_helpers = Helpers()

@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def home():
    res = { 'message' : 'Welcome to Home Page' }
    return res

@app.route('/users', methods=['POST'])
def create_user():
    firstName = str(request.json['firstName'])
    lastName = str(request.json['lastName'])
    email = str(request.json['email'])
    phone = str(request.json['phone'])
    password = str(request.json['password'])

    firstName = firstName.strip() if len(firstName.strip()) > 0 else False
    lastName = lastName.strip() if len(lastName.strip()) > 0 else False
    email = email.strip() if len(email.strip()) > 0 else False
    phone = phone.strip() if len(phone.strip()) == 10 else False
    password = password.strip() if len(password) > 0 else False

    if not (firstName and lastName and email and phone and password):
        return jsonify({ 'message' : 'Authentication Failed!'})

    userObject = {
        'firstName' : firstName,
        'lastName' : lastName,
        'email' : email,
        'phone' : phone,
        'password' : _helpers.hash_str(password)
    }

    res = _data.create('users', phone, json.dumps(userObject))
    if not res:
        return jsonify({ 'message' : 'User Already Exists!' })
    return jsonify({ 'message' : 'User Registered Successfully!' })

@app.route('/users', methods=['GET'])
def get_user():

    phone = str(request.args.get('phone'))
    
    # Validation
    phone = phone if len(phone) == 10 else False
    if not phone:
        return jsonify({ 'message' : 'Authentication Failed!'})

    userData = _data.read('users', phone)
    if not userData:
        return jsonify({ 'message' : 'User Not Found!' })
    result = json.loads(userData)
    del(result['password'])
    return result

# Run the serve
if __name__ == '__main__':
    app.run(debug=True)