
from gym.envs.registration import register


register(
    id='axis-and-allies-4x4-random-agent-v0',
    entry_point='gym_aa.envs:AxisAndAllies4x4RandomAgent'
    #timestep_limit=2000,
)

