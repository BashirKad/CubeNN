#Bashir Kadri
#101273518
#March 17, 2026
#COMP 4107 - Group 39

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
@app.route("/receiver", methods = ["POST"])

def receiver():
    data = request.json
    print(data)
    return jsonify({"Status" : "Successfully Received Message"})

if __name__=="__main__":
    app.run(host = "localhost", port = 8000)