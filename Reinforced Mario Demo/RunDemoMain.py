import os
import sys

def invalid_parameters(i):
    print("Invalid parameters", i)
    sys.exit()    

load = False

params = sys.argv[1:]
valid_params = ["-rom", "-gen", "-uni", "-create"]
params_out = ["Super Mario Bros (Machine Learned).nes", "0", "True", "False"]
default_rom = params_out[0]
completed_params = []

if len(params) % 2 == 0:
    param_value = -1
    for i, param in enumerate(params):
        if i % 2 == 0:
            print(param)
            print(valid_params)
            print(completed_params)
            if param in valid_params and not param in completed_params:
                param_value = valid_params.index(param) 
                completed_params.append(param)
            else:
                invalid_parameters(1)                
        else:
            if param_value == -1:
                invalid_parameters(2)
            else:
                params_out[param_value] = param
    load = True
else:
    invalid_parameters(3)
                
backup_loc = "Backups - " + params_out[valid_params.index("-rom")]
comment = "-- "
if params_out[valid_params.index("-uni")].lower() == "true" or params_out[valid_params.index("-rom")] == default_rom:
    backup_loc = "Universal Backups"        
elif params_out[valid_params.index("-uni")].lower() != "false":
    invalid_parameters()
if params_out[valid_params.index("-create")].lower() == "true":
    comment = ""
elif params_out[valid_params.index("-create")].lower() != "false":
    invalid_parameters()

valid_backup = True
try:
    file_check = open(backup_loc + "/Backup - " + params_out[valid_params.index("-gen")] + ".txt", "r")
    file_check.close()
except FileNotFoundError:
    valid_backup = False
    
if not valid_backup:
    backup_loc = "Universal Backups"
    comment = "-- "
    params_out[valid_params.index("-gen")] = "0"
    

lua_script = open("NeatEvolve.lua", "r")
running_script = open("RunningEvolve.lua", "w")

replace = {"David Was Here!!!!": backup_loc + "/Backup - " + params_out[valid_params.index("-gen")] + ".txt", "Mario Jumpman Mario": str(load).lower(), "LuigiBackups": backup_loc, "BowserComment ": comment}
script_text = lua_script.read()
for before, after in replace.items():
    script_text = script_text.replace(before, after)
       
#script_text = lua_script.read().replace("David Was Here!!!!", backup_loc + "/Backup - " + params_out[valid_params.index("-gen")] + ".txt").replace("Mario Jumpman Mario", str(load).lower()) \
#    .replace("LuigiBackups", backup_loc).replace("BowserComment ", comment)    
    
running_script.write(script_text)

run_demo_cmd = 'fceux "' + params_out[valid_params.index("-rom")] + '"'
os.system(run_demo_cmd)
