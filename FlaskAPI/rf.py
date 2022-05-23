import gym
from gym import spaces
import numpy as np

MAX_STEPS = 50000000

class CustomEnv(gym.Env):
    # Custom Environment that follows the gym inferface
    metadata = {'render.modes': ['human']}

    def __init__(self, df):
        super(CustomEnv, self).__init__()

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



    def render(self, mode='human', close=False):
        #render the environment as print 
        print(f'Step: {self.current_step}')

