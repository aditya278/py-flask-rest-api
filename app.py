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
        return jsonify({ 'message' : 'Authentication Failed!'}), 400

    userObject = {
        'firstName' : firstName,
        'lastName' : lastName,
        'email' : email,
        'phone' : phone,
        'password' : _helpers.hash_str(password)
    }

    res = _data.create('users', phone, json.dumps(userObject))
    if not res:
        return jsonify({ 'message' : 'User Already Exists!' }), 400
    return jsonify({ 'message' : 'User Registered Successfully!' }), 201

@app.route('/users', methods=['GET'])
def get_user():

    phone = str(request.args.get('phone'))
    
    # Validation
    phone = phone if len(phone) == 10 else False
    if not phone:
        return jsonify({ 'message' : 'Authentication Failed!'})

    userData = _data.read('users', phone)
    if not userData:
        return jsonify({ 'message' : 'User Not Found!' }), 400
    result = json.loads(userData)
    del(result['password'])
    return result, 200

@app.route('/users', methods=['PUT'])
def update_user():
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

    if not (phone and (firstName or lastName or email or password)):
        return jsonify({ 'message' : 'Authentication Failed!'}), 400

    # First: Read the User's Data
    userData = _data.read('users', phone)
    if not userData:
        return jsonify({ 'message' : 'User Does not Exists!' }), 400
    userObject = json.loads(userData)

    userObject['firstName'] = firstName if firstName else userObject['firstName']
    userObject['lastName'] = lastName if lastName else userObject['lastName']
    userObject['email'] = email if email else userObject['email']
    userObject['password'] = _helpers.hash_str(password) if password else userObject['password']

    # Second: Update the File
    res = _data.update('users', phone, json.dumps(userObject))
    if not res:
        return jsonify({ 'message' : 'Server Error. Try Later.'}), 500
    return jsonify({ 'message' : 'User Updated Successfully!' }), 202

@app.route('/users', methods=['DELETE'])
def delete_user():
    phone = str(request.args.get('phone'))

    phone = phone.strip() if len(phone.strip()) == 10 else False

    if not (phone):
        return jsonify({ 'message' : 'Authentication Failed!'}), 400

    res = _data.delete('users', phone)
    if not res:
        return jsonify({ 'message' : 'User Does not Exists.'}), 400
    return jsonify({ 'message' : 'User Deleted Successfully!' }), 202

# Run the serve
if __name__ == '__main__':
    app.run(debug=True, port=4000)