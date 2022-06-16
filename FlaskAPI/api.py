from distutils.fancy_getopt import fancy_getopt
from importlib.resources import path
from operator import truediv
from pickle import FALSE
from types import SimpleNamespace
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
# importam librarile pentru modelul de ML
from sklearn.tree import DecisionTreeClassifier # Import Decision Tree Classifier
from sklearn.ensemble import RandomForestClassifier #Inportam Random Forest
from sklearn.model_selection import train_test_split # Import train_test_split function
from sklearn import metrics #Import scikit-learn metrics module for accuracy calculation
import json
import pandas as pd
import numpy as np

# for automatisation
from pywinauto.application import Application
from pywinauto.keyboard import send_keys, KeySequenceError
import time
import os


app = Flask(__name__)
app.config["DEBUG"] = True
id = "0"

#mode = "rf"
mode = "supervised"

class kartAgent(object):
    id = 0
    fileId = 0
    time = 0.0000
    xPos = 0.0000
    yPos = 0.0000
    zPos = 0.0000
    leftSide = False
    leftForward = False
    centralForward = False
    rightForward = False
    rightSide = False
    leftSideDistance = 5.00
    leftForwardDistance = 5.00
    centralForwardDistance = 5.00
    rightForwardDistance = 5.00
    rightSideDistance = 5.00
    zone = 1
    movingForward = True
    moveForwardInput = True
    moveBackwardsInput = False
    moveLeftInput = True
    moveRightInput = False
    state = 15
    gameOver = False

kart = [
    {'id':kartAgent.id,
     'fileId':kartAgent.fileId,
     'time':kartAgent.time,
     'xPos':kartAgent.xPos,
     'yPos':kartAgent.yPos,
     'zPos':kartAgent.zPos,
     'leftSide':kartAgent.leftSide,
     'leftForward':kartAgent.leftForward,
     'centralForward':kartAgent.centralForward,
     'rightForward':kartAgent.rightForward,
     'rightSide':kartAgent.rightSide,
     'leftSideDistance':kartAgent.leftSideDistance,
     'leftForwardDistance':kartAgent.leftForwardDistance,
     'centralForwardDistance':kartAgent.centralForwardDistance,
     'rightForwardDistance':kartAgent.rightForwardDistance,
     'rightSideDistance':kartAgent.rightSideDistance,
     'zone':kartAgent.zone,
     'movingForward':kartAgent.movingForward,
     'moveForwardInput':kartAgent.moveForwardInput,
     'moveBackwardsInput':kartAgent.moveBackwardsInput,
     'moveLeftInput':kartAgent.moveLeftInput,
     'moveRigthInput':kartAgent.moveRightInput,
     'state':kartAgent.state,
     'gameOver':kartAgent.gameOver
    }
]



# game location
game_location = "C:\Poli\Dizertatie\Repo_Github\KartML\Export\ControlledByML\MachineLearning_Karts.exe"

###################################
#
# SUPERVISED ML
# 
###################################
#import merged cvs
#citim datele din fisier
data=pd.read_csv(r"C:\Poli\Dizertatie\Repo_Github\KartML\Export_Csv\merged_final.csv")

#clean data
#data = data[data['State'] != "0"]
data["xPos"] = pd.to_numeric(data["xPos"], downcast="float")
data = data[data['zone'].notna()]

# selectam coloana pe care vrem sa o considera tinta/target. In cazul de fata o sa vrem sa vedem care rezervare sunt anulate
y = data.state

#selectam features-urile. O sa fie toate coloanele mai putin coloanele de mai jos 
x=data
x.drop('fileId',axis=1,inplace = True)
x.drop('moveForwardInput', axis=1, inplace=True)
x.drop('moveBackwardsInput', axis=1, inplace=True)
x.drop('moveLeftInput', axis=1, inplace=True)
x.drop('moveRightInput', axis=1, inplace=True)
x.drop('state',axis=1,inplace=True)
x.drop('gameOver',axis=1,inplace=True)

#impartim setul de datele in set de antrenare si set de testare
x_train, x_test, y_train, y_test = train_test_split(x.values, y.values, test_size=0.3, random_state=10) # 70% training and 30% tes

