'''MarI/O by SethBling
Feel free to use this code, but please do not redistribute it.
Intended for use with the BizHawk emulator and Super Mario World or Super Mario Bros. ROM.
For SMW, make sure you have a save state named "DP1.state" at the beginning of a level,
and put a copy in both the Lua folder and the root directory of BizHawk. '''

from Gene import Gene
from Genome import Genome
from Network import Network
from Neuron import Neuron
from Pool import Pool
from Species import Species
from nes_py.wrappers import JoypadSpace
from MarioNESRomEnv import MarioNESRomEnv
from NeuralConstants import *

def recur_create(controls, prev, x):
    for y in x:
        next_cont = prev[:]
        next_cont.append(y)
        if "left" in next_cont and "right" in next_cont:
            next_cont.remove("left")
            next_cont.remove("right")
        if "up" in next_cont and "down" in next_cont:
            next_cont.remove("up")
            next_cont.remove("down")
        next_cont.sort()
        if not next_cont in controls and next_cont != []:
            controls.append(next_cont)
        z = x[:]
        z.remove(y)
        recur_create(controls, next_cont, z)


def calc_control_input(avail_movement, controller):
    controls = []
    for key, valid in controller.items():
        if valid:
            controls.append(key)

    controls.sort()
    sorted_movement = [move[:] for move in avail_movement]
    for avail in sorted_movement:
        avail.sort()

    if controls in sorted_movement:
        return sorted_movement.index(controls)
    
    return avail_movement.index(["NOOP"])

def initializePool(env):
    pool = Pool(env)
    for i in range(0,Population):
        basic = Genome(pool)
        basic.basicGenome()
        pool.addToSpecies(basic)
        
    pool.initializeRun()
    return pool

#writeFile("temp.pool")

#maxFitnessLabel = gui.text(5, 8, "Max Fitness: " .. math.floor(pool.maxFitness))
#form = forms.newform(200, 260, "Fitness")
#maxFitnessLabel = forms.label(form, "Max Fitness: " .. math.floor(pool.maxFitness), 5, 8)
#showNetwork = forms.checkbox(form, "Show Map", 5, 30)
#showMutationRates = forms.checkbox(form, "Show M-Rates", 5, 52)
#restartButton = forms.button(form, "Restart", initializePool, 5, 77)
#saveButton = forms.button(form, "Save", savePool, 5, 102)
#loadButton = forms.button(form, "Load", loadPool, 80, 102)
#saveLoadFile = forms.textbox(form, Filename .. ".pool", 170, 25, nil, 5, 148)
#saveLoadLabel = forms.label(form, "Save/Load:", 5, 129)
#playTopButton = forms.button(form, "Play Top", playTop, 5, 170)
#hideBanner = forms.checkbox(form, "Hide Banner", 5, 190)

complex_controls = [["NOOP"]]
recur_create(complex_controls, [], ButtonNames)
complex_controls = sorted(complex_controls, key=lambda k: len(k))

env = MarioNESRomEnv("/home/DavidDaghelian/Programs/Pie-Thon/ReinforcedMarioLearning/Reinforcing Mario Emulator/Super Mario Bros (Machine Learned).nes")
env = JoypadSpace(env, complex_controls)


pool = None
load = True
pool = initializePool(env)
if load:
    pool.loadFile("Backups/Backup - 267.txt", env)

while True:
    #local backgroundColor = 0xD0FFFFFF
    #if not forms.ischecked(hideBanner) then
    #	gui.drawBox(0, 0, 300, 26, backgroundColor, backgroundColor)
    #end

    species = pool.species[pool.currentSpecies]
    genome = species.genomes[pool.currentGenome]

    #if forms.ischecked(showNetwork) then
    #	displayGenome(genome)
    #end

    if pool.currentFrame % 5 == 0:
        pool.evaluateCurrent()

    control_input = calc_control_input(complex_controls, pool.controller)
    state, reward, done, info = env.step(control_input)

    pool.ram = info["ram"]
    pool.marioX = pool.ram[0x6D] * 0x100 + pool.ram[0x86]
    pool.marioY = pool.ram[0x03B8]+16
    pool.screenX = pool.ram[0x03AD]
    pool.screenY = pool.ram[0x03B8]       

    #joypad.write(1, pool.controller)

    if pool.marioX > pool.rightmost:
        pool.rightmost = pool.marioX
        pool.timeout = TimeoutConstant

    pool.timeout -= 1


    timeoutBonus = pool.currentFrame / 4
    if pool.timeout + timeoutBonus <= 0:
        fitness = pool.rightmost - pool.currentFrame / 2
        if pool.rightmost > 3186:
            fitness = fitness + 1000
        if fitness == 0:
            fitness = -1
        genome.fitness = fitness

        if fitness > pool.maxFitness:
            pool.maxFitness = fitness
            #gui.text(5, 8, "Max Fitness: " .. math.floor(pool.maxFitness))
            #forms.settext(maxFitnessLabel, "Max Fitness: " .. math.floor(pool.maxFitness))
            #pool.writeFile("backup - " + str(pool.generation) + ".txt")

        #console.writeline("Gen " .. pool.generation .. " species " .. pool.currentSpecies .. " genome " .. pool.currentGenome .. " fitness: " .. fitness)
        print("Gen", pool.generation, "species", pool.currentSpecies, "genome", pool.currentGenome, "fitness:", fitness)
        pool.currentSpecies = 0
        pool.currentGenome = 0
        while pool.fitnessAlreadyMeasured():
            pool.nextGenome()

        pool.initializeRun()

    measured = 0
    total = 0
    for species in pool.species:
        for genome in species.genomes:
            total = total + 1
            if genome.fitness != 0:
                measured = measured + 1

    #if not forms.ischecked(hideBanner) then
    #	gui.drawText(0, 0, "Gen " .. pool.generation .. " species " .. pool.currentSpecies .. " genome " .. pool.currentGenome .. " (" .. math.floor(measured/total*100) .. "%)", 0xFF000000, 11)
    #	gui.drawText(0, 12, "Fitness: " .. math.floor(rightmost - (pool.currentFrame) / 2 - (timeout + timeoutBonus)*2/3), 0xFF000000, 11)
    #	gui.drawText(100, 12, "Max Fitness: " .. math.floor(pool.maxFitness), 0xFF000000, 11)
    #end

    env.render()
    pool.currentFrame += 1
