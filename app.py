from flask import Flask, request, jsonify
import json
from lib.dataHandler import DataHandler

# Init app
app = Flask(__name__)
_data = DataHandler()

@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def home():
    res = { 'message' : 'Welcome to Home Page' }
    return res

# @app.route('/users', methods=['POST'])
# def create_user():


@app.route('/users', methods=['GET'])
def get_user():

    phone = request.args.get('phone')
    
    # Validation
    phone = phone if type(phone) == 'string' and len(phone) == 10 else False
    if not phone:
        return jsonify({ 'message' : 'Authentication Failed!'})

    userData = _data.read('users', phone)
    if not userData:
        return jsonify({ 'message' : 'User Not Found!' })
    return json.loads(userData)

# Run the serve
if __name__ == '__main__':
    app.run(debug=True)