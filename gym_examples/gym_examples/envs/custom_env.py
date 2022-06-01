import gym
from gym import spaces
import numpy as np
import requests
import json


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
kartRF = kartAgent()
##########################################################################
#
# UPDATE KART OBJECT
#
##########################################################################   
def update_kart(body,source):
    global kartRF
    if(source == "unity"):
        kartRF.id = body["id"]
        kartRF.fileId = 0
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
    

##########################################################################
#
#  REQUESTS TO FLASK API
#
##########################################################################

def get_kart_ml():
    response = requests.get("http://127.0.0.1:5000/api/get-kart-rf")
    update_kart(response.json(), "unity")

def init_kart_ml():
    response = requests.get("http://127.0.0.1:5000/api/init-kart-rf")

def post_req():
    global kartRF
    response = requests.post("http://127.0.0.1:5000/api/update-kart-rf",json={"state":kartRF.state})
    print(response.json())

##########################################################################
#
#   START/END GAME
#
##########################################################################
def start_game():
    response = requests.get("http://127.0.0.1:5000/api/start-game")
    print("game started ")

def end_game():
    response = requests.get("http://127.0.0.1:5000/api/end-game")
    print("game stoped ")

##########################################################################
#
#    INIT KART OBJECT
#
##########################################################################

def init_kartRF():
    global kartRF
    kartRF.id = 0
    kartRF.fileId = 0
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
    kartRF.state = 7
class CustomEnv(gym.Env):
    # Custom Environment that follows the gym inferface
    metadata = {'render.modes': ['human']}



##########################################################################
#
#  FUNCTIONS
#
##########################################################################


    def __init__(self):
        super(CustomEnv, self).__init__()
        init_kartRF()
        self.current_step = 0
        # define action space
        # gym.spaces objects
        action_space = spaces.Discrete(4)
        self.action_space = action_space
        self.reward = 0

        # define observation space
        # gym.spaces objects
        time = spaces.Box(low=0, high=50.0, shape=(1,),dtype=np.float32) #float (min 0 max 50) -> Box(low=0, high=50.0, dtype=np.float32)
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

    def _get_reward(self):
        movingForward = kartRF.movingForward
        #if moving -> return 100 else 0
        reward =  100 if movingForward else  -2000

        # distance == 5
        if kartRF.leftSideDistance == 5 :
            reward = reward + 10
        if kartRF.leftForwardDistance == 5 :
            reward = reward + 10
        if kartRF.centralForwardDistance == 5 :
            reward = reward + 10
        if kartRF.rightForwardDistance == 5 :
            reward = reward + 10
        if kartRF.rightSideDistance == 5 :
            reward = reward + 10

        # distance < 5 && distance >= 2.5
        if kartRF.leftSideDistance < 5 and kartRF.leftSideDistance >= 2.5:
            reward = reward - 50
        if kartRF.leftForwardDistance < 5 and kartRF.leftForwardDistance >= 2.5:
            reward = reward - 50
        if kartRF.centralForwardDistance < 5 and kartRF.centralForwardDistance >= 2.5:
            reward = reward - 50
        if kartRF.rightForwardDistance < 5 and kartRF.rightForwardDistance >= 2.5:
            reward = reward - 50
        if kartRF.rightSideDistance < 5 and kartRF.rightSideDistance >= 2.5:
            reward = reward - 50

        # distance < 2.5 && distance >= 1
        if kartRF.leftSideDistance < 2.5 and kartRF.leftSideDistance >= 1:
            reward = reward - 100
        if kartRF.leftForwardDistance < 2.5 and kartRF.leftForwardDistance >= 1:
            reward = reward - 1000
        if kartRF.centralForwardDistance < 2.5 and kartRF.centralForwardDistance >= 1:
            reward = reward - 1000
        if kartRF.rightForwardDistance < 2.5 and kartRF.rightForwardDistance >= 1:
            reward = reward - 1000
        if kartRF.rightSideDistance < 2.5 and kartRF.rightSideDistance >= 1:
            reward = reward - 1000

        # distance < 1
        if kartRF.leftSideDistance < 1:
            reward = reward - 2500
        if kartRF.leftForwardDistance < 1:
            reward = reward - 2500
        if kartRF.centralForwardDistance < 1:
            reward = reward - 2500
        if kartRF.rightForwardDistance < 1:
            reward = reward - 2500
        if kartRF.rightSideDistance < 1:
            reward = reward - 2500
        
        print("reward ",reward)
        return reward

    def _get_obs(self):
        global kartRF
        return [kartRF.time,kartRF.xPos,kartRF.yPos,kartRF.zPos,kartRF.movingForward,kartRF.leftForwardDistance,kartRF.leftSideDistance,kartRF.centralForwardDistance,kartRF.rightSideDistance,kartRF.rightForwardDistance,kartRF.zone,kartRF.gameOver]
##########################################################################
#
#  STEP
#
##########################################################################
    def getFromUnity(body,self):
        
        self.observation_space["time"] = object["time"]
        self.observation_space["position"] = np.array([object["xPos"],object["yPos"],object["zPos"]])
        self.observation_space["movingForward"] = np.array([object["leftSide"],object["leftForward"],object["centralForward"],object["rightForward"],object["rightSide"]])
        self.observation_space["zone"] = object["zone"]
        self.observation_space["gameOver"] = object["gameOver"]

    def step(self, action):
        print("action ", action)
        global kartRF
        get_kart_ml()
        #send command to Unity
        if action == 0:
            #move forward
            kartRF.state = 7
        elif action == 1:
            #move backwards
            kartRF.state = 11
        elif action == 2:
            #move left
            kartRF.state = 14
        elif action == 3:
            #move right
            kartRF.state = 13

        post_req()

        self.current_step += 1
        
        reward =self._get_reward()
        done = False 
        if kartRF.gameOver == True:
            done = True
        if kartRF.time > 80.00:
            done = True
        obs = self._get_obs()
        return obs, reward, done, {}  

##########################################################################
#
#  RESET
#
##########################################################################
    def reset(self):
        # reset the state of the environment to the initil state
        init_kartRF()
        # call the reset endpoint which will close the exe and open again
        end_game()
        init_kart_ml()
        start_game()
        observation = self._get_obs()
        return observation

##########################################################################
#
#  RENDER
#
##########################################################################
    def render(self, mode='human', close=False):
        #render the environment as print 
        print(f'Step: {self.current_step}')

