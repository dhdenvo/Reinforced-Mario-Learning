import os

rom_name = ""

lua_script = open("NeatEvolve.lua", "r")
running_script = open("RunningEvolve.lua", "w")
running_script.write(lua_script.replace("David Was Here!!!!", "Backups/Backup - 267.txt"))

run_demo_cmd = "fceux -lua RunningEvolve.lua " + rom_name
os.system(run_demo_cmd)