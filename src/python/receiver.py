#Bashir Kadri
#101273518
#March 17, 2026
#COMP 4107 - Group 39

from flask import Flask, request, jsonify
from flask_cors import CORS
import helpers
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
import time

app = Flask(__name__)
CORS(app)
@app.route("/receiver", methods = ["POST"])

def receiver():
    data = request.json

    print(data)

    return jsonify({"Status" : "Successfully Received Message"})

def bootup(sizeID):
    driver = webdriver.Chrome()
    driver.get("https://bashirkad.github.io/CubeNN/")

    time.sleep(1)
    #get rid of pop-up
    driver.find_element(By.TAG_NAME, "body").click()
    driver.switch_to.active_element.send_keys(Keys.ESCAPE)

    #select 3x3 for this project
    button = driver.find_element(By.ID, sizeID)
    button.click()

    #double click 
    time.sleep(0.3)
    driver.find_element(By.TAG_NAME, "body").click()
    driver.find_element(By.TAG_NAME, "body").click()
    
    time.sleep(5) #provide time for scramble to happen

    driver.save_screenshot("cube.png")
    time.sleep(0.1)
    image = Image.open("cube.png")

    coordList = [(1200, 380), (1320, 440), (1430, 500)]

    for coordX, coordY in coordList:
        pixel = image.getpixel((coordX, coordY))

        print(f"Pixel at ({coordX}, {coordY}) = {pixel}")

    input("")
    

if __name__=="__main__":
    bootup("solobutton333")
    app.run(host = "localhost", port = 8000)