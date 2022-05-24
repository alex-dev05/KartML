from gym.envs.registration import register

register(
    id='envs/KartML-v0',
    entry_point='gym_examples.envs:KartML',
    max_episode_steps=300,
)