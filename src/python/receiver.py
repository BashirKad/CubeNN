#Bashir Kadri
#101273518
#March 17, 2026
#COMP 4107 - Group 39

from flask import Flask, request, jsonify
from flask_cors import CORS
# from multiprocessing import Process
from threading import Thread

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from PIL import Image
from collections import deque
import time
import colorsys
import random

import numpy 
import torch

#consts & global vars
COORD_LIST = [(1200, 380), (1320, 440), (1430, 500), (1090, 440), (1320, 580), (970, 500), (1090, 580), (1200, 650),
              (920, 620), (1030, 680), (1140, 750), (920, 740), (1140, 890), (920, 870), (1030, 940), (1140, 1010),
              (1260, 750), (1380, 680), (1490, 620), (1260, 890), (1490, 740), (1260, 1010), (1380, 940), (1490, 870),
              (1445, 562), (1330, 495), (1217, 432), (1444, 693), (1219, 563), (1444, 820), (1330, 756), (1290, 650),
              (1185, 433), (1069, 495), (955, 561), (1183, 561), (953, 693), (1179, 692), (1076, 745), (965, 805),
              (1200, 760), (1315, 830), (1425, 900), (1090, 830), (1315, 970), (975, 900), (1090, 970), (1200, 1040)]

COLOR_MAP = {
    "white": 0,
    "yellow": 1,
    "green": 2,
    "blue": 3,
    "red": 4,
    "orange": 5,
    "locked": 6
}

TARGET_SCORE = 54

sharedData = {"solvingScore": 0}

#setting up connection to the website
app = Flask(__name__)
CORS(app)
@app.route("/receiver", methods = ["POST"])

def receiver():
    data = request.json
    sharedData["solvingScore"] = int(data)

    return jsonify({"Status" : "Successfully Received Message"})

def runServer():
    app.run(port = 8000)

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

class cubeNetwork(torch.nn.Module):

    def __init__(self):

        super().__init__()
        #input is 48 neurons, output is 12
        self.lin1 = torch.nn.Linear(48, 128)
        self.lin2 = torch.nn.Linear(128, 64)
        self.lin3 = torch.nn.Linear(64, 32)
        self.lin4 = torch.nn.Linear(32, 12)

        self.relu = torch.nn.ReLU()
    
    def forward(self, x):
        x = self.lin1(x)
        x = self.relu(x)
        x = self.lin2(x)
        x = self.relu(x)
        x = self.lin3(x)
        x = self.relu(x)
        x = self.lin4(x)
        x = self.relu(x)

        return x

class cubeAgent:


    def __init__(self, stateSize, actionSize):

        self.ALPHA = 0.1
        self.GAMMA = 0.9
        self.EPSILON = 1.0
        self.EPSILON_MIN = 0.05
        self.EPSILON_DECAY = 0.995

        self.stateSize = stateSize
        self.actionSize = actionSize
        self.memory = deque(maxlen = 2000)

        self.model = cubeNetwork()
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr = self.ALPHA)
        self.lossFunc = torch.nn.MSELoss()

    def remember(self, state, action, reward, nextState, done):
        self.memory.append((state, action, reward, nextState, done))

    def act(self, state):
        if numpy.random.rand() <= self.EPSILON:
            return random.randrange(self.actionSize)
        stateTensor = torch.FloatTensor(state).unsqueeze(0)
        with torch.no_grad():
            qValues = self.model(stateTensor)
        return torch.argmax(qValues).item()
    
    def replay(self, batchSize = 32):
        if len(self.memory) < batchSize:
            return
        miniBatch = random.sample(self.memory, batchSize)
        states = torch.FloatTensor([m[0] for m in miniBatch])
        actions = torch.LongTensor([m[1] for m in miniBatch])
        rewards = torch.FloatTensor([m[2] for m in miniBatch])
        nextStates = torch.FloatTensor([m[3] for m in miniBatch])
        dones = torch.FloatTensor([m[4] for m in miniBatch])

        qCurrent = self.model(states).gather(1, actions.unsqueeze(1)).squeeze(1)
        qNext = self.model(nextStates).max(1)[0]
        qTarget = rewards + (self.GAMMA * qNext * (1 - dones))

        loss = self.lossFunc(qCurrent, qTarget.detach())
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        if self.EPSILON > self.EPSILON_MIN:
            self.EPSILON *= self.EPSILON_DECAY

    def applyMove(self, move, actions):

        clockwise = True
        letter = ""

        if move > 5:
            clockwise = False

        match move:
            case 0 | 6:
                letter = "U"
            case 1 | 7:
                letter = "D"
            case 2 | 8:
                letter = "L"
            case 3 | 9:
                letter = "R"
            case 4 | 10:
                letter = "F"
            case 5 | 11:
                letter = "B"

        if clockwise:
            actions.send_keys(letter).perform()
        else:
            actions.key_down(Keys.SHIFT) \
                .send_keys(letter) \
                .key_up(Keys.SHIFT) \
                .perform()
        

if __name__=="__main__":
    flaskThread = Thread(target = runServer, daemon = True)
    flaskThread.start()

    driver = bootup("solobutton333")
    actions = ActionChains(driver)

    stateSize = len(COORD_LIST)
    actionSize = 12
    agent = cubeAgent(stateSize, actionSize)

    lastState = None
    lastAction = None

    while True:
        driver.save_screenshot("cube.png")
        image = Image.open("cube.png")

        state = []
        for coordX, coordY in COORD_LIST:
            pixel = image.getpixel((coordX, coordY))
            state.append(COLOR_MAP[colourClass(pixel)])

        if lastState is not None and lastAction is not None:
            reward = sharedData["solvingScore"]
            done = reward >= TARGET_SCORE
            agent.remember(lastState, lastAction, reward, state, done)
            agent.replay(batchSize = 32)

        action = agent.act(state)
        agent.applyMove(action, actions)

        lastState = state
        lastAction = action

        time.sleep(0.2)
