import os
import sys

#The function that gets called when invalid parameters are entered
def invalid_parameters(i):
    print("Invalid parameters", i)
    sys.exit()    

load = False

#The parameters that get entered when the program is called from the command line
#This excludes the name of the python script (ex python RunDemoMain.py -gen 48 => params = ["RunDemoMain.py", "-gen", "48"])
params = sys.argv[1:]
#Valid options for the parameters (ex: python RunDemoMain.py -gen 10 -uni False)
valid_params = ["-rom", "-gen", "-uni", "-create"]
#Default values for the above options
params_out = ["Super Mario Bros (Machine Learned).nes", "0", "True", "False"]
default_rom = params_out[0]
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
            if param_value == -1 or (param_value == 1 and not param.isdigit()):
                invalid_parameters(2)
            else:
                params_out[param_value] = param
    load = True
else:
    invalid_parameters(3)
             
#The location for the backups   
backup_loc = "Backups - " + params_out[valid_params.index("-rom")]
#The string that gets added for the comments
comment = "-- "
#If using the -uni option is true or using the default rom, then use the Universal Backups
if params_out[valid_params.index("-uni")].lower() == "true" or params_out[valid_params.index("-rom")] == default_rom:
    backup_loc = "Universal Backups"
#If the -uni option isn't false or true (checked above), then the command is invalid
elif params_out[valid_params.index("-uni")].lower() != "false":
    invalid_parameters()
#If the program creates new backups, make sure that the loading lines are not commented
if params_out[valid_params.index("-create")].lower() == "true":
    comment = ""
    #If the -create option isn't false or true (checked above), then the command is invalid
elif params_out[valid_params.index("-create")].lower() != "false":
    invalid_parameters()

#Check if the backup is valid
valid_backup = True
try:
    file_check = open(backup_loc + "/Backup - " + params_out[valid_params.index("-gen")] + ".txt", "r")
    file_check.close()
except FileNotFoundError:
    valid_backup = False
    
#If the backup is invalid, make it start from scratch, but not writing to the backups
if not valid_backup:
    backup_loc = "Universal Backups"
    comment = "-- "
    params_out[valid_params.index("-gen")] = "0"
    
#Load the blank ready to be formatted lua script
lua_script = open("NeatEvolve.lua", "r")
#Load the file which is going to be written with the new lua script
running_script = open("RunningEvolve.lua", "w")

#Dynamic method of mass replacing several strings in the lua script with other string
replace = {"David Was Here!!!!": backup_loc + "/Backup - " + params_out[valid_params.index("-gen")] + ".txt", "Mario Jumpman Mario": str(load).lower(), "LuigiBackups": backup_loc, "BowserComment ": comment}
script_text = lua_script.read()
for before, after in replace.items():
    script_text = script_text.replace(before, after)  

#Write the formatted lua script to the new lua script file    
running_script.write(script_text)

#Run fceux with the rom loaded (the user has to load the lua script themselves)
run_demo_cmd = 'fceux "' + params_out[valid_params.index("-rom")] + '" &'
os.system(run_demo_cmd)
