from flask import Flask, jsonify, request
from flask_restful import Resource, Api

app = Flask(__name__)
app.config["DEBUG"] = True

class kartAgent(object):
    id = 0
    file_id = 0
    time = 0.0000
    x_pos = 0.0000
    y_pos = 0.0000
    z_pos = 0.0000
    left_side = False
    left_forward = False
    central_forward = False
    right_forward = False
    right_side = False
    zone = "zone 1"
    moving_forward = True

kart = [
    {'id':kartAgent.id,
     'file_id':kartAgent.file_id,
     'time':kartAgent.time,
     'x_pos':kartAgent.x_pos,
     'y_pos':kartAgent.y_pos,
     'z_pos':kartAgent.z_pos,
     'left_side':kartAgent.left_side,
     'left_forward':kartAgent.left_forward,
     'central_forward':kartAgent.central_forward,
     'right_forward':kartAgent.right_forward,
     'right_side':kartAgent.right_side,
     'zone':kartAgent.zone,
     'moving_forward':kartAgent.moving_forward
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
            return "The request body is null", 400
        if 'id' not in body:
            return 'You need to specify the id',400
        if 'file_id' not in body:
            return 'You need to specify the file_id', 400
        if 'time' not in body:
            return 'You need to specify the time', 400
        if 'x_pos' not in body:
            return 'You need to specify the x_pos', 400
        if 'y_pos' not in body:
            return 'You need to specify the y_pos', 400
        if 'z_pos' not in body:
            return 'You need to specify the z_pos', 400
        if 'left_side' not in body:
            return 'You need to specify the left_side', 400
        if 'left_forward' not in body:
            return 'You need to specify the left_forward', 400
        if 'central_forward' not in body:
            return 'You need to specify the central_forward', 400
        if 'right_side' not in body:
            return 'You need to specify the right_side', 400
        if 'right_forward' not in body:
            return 'You need to specify the right_forward', 400
        if 'zone' not in body:
            return 'You need to specify the zone', 400
        if 'moving_forward' not in body:
            return 'You need to specify the moving_forward', 400
        return "ok", 200

app.run()