import os
import sys

def invalid_parameters():
    print("Invalid parameters")
    sys.exit()    

load = False

params = sys.argv[1:]
valid_params = ["-rom", "-gen", "-uni", "-create"]
params_out = ["Super Mario Bros (Machine Learned).nes", "0", "True", "False"]
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
            if param_value == -1:
                invalid_parameters()
            else:
                params_out[param_value] = param
    load = True
else:
    invalid_parameters()
                
backup_loc = "Backups - " + params_out[valid_params.index("-rom")]
if params_out[valid_params.index("-uni")].lower() == "true":
    backup_loc = "Universal Backups"
    
    comment = ""
    if params_out[valid_params.index("-create")].lower() == "false":
        comment = "-- "
    elif params_out[valid_params.index("-create")].lower() != "true":
        invalid_parameters()
        
elif params_out[valid_params.index("-uni")].lower() != "false":
    invalid_parameters()

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