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

    blueFace = data["x+"]
    greenFace = data["x-"]
    whiteFace = data["y+"]
    yellowFace = data["y-"]
    redFace = data["z+"]
    orangeFace = data["z-"]

    print(type(blueFace))
    print(type(blueFace[0]))

    helper(blueFace)
    helper(greenFace)
    helper(whiteFace)
    helper(yellowFace)
    helper(redFace)
    helper(orangeFace)

    return jsonify({"Status" : "Successfully Received Message"})

if __name__=="__main__":
    app.run(host = "localhost", port = 8000)

def helper(arr):
    for i in range(9):
        if (not arr[i].locked):
            print(arr[i].color)
        else:
            print("locked")