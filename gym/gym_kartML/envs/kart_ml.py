import gym
from gym import spaces
import numpy as np

# flask
from distutils.fancy_getopt import fancy_getopt
from importlib.resources import path
from operator import truediv
from types import SimpleNamespace
from flask import Flask, jsonify, request
from flask_restful import Resource, Api

# for automatisation
from pywinauto.application import Application
from pywinauto.keyboard import send_keys, KeySequenceError
import time
import os

app = Flask(__name__)
app.config["DEBUG"] = True

class KartML(gym.Env):
    # Custom Environment that follows the gym inferface
    metadata = {'render.modes': ['human']}

    def __init__(self, df):
        super(KartML, self).__init__()

        # define action space
        # gym.spaces objects
        action_space = spaces.Discrete(4)
        self.action_space = action_space

        
        """
        The following dictionary maps abstract actions from `self.action_space` to 
        the direction we will walk in if that action is taken.
        I.e. 0 corresponds to "right", 1 to "up" etc.
        """
        self._action_to_direction = {
            0: np.array([1, 0]),
            1: np.array([0, 1]),
            2: np.array([-1, 0]),
            3: np.array([0, -1]),
        }


        # define observation space
        # gym.spaces objects
        time = spaces.Box(low=0, high=50.0, dtype=np.float32) #float (min 0 max 50) -> Box(low=0, high=50.0, dtype=np.float32)
        #x_pos = 1 #float (min -100 max 100) -> Box(low=-100.0, high=100.0, dtype=np.float32)
        #y_pos = 2 #float (min -100 max 100) -> Box(low=-100.0, high=100.0, dtype=np.float32)
        #z_pos = 3 #float (min -100 max 100) -> Box(low=-100.0, high=100.0, dtype=np.float32)
        # x-pos, y-pos, z-pos
        pos = spaces.Box(low=np.array([-100.0,-100.0,-100.0]), high=np.array([100.0,100.0,100.0]),dtype=np.float32)
        moving_forward = spaces.Discrete(1, start = 0) #bool -> Discrete(1)
        #left_forward_sensor = 3.5 # float (min 0 max 5) -> Box(low=0, high=5.0, dtype=np.float32)
        #left_central_sensor = 3.5 # float (min 0 max 5) -> Box(low=0, high=5.0, dtype=np.float32)
        #central_sensor = 3.5 # float (min 0 max 5) -> Box(low=0, high=5.0, dtype=np.float32)
        #right_central_sensor = 3.5 # float (min 0 max 5) -> Box(low=0, high=5.0, dtype=np.float32)
        #right_forward_sensor = 3.5 # float (min 0 max 5) -> Box(low=0, high=5.0, dtype=np.float32)
        sensors = spaces.Box(low=np.array([0,0,0,0,0]), high=np.array([5,5,5,5,5]),dtype=np.float32)
        zone = spaces.Discrete(3, start = 1) #int (min 1 max 3) -> Discrete(3, start = 1)
        gameOver = spaces.Discrete(2)
        observation_space =  spaces.Dict(
            {
                "time":time,
                "position":pos,
                "movingForward":moving_forward,
                "sensors":sensors,
                "zone":zone,
                "gameOver":gameOver
            }
        )
        self.observation_space = observation_space

    def _get_obs(self):
        return {
                "time": self._time,
                "position": self._position,
                "movingForward":self._moving_forward,
                "sensors":self._sensors,
                "zone":self.zone,
                "gameOver":self.gameOver
            }

    def step(self, action):
        # Map the action (element of {0,1,2,3}) to the direction we walk in
        direction = self._action_to_direction[action]
       
        if direction == 0:
            #move forward
        elif direction == 1:
            #move backwards
        elif direction == 2:
            #move left
        elif direction == 3
            #move right
        self.current_step += 1
        
        reward =self._get_reward() 
  
        done = self.observation_space["gameOver"]
        obs = self._get_obs()
        return obs, reward, done, {}  

    def reset(self):
        # reset the state of the environment to the initil state
        # call the reset endpoint which will close the exe and open again
        observation = self._get_obs()
        return self.observation()


    def _get_reward(self):
        
        movingForward = self.observation_space["movingForward"]
        #if moving -> return 100 else 0
        reward = 100 if movingForward else 0
        
        sensors = self.observation_spaces["sensors"]
        obstacle = False
        for sensor in sensors:
            if sensor < 1:
                obstacle = True

       #if distance to one wall < 1 -> return -200
        reward = reward - 200 if obstacle  else 0
        return reward

    def getFromUnity():
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
        kartLoc.state = str(prediction[0])
        return json.dumps(kartLoc.__dict__)
    



    def render(self, mode='human', close=False):
        #render the environment as print 
        print(f'Step: {self.current_step}')


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
        if 'state' not in body:
            return 'You need to specify the state', 404
        if 'gameOver' not in body:
             return 'You need to specify the game status (done/ongoing)', 404
        return getActions(body)
        #return "ok", 200

# A route to start the game
@app.route('/api/start-game', methods=['GET'])
def start_game():
    # start game
    #os.startfile(game_location)
    app1 = Application(backend="win32").start(cmd_line="C:\Poli\Dizertatie\Repo_Github\KartML\Export\ControlledByHuman\MachineLearning_Karts.exe")
    time.sleep(5)
    send_keys("{SPACE}")
    time.sleep(1)
    send_keys("{SPACE}")
    return jsonify("OK")

# A route to start the game
@app.route('/api/end-game', methods=['GET'])
def end_game():
    # start game
    os.system("TASKKILL /F /IM MachineLearning_Karts.exe")
    return jsonify("OK")
    
app.run()