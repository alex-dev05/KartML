from gym.envs.registration import register

register(
    id='CustomEnv-v1',
    entry_point='gym_examples.envs:CustomEnv'
)
