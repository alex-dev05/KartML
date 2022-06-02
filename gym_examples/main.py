import gym
import gym_examples
env = gym.make('CustomEnv-v1')
episodes = 0
observation = env.reset()
for _ in range(10000000):
    env.render()
    print(observation)
    action = env.action_space.sample()
    observation, reward, done, info = env.step(action)
    print(observation, reward, done, info)
    if done:
        observation = env.reset(  )
        print("Finished after{} timesteps".format(_+1))
        print("Episode nb{}".format(episodes))
env.close  