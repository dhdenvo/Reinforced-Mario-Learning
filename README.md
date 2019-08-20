# Reinforcement Learning Mario Program

**Instalation (Ubuntu):**

git clone https://github.com/dhdenvo/Reinforced-Mario-Learning.git

sudo apt-get update
sudo apt-get install fceux

pip install pygame
pip install numpy

cd into cloned directory (Reinforced-Mario-Learning)

**Command Line General Formula:**

python DemoMain.py -game {"machine" or "create"} -name {name of rom} -gen {generation between 0 - 459 (preferred 267)}

**Command Line Presets:**

**Run Machine Learned Game:**
python DemoMain.py -game machine -gen {0 – 459}

**Create Level:**
python DemoMain.py -game create -name {any name} -gen {0 – 459}

**Load Made Level:**
python DemoMain.py -game machine -name “Super Mario Bros – {*any name}.nes” -gen {0 – 459}

\*** Make sure that the name is the same that was chosen above in the Create Level section \***

**Running Program Steps:**

1) Enter one of the preset commands above into the command line.
2) If the game option is “machine”, skip this step. If the game option is “create”, create the level you wish to use and push the create button when you are done.
3) When fceux opens, go to File>Load Lua Script and open the lua script “Reinforced Mario Demo/RunningEvolve.lua” in the repo folder.
4) Watch the emulator play for itself.
5) To skip a genome, enter the “control and enter” buttons (loads the save state at the beginning of the level). To make the program full screen enter the “alt and enter” buttons.
* On mac “control” is the “command” button and “alt” is the “control” button (I believe)
6) To close the program, close fceux and in the terminal enter the “control and C” buttons.


**NeatEvolve - Neural Network Program Origin**

The neatevolve.lua program was designed by [SethBling](https://www.youtube.com/watch?v=qv6UVOQ0F44). This code computes all the neural network sections of the project. I editted his code partially to make it work with the emulator [FCEUX](http://www.fceux.com/web/home.html) rather than [BlizHawk](http://tasvideos.org/BizHawk.html). I also editted his code in the directory "Reinforced Mario Demo" to add options for specific runs of the demo. Later on, I converted his neatevolve.lua into python to work with the python package gym-super-mario-bros. My python version uses classes to define all of the neural network aspects that were defined in SethBling's lua version. The python version can be found in the repository in the directory "Reinforcing Mario Emulator". The python version is not used in the final demo.

**Neural Network and Genetic Basics: (In Relation To This Program)**

When the program starts, generation 1 has 300 species each with 1 genome, all started off with random genes. Each run of the level is one genome. Once all of the genomes of a species run through the level, the next species is ran through. Once all the species of a generation are ran through, a new generation is started.

Each genome has its own neural network which determines the inputs for Mario based on the blocks and enemies around him. As well, each genome has specific values for their mutation rates that effect how drastically the genome mutates throughout generations. Every genome has a fitness value that is calculated based on the distance that Mario travels. Every species keeps track of its top fitness as a measure of success in comparison to other species.

Every generation, genomes crossover (two random genomes combine) and mutate (randomly change aspects of the genome) to improve the network and eventually improve the species. 
Over the generations, the species with the lowest top fitness get killed off. Also if a species becomes stale, it also gets killed off.

**Map Creator Program:**

The map creator edits the original Super Mario Bros rom file based on the map that is drawn in the gui. The program that edits the original rom file is an unorthodox way to add maps to the game, but it works to an extent. 

The game has a size limit for the map, restricting the amount of blocks and enemies in the level. Any blocks and enemies within a 10 block radius of Mario’s original starting location will not appear in the game. After the flag, some random blocks are added in randomly. This does not effect the gameplay, but it is just a weird quirk. Another small weird quirk is that some blocks may not be added in correctly. The original game was not meant to be built in a modular way where any map can be created and played.

**Backups For The Reinforcement Model:**

The universal backups that are stored in the “Reinforcement Mario Demo/Universal Backups” are all trained off of the Super Mario Bros (Machine Learned).nes rom file (the level that I made last year with machine learning). As a result, the backups are very good at playing that specific level, but not specifically trained for any random levels.

To have the models play the Super Mario Bros (Machine Learned).nes level, the best and most consistent backup is Backup – 267.txt. The 2nd species in generation 267 very consistently gets to the furthest part of level that all the other backups can get to. Backups 430+ around have gotten slightly further than this point, but not as consistently. At this point of the level, the returns from new generations are not worth the amount of time they take to run. This makes the backups at this point over trained and only work for this level. This is why the later backups for the model are not trained general programs, making the best backup to run a general program be Backup – 267 and generally any backup with a generation lower than that. 

If you want to train a model for a different level, cd into the directory “Reinforced Mario Demo”, make sure the rom file of the level is in the directory, create the directory “Backups – {Rom Filename}”, and run the command:

python RunDemoMain.py -rom {Rom Filename} -gen 0 -uni False -create True
