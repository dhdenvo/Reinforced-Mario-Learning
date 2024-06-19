import numpy as np
import sys

#File Extraction Functions

#Extracts all the bytes from the game and puts it into a numpy array
def extract_bits(filename):
    bytes = np.fromfile(filename, dtype=np.uint8)
    return np.unpackbits(bytes)

#Extract the bytes and return them in hex form
def load_hex(filename):
    game_bit_data = extract_bits(filename).reshape(-1, 8, 8)
    game_hex_data = []
    for row in game_bit_data:
        for byte in row:
            game_hex_data.append(bit_to_hex(''.join([str(i) for i in byte])))  
    return game_hex_data

#Save the hex data into binary then to a file
def save_hex(filename, hex_code):
    bit_array = []
    #print(hex_code[:10])
    for byte in hex_code:
        byte = hex_to_bit(byte)
        for bit in byte:
            bit_array.append(np.uint8(bit))
        
    bit_array = np.array(bit_array, dtype=np.uint8)
    bit_array = np.packbits(bit_array)
    bit_array.tofile(filename)


#Loads a local file and returns its contents as a text
def load_doc(filename):
    file = open(filename, 'r')
    text = file.read()
    file.close()
    return text

#Computer Language Conversion Functions

#Converts hexadecimal to binary
def hex_to_bit(hexdata):
    scale = 16
    num_of_bits = 8
    return bin(int(hexdata, scale))[2:].zfill(num_of_bits)
    
#Converts binary to decimal
def bit_to_dec(bit):
    return int(bit, 2)

#Converts binary to hexadecimal
def bit_to_hex(bit, max = 8):
    return dec_to_hex(bit_to_dec(bit))

#Converts decimal to binary
def dec_to_bit(dec):
    return "{0:b}".format(int(dec))

#Converts decimal to hexadecimal
def dec_to_hex(dec):
    return '{:02x}'.format(int(dec))

#Converts hexadecimal to decimal
def hex_to_dec(hexdata):
    return bit_to_dec(hex_to_bit(hexdata))

#Main Data Dealing Functions

#Loads the game data and puts the level data into a dictionary
def load_worlds(game_data, level_start, level_order, ending):
    curr_level = []
    levels = {}
    level_one = 0
    found = False
    
    for i, data in enumerate(game_data[level_start:]):
        curr_level.append(data)
        if data == ending:
            levels[level_order.pop(0)] = curr_level
            curr_level = []
            if not found and level_order[0] == '1-1':
                level_one = level_start + i + 1
                found = True
        if level_order == []:
            break
    return (levels, level_one)

#Load the dictionaries from the file and convert it into a usable dictionary of dictionaries
def load_dictionaries(filename):
    dictionary_file = load_doc(filename).split('\n')
    type_dictionaries = {}
    curr_dict = ''
    for line in dictionary_file:
        line = line.strip()
        if line.endswith(':'):
            curr_dict = line[:-1]
            type_dictionaries[curr_dict] = {}
        elif not line == '':
            if '-' in line:
                start = hex_to_dec(line[:line.find('-')])
                end = hex_to_dec(line[line.find('-') + 1:line.find('=')])
                for stuff in range(start, end + 1):
                    type_dictionaries[curr_dict][line[line.find('=') + 1:]] = dec_to_hex(stuff).lower()
            else:
                type_dictionaries[curr_dict][line[line.find('=') + 1:]] = line[:line.find('=')].lower()
                
    return type_dictionaries

#Go through pages and clean them up
def sort_pages(pages):
    hex_code = []
    for page in pages.values():
        page[0].append('1')
        hex_code += convert_to_hex(page[0])
        if len(page[1:]) != 0:
            for block in page[1:]:
                block.append('0')
                hex_code += convert_to_hex(block) 
    return hex_code

#Convert a block into a hex version readable for the rom file
def convert_to_hex(block):
    x = block[0] % 16
    y = block[1]
    new_page = block[3]
    block_type = block[2]
   
    new_x = dec_to_bit(x)
    while len(new_x) < 4:
        new_x = '0' + new_x 
   
    second_byte = hex_to_bit(block_type)
    second_byte = new_page + second_byte[1:]
    
    return [bit_to_hex(new_x + y), bit_to_hex(second_byte)]


#Start of Main Code

#Load original game
game_hex_data = load_hex('ROM Files/Super Mario Bros (E).nes')
        
level_order = ['1-4/6-4', '4-4', '2-4/5-4', '3-4', '7-4', '8-4', '3-3', '8-3', '4-1', '6-2', '3-1', '1-1', '1-3/5-3', '2-3/7-3', '2-1', 'Pipe', '5-1', \
               'Sky D', '4-3', '6-3', '6-1', '4-2 Warp', '8-1', '5-2', '8-2', '7-1', 'Sky N', '3-2', '1-2', '4-2', 'UG', 'UW', '2-2/7-2', '8-4 UW']

# Get the exact location of level one in the game (can remove the functionality of saving the hex since not needed)
(levels_hex, level_one_loc) = load_worlds(game_hex_data, hex_to_dec('2181'), level_order[:], 'fd') #Around 2181 (Not sure exactly)
(monsters_hex, monster_one_loc) = load_worlds(game_hex_data, hex_to_dec('1D8E'), level_order[:], 'ff') #Around 1D8E (Not sure exactly)


print(level_one_loc)
print(monster_one_loc)

#Download the generated level of the game
level_name = ""
if len(sys.argv) == 1:
    level_name = "Mario Working Level.txt"
elif len(sys.argv) == 2:
    level_name = sys.argv[1]