# construim modelul - Decision Tree Clasifier
# Create Decision Tree classifer object
dtc_ML = DecisionTreeClassifier()
rf_ML = RandomForestClassifier()

# Train Decision Tree Classifer
dtc_ML = dtc_ML.fit(x_train,y_train)
rf_ML = rf_ML.fit(x_train,y_train)

#Predict the response for test dataset
y_pred_dtc = dtc_ML.predict(x_test)
y_pred_rf = rf_ML.predict(x_test)
#Evaluam Modelul
# Model Accuracy, how often is the classifier correct?
print("Accuracy Decision Tree:",metrics.accuracy_score(y_test, y_pred_dtc))
print("Accuracy Random Forest:",metrics.accuracy_score(y_test, y_pred_rf))
def returnActions(object):
    kartLoc = kartAgent()
    kartLoc.time = object['time']
    kartLoc.xPos = object['xPos']
    kartLoc.yPos = object['yPos']
    kartLoc.zPos = object['zPos']
    kartLoc.leftSide = object['leftSide']
    kartLoc.leftForward = object['leftForward']
    kartLoc.centralForward = object['centralForward']
    kartLoc.rightForward = object['rightForward']
    kartLoc.rightSide = object['rightSide']
    kartLoc.leftSideDistance = object['leftSideDistance']
    kartLoc.leftForwardDistance = object['leftForwardDistance']
    kartLoc.centralForwardDistance = object['centralForwardDistance']
    kartLoc.rightForwardDistance = object['rightForwardDistance']
    kartLoc.rightSideDistance = object['rightSideDistance']
    kartLoc.zone = object['zone']
    kartLoc.movingForward = object['movingForward']
    kartLoc.gameOver = object['gameOver']

    newModel = [[kartLoc.time,kartLoc.xPos,kartLoc.yPos,kartLoc.zPos,kartLoc.leftSide,kartLoc.leftForward,kartLoc.centralForward,kartLoc.rightForward,kartLoc.rightSide,kartLoc.leftSideDistance,kartLoc.leftForwardDistance,kartLoc.centralForwardDistance,kartLoc.rightForwardDistance,kartLoc.rightSideDistance,kartLoc.zone,kartLoc.movingForward]]
    prediction = rf_ML.predict(newModel)
    kartLoc.state = str(prediction[0])
    #print(object)
    print("Decision: ",kartLoc.state)
    return json.dumps(kartLoc.__dict__)

###############################################################
#
# REINFORCEMENT LEARNING
#
###############################################################

# init kart object
kartRF = kartAgent()
def init_kartRF():
    kartRF.id = 0
    kartRF.time = 0
    kartRF.xPos = 0
    kartRF.yPos = 0
    kartRF.zPos = 0
    kartRF.leftSide = False
    kartRF.leftForward = False
    kartRF.centralForward = False
    kartRF.rightForward = False
    kartRF.rightSide = False
    kartRF.leftSideDistance = 5
    kartRF.leftForwardDistance = 5
    kartRF.centralForwardDistance = 5
    kartRF.rightForwardDistance = 5
    kartRF.rightSideDistance = 5
    kartRF.zone = 1
    kartRF.movingForward = False
    kartRF.gameOver = False
    kartRF.state = 0

def update_kart_RF(body):
    global kartRF
    kartRF.state = body["state"]

def update_kart_unity(body):
    global kartRF
    kartRF.id = body["id"]
    kartRF.time = body["time"]
    kartRF.xPos = body["xPos"]
    kartRF.yPos = body["yPos"]
    kartRF.zPos = body["zPos"]
    kartRF.leftSide = body["leftSide"]
    kartRF.leftForward = body["leftForward"]
    kartRF.centralForward = body["centralForward"]
    kartRF.rightForward = body["rightForward"]
    kartRF.rightSide = body["rightSide"]
    kartRF.leftSideDistance = body["leftSideDistance"]
    kartRF.leftForwardDistance = body["leftForwardDistance"]
    kartRF.centralForwardDistance = body["centralForwardDistance"]
    kartRF.rightForwardDistance = body["rightForwardDistance"]
    kartRF.rightSideDistance = body["rightSideDistance"]
    kartRF.zone = body["zone"]
    kartRF.movingForward = body["movingForward"]
    kartRF.gameOver = body["gameOver"]
    
