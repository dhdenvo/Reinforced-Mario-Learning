import sys
import os

#The function that gets called when invalid parameters are entered
def invalid_parameters(i):
    print("Invalid Parameters", i)
    quit()

#The parameters that get entered when the program is called from the command line
#This excludes the name of the python script (ex python DemoMain.py -gen 48 => params = ["DemoMain.py", "-gen", "48"])
params = sys.argv[1:]
#Valid options for the parameters (ex: python DemoMain.py -gen 10 -game machine)
valid_params = ["-gen", "-game", "-name"]
#Default values for the above options
params_out = ["267", "machine", "Super Mario Bros (Machine Learned).nes"]
#Parameters that have already been used
completed_params = []

#Make sure that every option has a given value
if len(params) % 2 == 0:
    param_value = -1
    for i, param in enumerate(params):
        #If the parameter is an option (ex "-gen")
        if i % 2 == 0:
            #The option is valid and not already used
            if param in valid_params and not param in completed_params:
                param_value = valid_params.index(param) 
                completed_params.append(param)
            else:
                invalid_parameters(1)  
        #If the parameter is a value for an option
        else:
            #Check if the value is valid for the specific option
            #If the option is the "-gen" option then the value must be a number
            if param_value == -1 or (param_value == 0 and not param.isdigit()):
                invalid_parameters(2)
            else:
                params_out[param_value] = param
else:
    invalid_parameters(3)

#If we are creating a map, run the map creator program with the parameters of the name and generation and let it do the rest
if params_out[valid_params.index("-game")].lower() == "create":
    os.system("cd 'Map Creator/'; python MapCreatorMain.py " + params_out[valid_params.index("-name")] + " " + params_out[valid_params.index("-gen")])
#If we are running a current map (with the machine playing) then open the more advanced demo program with the basic options set
elif params_out[valid_params.index("-game")].lower() == "machine":
    os.system("cd Reinforced\ Mario\ Demo; python RunDemoMain.py -gen " + params_out[valid_params.index("-gen")] + " -rom '" + params_out[valid_params.index("-name")] + "'")
else:
    print("Invalid game type")
