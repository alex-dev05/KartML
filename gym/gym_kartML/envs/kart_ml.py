import gym
from gym import spaces
import numpy as np
import requests
import json



app = Flask(__name__)
app.config["DEBUG"] = True

class KartML(gym.Env):

    
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

    # Custom Environment that follows the gym inferface
    metadata = {'render.modes': ['human']}

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
        elif(source == "rf"):
            kartRF.state = body["state"]
##########################################################################
#
#  REQUESTS TO FLASK API
#
##########################################################################

    def get_kart_ml():
        response = requests.get("http://127.0.0.1:5000/api/get-kart-rf")
        update_kart(response, "unity")

    def post_req():
        global kartRF
        response = requests.post("http://127.0.0.1:5000/api/update-kart-rf",json=jsonify(kartRF))
        print(response.json())

##########################################################################
#
#   START/END GAME
#
##########################################################################
    def start_game():
        response = requests.get("http://127.0.0.1:5000/api/start-game")
        print("game started " + response)

    def stop_game():
         response = requests.get("http://127.0.0.1:5000/api/end-game")
         print("game stoped " + response)
##########################################################################
#
#  FUNCTIONS
#
##########################################################################
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

    
        

##########################################################################
#
#    INIT KART OBJECT
#
##########################################################################
    def init_kartRF():
        global kartRF
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
        kartRF.leftSideDistance = False
        kartRF.leftForwardDistance = 5
        kartRF.centralForwardDistance = 5
        kartRF.rightForwardDistance = 5
        kartRF.rightSideDistance = 5
        kartRF.zone = 1
        kartRF.movingForward = False
        kartRF.gameOver = False
        kartRF.state = 0



    def __init__(self, df):
        super(KartML, self).__init__()

        # define action space
        # gym.spaces objects
        action_space = spaces.Discrete(4)
        self.action_space = action_space


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
        global kartRF
        #send command to Unity
        if action == 0:
            #move forward
            kartRF.state = 7
        elif action == 1:
            #move backwards
            kartRF.state = 11
        elif action == 2:
            #move left
            kartRF.state = 13
        elif action == 3:
            #move right
            kartRF.state = 14

        self.current_step += 1
        
        reward =self._get_reward() 
  
        done = self.observation_space["gameOver"]
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
        start_game()
        end_game()
        observation = self._get_obs()
        return self.observation()

##########################################################################
#
#  RENDER
#
##########################################################################
    def render(self, mode='human', close=False):
        #render the environment as print 
        print(f'Step: {self.current_step}')

