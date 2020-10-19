from flask import Flask, request, jsonify

# Init app
app = Flask(__name__)

# Run the serve
if __name__ == '__main__':
    app.run(debug=True)