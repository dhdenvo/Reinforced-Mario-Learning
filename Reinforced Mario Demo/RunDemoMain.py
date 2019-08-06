import os
import sys

def invalid_parameters():
    print("Invalid parameters")
    sys.exit()    

load = False

params = sys.argv[1:]
valid_params = ["-rom", "-gen"]
params_out = ["Super Mario Bros (Machine Learned).nes", "0"]
completed_params = []

if len(params) > 0 and len(params) % 2 == 0:
    param_value = -1
    for i, param in enumerate(params):
        if i % 2 == 0:
            if param in valid_params and not param in completed_params:
                param_value = valid_params.index(param) 
                completed_params.append(param)
            else:
                invalid_parameters()                
        else:
            if param_value == -1:
                invalid_parameters()
            else:
                params_out[param_value] = param
    load = True
else:
    invalid_parameters()
                

lua_script = open("NeatEvolve.lua", "r")
running_script = open("RunningEvolve.lua", "w")
running_script.write(lua_script.read().replace("David Was Here!!!!", "Backups/Backup - " + params_out[valid_params.index("-gen")] + ".txt").replace("Mario Jumpman Mario", str(load)))

run_demo_cmd = 'fceux -lua RunningEvolve.lua "' + params_out[valid_params.index("-rom")] + '"'
os.system(run_demo_cmd)