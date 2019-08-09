import sys
import os

params = sys.argv[1:]
valid_params = ["-gen" "-game", "-name"]
params_out = ["267", "machine", "Handmade"]
default_rom = params_out[0]
completed_params = []

if len(params) % 2 == 0:
    param_value = -1
    for i, param in enumerate(params):
        if i % 2 == 0:
            if param in valid_params and not param in completed_params:
                param_value = valid_params.index(param) 
                completed_params.append(param)
            else:
                invalid_parameters()                
        else:
            if param_value == -1 or (param_value == 0 and not param.isdigit()):
                invalid_parameters()
            else:
                params_out[param_value] = param
    load = True
else:
    invalid_parameters()
    
if params_out[valid_params.index("-game")].lower() == "create":
    os.system("cd Map\ Creation; python MapCreatorMain.py " + params_out[valid_params.index("-name")])
elif params_out[valid_params.index("-game")].lower() == "machine":
    os.system("cd Reinforced\ Mario\ Demo; python RunDemoMain.py -gen " + params_out[valid_params.index("-gen")] + " -game " + params_out[valid_params.index("-game")])
else:
    print("Invalid game type")