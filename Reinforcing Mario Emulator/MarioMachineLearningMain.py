from nes_py.wrappers import JoypadSpace
import gym_super_mario_bros
from gym_super_mario_bros.actions import SIMPLE_MOVEMENT
env = gym_super_mario_bros.make('SuperMarioBros-v0')
env = JoypadSpace(env, SIMPLE_MOVEMENT)

done = True
step = 0
while True:
    if done:
        state = env.reset()
    state, reward, done, info = env.step(env.action_space.sample())
    #print(info)
    #print(reward, info["x_pos"], info["y_pos"])
    env.render()
    step += 1

env.close()