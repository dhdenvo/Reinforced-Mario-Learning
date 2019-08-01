from gym_super_mario_bros import SuperMarioBrosEnv

class MarioNESRomEnv(SuperMarioBrosEnv):
    def __init__(self, rom_path):
        super(SuperMarioBrosEnv, self).__init__(rom_path)        
        self._target_world, self._target_stage, self._target_area = 1, 1, 1
        # setup a variable to keep track of the last frames time
        self._time_last = 0
        # setup a variable to keep track of the last frames x position
        self._x_position_last = 0
        # reset the emulator
        self.reset()
        # skip the start screen
        self._skip_start_screen()
        # create a backup state to restore from on subsequent calls to reset
        self._backup()        
        
    def _get_info(self):
        info = super()._get_info()
        info["ram"] = self.ram
        return info
   
#Example code to create a basic environment of the class 
'''env = MarioNESRomEnv("/home/DavidDaghelian/Programs/Pie-Thon/Super Mario Bros Programs/Super Mario Bros Details/Final Products/Super Mario Bros (Machine Learned).nes")

done = True
frame = 0

while True:
    if done:
        state = env.reset()
        frame = 0
        
    state, reward, done, info = env.step(env.action_space.sample())
    env.render()
    frame += 1
env.close()'''
    