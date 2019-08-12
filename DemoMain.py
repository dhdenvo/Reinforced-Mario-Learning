import sys
import os

def invalid_parameters(i):
    print("Invalid Parameters", i)
    quit()

params = sys.argv[1:]
valid_params = ["-gen", "-game", "-name"]
params_out = ["267", "machine", "Super Mario Bros (Machine Learned).nes"]
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
                invalid_parameters(1)                
        else:
            if param_value == -1 or (param_value == 0 and not param.isdigit()):
                invalid_parameters(2)
            else:
                params_out[param_value] = param
    load = True
else:
    invalid_parameters(3)

if params_out[valid_params.index("-game")].lower() == "create":
    os.system("cd 'Map Creator/'; python MapCreatorMain.py " + params_out[valid_params.index("-name")] + " " + params_out[valid_params.index("-gen")])
elif params_out[valid_params.index("-game")].lower() == "machine":
    os.system("cd Reinforced\ Mario\ Demo; python RunDemoMain.py -gen " + params_out[valid_params.index("-gen")] + " -rom '" + params_out[valid_params.index("-name")] + "'")
else:
    print("Invalid game type")
