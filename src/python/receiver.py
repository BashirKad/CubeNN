#Bashir Kadri
#101273518
#March 17, 2026
#COMP 4107 - Group 39

from flask import Flask, request, jsonify
from flask_cors import CORS
from multiprocessing import Process
import helpers
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
import time
import colorsys
import math
from collections import defaultdict


COORD_LIST = [(1200, 380), (1320, 440), (1430, 500), (1090, 440), (1320, 580), (970, 500), (1090, 580), (1200, 650),
              (920, 620), (1030, 680), (1140, 750), (920, 740), (1140, 890), (920, 870), (1030, 940), (1140, 1010),
              (1260, 750), (1380, 680), (1490, 620), (1260, 890), (1490, 740), (1260, 1010), (1380, 940), (1490, 870),
              (1445, 562), (1330, 495), (1217, 432), (1444, 693), (1219, 563), (1444, 820), (1330, 756), (1290, 650),
              (1185, 433), (1069, 495), (955, 561), (1183, 561), (953, 693), (1179, 692), (1076, 745), (965, 805),
              (1200, 760), (1315, 830), (1425, 900), (1090, 830), (1315, 970), (975, 900), (1090, 970), (1200, 1040)]

app = Flask(__name__)
CORS(app)
@app.route("/receiver", methods = ["POST"])

def receiver():
    data = request.json

    print("Allo")
    print(data)

    return jsonify({"Status" : "Successfully Received Message"})

def runServer():
    app.run(port = 5000)

def bootup(sizeID):
    driver = webdriver.Chrome()
    driver.get("https://bashirkad.github.io/CubeNN/")

    time.sleep(1)
    #get rid of pop-up
    driver.find_element(By.TAG_NAME, "body").click()
    driver.switch_to.active_element.send_keys(Keys.ESCAPE)

    #select 3x3 for this project (sizeID)
    button = driver.find_element(By.ID, sizeID)
    button.click()

    #double click 
    time.sleep(4)
    driver.find_element(By.TAG_NAME, "html").click()
    driver.find_element(By.TAG_NAME, "html").click()
    
    time.sleep(5) #provide time for scramble to happen

    return driver

def colourClass(pix):
    r, g, b = [x / 255 for x in pix]
    h, s, v = colorsys.rgb_to_hsv(r, g, b) #RGB -> HSV

    h = h * 360

    #white and grey closest colours, differentiate those first by value (brightness) (i hecking love coloru theory)
    if s < 0.2:
        if v >= 0.7:
            return "white"
        else:
            return "locked"

    if h < 15 or h >= 345:
        return "red"
    elif h < 45:
        return "orange"
    elif h < 70:
        return "yellow"
    elif h < 170:
        return "green"
    elif h < 260:
        return "blue"
    else:
        return "locked" #just in case

class qlCube:

    ALPHA = 0.1
    GAMMA = 0.9

    def __init__(self, trials):

        self.actionQValues = defaultdict(float)
        self.actions = defaultdict(set)

        #set up q-values 
        for trial in trials:
            for state, action in trial:
                if action is None:
                    continue

                state = tuple(state)

                self.actions[state] = self.validActions(state)
                self.actionQvalues[(state, action)] = self.reward()
        
        epochs = 50
        threshold = 1e-5

        for epoch in range(epochs):
            delta = 0.0

            for trial in trials:
                for i in range(len(trial) - 1):
                    curState, action = trial[i]
                    nextState, _ = trial[i + 1]

                    curState = tuple(curState)
                    nextState = tuple(nextState)

                    if self.isTerminal(curState):
                        continue

                    self.initializeQVal(curState, action)

                    currentQ = self.actionQvalues[(curState, action)]
                    newQ = self.calculateQ(curState, action, nextState)

                    curDelta = abs(newQ - currentQ)
                    delta = max(delta, curDelta)

                    self.actionQvalues[(curState, action)] = newQ

            if delta < threshold:
                break

    def qvalue(self, state, action):
        # state = tuple(state)

        if self.isTerminal(state):
            return self.reward()

        return self.actionQvalues[(state, action)]
    
    def policy(self, state):
        # state = tuple(state)

        if self.isTerminal(state):
            return None

        maxAction = None
        maxQ = -math.inf

        for action in self.validActions(state):
            q = self.actionQvalues[(state, action)]
            if q > maxQ:
                maxQ = q
                maxAction = action

        return maxAction
    
    def policy(self, state):
        # state = tuple(state)

        if self.isTerminal(state):
            return None

        maxAction = None
        maxQ = -math.inf

        for action in self.validActions(state):
            q = self.actionQvalues[(state, action)]
            if q > maxQ:
                maxQ = q
                maxAction = action

        return maxAction

    def reward():
        #start app to get input from server itself
        flask_process = Process(target = runServer)
        flask_process.start()




        #terminate to not mess with anything
        flask_process.terminate()
        flask_process.join()

        solvingScore = 3
        return solvingScore
    
    def isTerminal():
        return False
    
    def validActions():

        return set(range(12)) #6 clockwise moves, 6 c-clockwise moves
    
    def initializeQVal(self, state, action):
        if (state, action) not in self.actionQvalues:
            self.actionQvalues[(state, action)] = self.reward()

    def applyMove(state, action, actions):

        clockwise = True
        move = ""

        if action > 5:
            clockwise = False

        match action:
            case 0, 6:
                move = "U"
            case 1, 7:
                move = "D"
            case 2, 8:
                move = "L"
            case 3, 9:
                move = "R"
            case 4, 10:
                move = "F"
            case 5, 11:
                move = "B"

        if clockwise:
            actions.send_keys(move).perform()
        else:
            actions.key_down(Keys.SHIFT) \
                .send_keys(move) \
                .key_up(Keys.SHIFT) \
                .perform()
        



        



if __name__=="__main__":
    driver = bootup("solobutton333")

    #start app to get input from server itself
    flask_process = Process(target = runServer)
    flask_process.start()

    #terminate to not mess with anything
    flask_process.terminate()
    flask_process.join()

    inputs = []

    while (True):
        driver.save_screenshot("cube.png")
        time.sleep(0.1)
        image = Image.open("cube.png")
        inputs.clear()

        for coordX, coordY in COORD_LIST:
            pixel = image.getpixel((coordX, coordY))

            # print(f"Pixel at ({coordX}, {coordY}) = {pixel}")
            # print(colourClass(pixel))
            inputs.append(colourClass(pixel)) #make a list of all pieces as per their colour in order (yes locked is a colour, dont think too hard about it)
        print(inputs)

        # model = qlCube([])

        input("")