###############################################################
#
# FLASK API
# 
###############################################################

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''

# A route to return all of the available entries in our catalog.
@app.route('/api/kart', methods=['GET'])
def api_all():
    return jsonify(kart)

########################################################################
#
# RANDOM FORREST / DECISSION TREE ENDPOINTS
#
########################################################################

# Endpoint to create a new guide
@app.route('/kart', methods=['POST'])
def create_person():
    # POST request 
        global kartRF
        body = request.get_json() # get the request body content
        if body is None:
            return "The request body is null", 404
        if 'id' not in body:
            return 'You need to specify the id',404
        if 'fileId' not in body:
            return 'You need to specify the fileId', 404
        if 'time' not in body:
            return 'You need to specify the time', 404
        if 'xPos' not in body:
            return 'You need to specify the xPos', 404
        if 'yPos' not in body:
            return 'You need to specify the yPos', 404
        if 'zPos' not in body:
            return 'You need to specify the zPos', 404
        if 'leftSide' not in body:
            return 'You need to specify the leftSide', 404
        if 'leftForward' not in body:
            return 'You need to specify the leftForward', 404
        if 'centralForward' not in body:
            return 'You need to specify the centralForward', 404
        if 'rightForward' not in body:
            return 'You need to specify the rightForward', 404
        if 'rightSide' not in body:
            return 'You need to specify the rightSide', 404
        if 'leftSideDistance' not in body:
            return 'You need to specify the leftSideDistance', 404
        if 'leftForwardDistance' not in body:
            return 'You need to specify the leftForwardDistance', 404
        if 'centralForwardDistance' not in body:
            return 'You need to specify the centralForwardDistance', 404
        if 'rightForwardDistance' not in body:
            return 'You need to specify the rightForwardDistance', 404
        if 'rightSideDistance' not in body:
            return 'You need to specify the rightSideDistance', 404
        if 'zone' not in body:
            return 'You need to specify the zone', 404
        if 'movingForward' not in body:
            return 'You need to specify the movingForward', 404
        if 'state' not in body:
            return 'You need to specify the state', 404
        if 'gameOver' not in body:
             return 'You need to specify the game status (done/ongoing)', 404
        if(mode == "rf"):
            update_kart_unity(body)
            return json.dumps(kartRF.__dict__)
        else:
            return returnActions(body)
        #return "ok", 200

###################################################################
#
# START/END GAME
#
###################################################################
# A route to start the game
@app.route('/api/start-game', methods=['GET'])
def start_game():
    # start game
    #os.startfile(game_location)
    app1 = Application(backend="win32").start(cmd_line="C:\Poli\Dizertatie\Repo_Github\KartML\Export\ControlledByML\MachineLearning_Karts.exe")
    time.sleep(12)
    send_keys("{SPACE}")
    time.sleep(1)
    send_keys("{SPACE}")
    time.sleep(4)
    return jsonify("OK")

# A route to start the game
@app.route('/api/end-game', methods=['GET'])
def end_game():
    # start game
    os.system("TASKKILL /F /IM MachineLearning_Karts.exe")
    return jsonify("OK")

##############################################################################
#
# REINFORCEMENT LEARING ENDPOINTS
#
##############################################################################

# A route to return all of the available entries in our catalog.
@app.route('/api/get-kart-rf', methods=['GET'])
def get_kart_rf():
    return json.dumps(kartRF.__dict__)

# A route to return all of the available entries in our catalog.
@app.route('/api/init-kart-rf', methods=['GET'])
def init_kart_rf():
    init_kartRF()
    return json.dumps(kartRF.__dict__)

# A route to start the game
@app.route('/api/update-kart-rf', methods=['POST'])
def update_kart_rf():
    # POST request
    body = request.get_json() # get the request body content
    if body is None:
        return "The request body is null", 404
    if 'state' not in body:
        return 'You need to specify the state', 404
    update_kart_RF(body)
    return json.dumps(kartRF.__dict__)
app.run()


