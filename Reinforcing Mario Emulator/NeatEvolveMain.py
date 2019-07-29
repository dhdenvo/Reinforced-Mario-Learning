'''MarI/O by SethBling
Feel free to use this code, but please do not redistribute it.
Intended for use with the BizHawk emulator and Super Mario World or Super Mario Bros. ROM.
For SMW, make sure you have a save state named "DP1.state" at the beginning of a level,
and put a copy in both the Lua folder and the root directory of BizHawk. '''

ButtonNames = ["A","B","up","down","left","right"]

joypad.write(1, {start:True})

BoxRadius = 6
InputSize = (BoxRadius*2+1)*(BoxRadius*2+1)

Inputs = InputSize + 1
Outputs = len(ButtonNames)

Population = 300
DeltaDisjoint = 2.0
DeltaWeights = 0.4
DeltaThreshold = 1.0

StaleSpecies = 15

MutateConnectionsChance = 0.25
PerturbChance = 0.90
CrossoverChance = 0.75
LinkMutationChance = 2.0
NodeMutationChance = 0.50
BiasMutationChance = 0.40
StepSize = 0.1
DisableMutationChance = 0.4
EnableMutationChance = 0.2

TimeoutConstant = 20

MaxNodes = 1000000

def getPositions():
    marioX = memory.readbyte(0x6D) * 0x100 + memory.readbyte(0x86)
    marioY = memory.readbyte(0x03B8)+16
    
    screenX = memory.readbyte(0x03AD)
    screenY = memory.readbyte(0x03B8)


def getTile(dx, dy):
    x = marioX + dx + 8
    y = marioY + dy - 16
    page = math.floor(x/256)%2

    subx = math.floor((x%256)/16)
    suby = math.floor((y - 32)/16)
    addr = 0x500 + page*13*16+suby*16+subx

    if suby >= 13 or suby < 0:
        return 0

    if memory.readbyte(addr) != 0:
        return 1
    else:
        return 0
    

def getSprites():
    sprites = []
    for slot in range(0,5):
        enemy = memory.readbyte(0xF+slot)
        if enemy != 0:
            ex = memory.readbyte(0x6E + slot)*0x100 + memory.readbyte(0x87+slot)
            ey = memory.readbyte(0xCF + slot)+24
            sprites[len(sprites)+1] = {["x"]:ex,["y"]:ey}

    return sprites

def getExtendedSprites():
        return []

def getInputs():
    getPositions()

    sprites = getSprites()
    extended = getExtendedSprites()

    local inputs = {}

    for dy=-BoxRadius*16,BoxRadius*16,16 do
        for dx=-BoxRadius*16,BoxRadius*16,16 do
            inputs[len(inputs)+1] = 0

                               tile = getTile(dx, dy)
                        if tile == 1 and marioY+dy < 0x1B0 then
                        inputs[len(inputs)] = 1
                                       end

                        for i = 1,len(sprites) do
                        distx = math.abs(sprites[i]["x"] - (marioX+dx))
                                disty = math.abs(sprites[i]["y"] - (marioY+dy))
                                if distx <= 8 and disty <= 8 then
                                inputs[len(inputs)] = -1
                                               end
                                end

                        for i = 1,len(extended) do
                        distx = math.abs(extended[i]["x"] - (marioX+dx))
                                disty = math.abs(extended[i]["y"] - (marioY+dy))
                                if distx < 8 and disty < 8 then
                                inputs[len(inputs)] = -1
                                               end
                                end
                        end
                end

        #mariovx = memory.read_s8(0x7B)
        #mariovy = memory.read_s8(0x7D)

    return inputs
end

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

def initializePool():
    pool = Pool()
    for i in range(0,Population):
        basic = Genome.basicGenome(pool)
        pool.addToSpecies(basic)
            
    initializeRun()
    return pool


pool = None
begin = True
if begin:
    pool = initializePool()
#else:
    #pool = LoadPool()

'''def savePool()
    #local filename = forms.gettext(saveLoadFile)
    writeFile(filename)
end'''

'''def loadPool()
    #local filename = forms.gettext(saveLoadFile)
    loadFile(filename)
end'''


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

complex_controls = []
recur_create(complex_controls, [], ButtonNames)
complex_controls = sorted(complex_controls, key=lambda k: len(k))

env = gym_super_mario_bros.make('SuperMarioBros-v0')
env = JoypadSpace(env, complex_controls)

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

    control_input = cal_control_input(complex_controls, pool.controller)
    state, reward, done, info = env.step(control_input)
    #joypad.write(1, pool.controller)

    getPositions()
    if marioX > rightmost then
        rightmost = marioX
        timeout = TimeoutConstant
    end

    timeout = timeout - 1


    local timeoutBonus = pool.currentFrame / 4
    if timeout + timeoutBonus <= 0 then
        local fitness = rightmost - pool.currentFrame / 2
        if gameinfo.getromname == "Super Mario World (USA)" and rightmost > 4816 then
            fitness = fitness + 1000
        end
        if gameinfo.getromname == "Super Mario Bros." and rightmost > 3186 then
            fitness = fitness + 1000
        end
        if fitness == 0 then
            fitness = -1
        end
        genome.fitness = fitness

        if fitness > pool.maxFitness then
            pool.maxFitness = fitness
            gui.text(5, 8, "Max Fitness: " .. math.floor(pool.maxFitness))
	    #forms.settext(maxFitnessLabel, "Max Fitness: " .. math.floor(pool.maxFitness))
	    writeFile("backup." .. pool.generation .. ".")
	    #writeFile("backup." .. pool.generation .. "." .. forms.gettext(saveLoadFile))
	end

    #console.writeline("Gen " .. pool.generation .. " species " .. pool.currentSpecies .. " genome " .. pool.currentGenome .. " fitness: " .. fitness)
    print("Gen", pool.generation, "species", pool.currentSpecies, "genome", pool.currentGenome, "fitness:", fitness)
    pool.currentSpecies = 1
    pool.currentGenome = 1
    while fitnessAlreadyMeasured() do
        nextGenome()
    end
    initializeRun()
    end

    local measured = 0
    local total = 0
    for _,species in pairs(pool.species) do
        for _,genome in pairs(species.genomes) do
            total = total + 1
            if genome.fitness ~= 0 then
                measured = measured + 1
            end
        end
    end
    #if not forms.ischecked(hideBanner) then
    #	gui.drawText(0, 0, "Gen " .. pool.generation .. " species " .. pool.currentSpecies .. " genome " .. pool.currentGenome .. " (" .. math.floor(measured/total*100) .. "%)", 0xFF000000, 11)
    #	gui.drawText(0, 12, "Fitness: " .. math.floor(rightmost - (pool.currentFrame) / 2 - (timeout + timeoutBonus)*2/3), 0xFF000000, 11)
    #	gui.drawText(100, 12, "Max Fitness: " .. math.floor(pool.maxFitness), 0xFF000000, 11)
    #end

    pool.currentFrame = pool.currentFrame + 1

    emu.frameadvance();
end