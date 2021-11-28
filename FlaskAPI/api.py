from flask import Flask, jsonify, request
from flask_restful import Resource, Api

app = Flask(__name__)
app.config["DEBUG"] = True

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
    zone = "zone 1"
    movingForward = True

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
     'movingForward':kartAgent.movingForward
    }
]

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''

# A route to return all of the available entries in our catalog.
@app.route('/api/kart', methods=['GET'])
def api_all():
    return jsonify(kart)

# Endpoint to create a new guide
@app.route('/kart', methods=['POST'])
def create_person():
    # POST request
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
        return "ok", 200

app.run()