#Bashir Kadri
#101273518
#March 17, 2026
#COMP 4107 - Group 39

from flask import Flask, request, jsonify
from flask_cors import CORS
import helpers

app = Flask(__name__)
CORS(app)
@app.route("/receiver", methods = ["POST"])

def receiver():
    data = request.json

    print(data)

    # blueFace = data["x+"]
    # greenFace = data["x-"]
    # whiteFace = data["y+"]
    # yellowFace = data["y-"]
    # redFace = data["z+"]
    # orangeFace = data["z-"]

    # print("BLUE")
    # helpers.helper(blueFace)

    # print("GREEN")
    # helpers.helper(greenFace)

    # print("WHITE")
    # helpers.helper(whiteFace)

    # print("YELLOW")
    # helpers.helper(yellowFace)

    # print("RED")
    # helpers.helper(redFace)

    # print("ORANGE")
    # helpers.helper(orangeFace)

    return jsonify({"Status" : "Successfully Received Message"})

if __name__=="__main__":
    app.run(host = "localhost", port = 8000)