else:
    print("Invalid map file")
    quit()
    
try:
    gen_level = load_doc(level_name).split('\n')
except:
    print("Invalid map file")
    quit()
    
#Gather the type dictionaries from a txt file
type_dictionaries = load_dictionaries('Mario Type Dictionary.txt')
#print(type_dictionaries)

objects = []

#Go through the generated game and save only the necessary blocks
for y, row in enumerate(gen_level[:-2]):
    for x, block in enumerate(row):
        
        #Coin on top of broken block = brick
        if block == 'O' and gen_level[y - 1][x] == 'C':
            block = 'B'
        elif block == 'C' and gen_level[y + 1][x] == 'O':
            block = '-'
        #Decides the pipe hex based on the length of the pipe
        elif block == 'P' and gen_level[y - 1][x] != 'P' and gen_level[y][x - 1] != 'P':
            wall_y = y
            height = 0
            while gen_level[wall_y][x] == 'P':
                wall_y += 1
                height += 1
            block = str(69 + height)
        #Makes sure that only one piranha spawns
        elif block == 'Y' and gen_level[y][x - 1] != 'Y':
            pass  
        #If there is a wall, bullet launcher, or its base, turn it into a wall and stack it
        elif block in ['W', 'N', 'V', '|'] and not gen_level[y - 1][x] in ['W', 'N', 'V', '|']:
            pipe_y = y
            height = -1
            while gen_level[pipe_y][x] in ['W', 'N', 'V', '|']:
                pipe_y += 1
                height += 1
            block = dec_to_hex(96 + height)
        #If its a brick or broken block with something is on top of it, change the block type    
        elif (block == 'B' or block == 'O') and gen_level[y - 1][x] in ['R', '!', 'S', 'U']:
            block = gen_level[y - 1][x]
        #If the block is a question mark with a mushroom on top, make it a Q rather than a ?
        elif block == '?' and gen_level[y - 1][x] == 'R':
                block = 'Q' 
        #Possible addition to save space is combining several horizontal coins into two bytes            
        elif block == 'R' or block == 'U' or block == '!' or block == 'T' or (block == 'F' and y != 1) or block == 'M' \
             or block == 'P' or block == 'Y' or block == 'W' or block == 'S':
            block = '-'        
        
        #If the block is the top of the flag add a flag
        if block == 'F' and y == 1:
            objects.append([x, '1101', 'F'])
        #If the block isnt a background and not below a 'T' save it to the game's list
        elif block != '-' and gen_level[y - 1][x] != 'T':
            #Adjusting height of the blocks
            move = -1
            if block == 'Y':
                move = 1
            elif block == '^':
                move = -2
            elif block in type_dictionaries['Monsters']:
                move = 0
            new_y = dec_to_bit(y + move)
            
            #Making sure the y is 4 bits
            while len(new_y) < 4:
                new_y = '0' + new_y
            #Saving the block to the game's list
            objects.append([x, new_y, block])
            
#Looking at the floor checking for holes and adding them to the game's list
for x, block in enumerate(gen_level[-2]):
    if block == '-':
        objects.append([x, '1100', 'D'])
            
objects.sort()
map_length = objects[-1][0]
num_of_pages = (map_length + 15) // 16
page_ranges = {x: range(x * 16, (x + 1) * 16) for x in range(num_of_pages)}

mon_pages = {page_num: [] for page_num in range(num_of_pages)}
blo_pages = {page_num: [] for page_num in range(num_of_pages)}

#Goes through each object and checks which page they are in and whether they are monsters or a block
for (page_num, page) in page_ranges.items():
    for block in objects:
        if block[0] in page:
            if block[2] in type_dictionaries['Normal']:
                block[2] = type_dictionaries['Normal'][block[2]]
                blo_pages[page_num].append(block)
               
            elif block[2] in type_dictionaries['Monsters']:
                block[2] = type_dictionaries['Monsters'][block[2]]
                mon_pages[page_num].append(block)
                
            elif block[2].isnumeric() and int(block[2]) in range(60, 75):
                blo_pages[page_num].append(block)
                
    #Makes sure there are no empty pages
    if len(mon_pages[page_num]) == 0:
        mon_pages[page_num].append([0,'0000', '18'])
    if len(blo_pages[page_num]) == 0:
        blo_pages[page_num].append([0,'0000', '0F'])      
        
#print(mon_pages)        

#Fixes an empty page which shouldn't be there
blo_pages.pop(0)
mon_pages.pop(0)

#Adjusts the pages x coordinates from anything to below 16 and adds the page bit
mon_hex = sort_pages(mon_pages)
blo_hex = sort_pages(blo_pages)   
print(blo_pages)
print(mon_pages)

#Makes sure the page doesn't go over the allocated limit (monsters can go higher but blocks can't)
if len(mon_hex) >= 132:
    mon_hex = mon_hex[:132]
    print('Cropped Map Monsters')
if len(blo_hex) >= 255:
    print(len(blo_hex))
    print(blo_hex[254:])    
    blo_hex = blo_hex[:254]
    print('Cropped Map Blocks')
    
clean_game = load_hex('ROM Files/Super Mario Bros (E) - Editted Version.nes')

clean_game = clean_game[:monster_one_loc] + mon_hex + clean_game[monster_one_loc + len(mon_hex):]
clean_game = clean_game[:level_one_loc + 2] + blo_hex + clean_game[level_one_loc + len(blo_hex) + 2:]

save_hex('../Reinforced Mario Demo/Super Mario Bros - ' + level_name.split(".")[0] + '.nes', clean_game)
print("Created Rom File")
