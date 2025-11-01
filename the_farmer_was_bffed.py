set_world_size(8)
# Write:
# till:
# 00000000
# harvest:
# 00000001
# move:
# 000001xx
# plant:
# 10000xxx
# use_item:
# 010000xx
# swap:
# 001000xx
#
#
# Read:
# first:
# 0wwpppth (water level (0-.25, .25-.5, .5-.75, .75-1), plant type, tilled state, harvestable)
# second if companion:
# 01000xxx (plant)
# third if companion:
# 1000xxxxx (X)
# fourth if companion:
# 110xxxxx (Y)
# second if measure cactus or sunflower:
# 0000xxxx (value center)
# third if measure cactus or sunflower
# 0010xxxx (value north)
# fourth if measure cactus or sunflower
# 0100xxxx (value east)
# fifth if measure cactus or sunflower
# 0110xxxx (value south)
# sixth if measure cactus or sunflower
# 1000xxxx (value west)
# second if measure pumpkin
# xxxxxxxx (counting 0 to 255 for every unique pumpkin, center)
 
def left_shift(x, n):
    return x * (2 ** n)
def right_shift(x, n):
    return x // (2 ** n)

def the_farmer_was_brainfucked(code):
    ptr = 0
    data_ptr = 0
    memory = [0]
    code_length = len(code)
    moves = {4:North,5:East,6:South,7:West}
    swap_moves = {32:North,33:East,34:South,35:West}
    plants_write = {128:Entities.Grass,129:Entities.Bush,130:Entities.Tree,131:Entities.Carrot,132:Entities.Pumpkin,133:Entities.Cactus,134:Entities.Sunflower}
    plants_read = {None:0,Entities.Grass:1,Entities.Bush:2,Entities.Tree:3,Entities.Carrot:4,Entities.Pumpkin:5,Entities.Cactus:6,Entities.Sunflower:7}
    items = {64:Items.Water,65:Items.Fertilizer,66:Items.Weird_Substance}
    plant_info = []
    info_ptr = 0
    plants_with_companions = {Entities.Grass,Entities.Bush,Entities.Tree,Entities.Carrot}
    plants_with_values = {Entities.Cactus,Entities.Sunflower}
    pumpkin_numbers = dict()
    bracket_partners = dict()
    while ptr < code_length:
        if code[ptr] == '>':
            while code[ptr] == '>':
                data_ptr += 1
                if data_ptr == len(memory):
                    memory.append(0)
                ptr += 1
        elif code[ptr] == '<':
            while code[ptr] == '<':
                data_ptr -= 1
                ptr += 1
        elif code[ptr] == '+':
            while code[ptr] == '+':
                memory[data_ptr] = memory[data_ptr] + 1
                ptr += 1
            memory[data_ptr] = memory[data_ptr] % 256
        elif code[ptr] == '-':
            while code[ptr] == '-':
                memory[data_ptr] = memory[data_ptr] - 1
                ptr += 1
            memory[data_ptr] = memory[data_ptr] % 256
        elif code[ptr] == '[':
            if memory[data_ptr] == 0:
                if code[ptr+1] == '-' and code[ptr+2] == ']':
                    memory[data_ptr] = 0
                    ptr += 2
                else:
                    if ptr in bracket_partners:
                        ptr = bracket_partners[ptr]
                    else:
                        start = ptr
                        open_brackets = 1
                        while open_brackets > 0:
                            ptr += 1
                            if code[ptr] == '[':
                                open_brackets += 1
                            elif code[ptr] == ']':
                                open_brackets -= 1
                        bracket_partners[start] = ptr
                        bracket_partners[ptr] = start
            ptr += 1
        elif code[ptr] == ']':
            if memory[data_ptr] != 0:
                if ptr in bracket_partners:
                    ptr = bracket_partners[ptr]
                else:
                    start = ptr
                    close_brackets = 1
                    while close_brackets > 0:
                        ptr -= 1
                        if code[ptr] == '[':
                            close_brackets -= 1
                        elif code[ptr] == ']':
                            close_brackets += 1
                    bracket_partners[start] = ptr
                    bracket_partners[ptr] = start
            ptr += 1
        elif code[ptr] == '.':
            #quick_print("write: ", memory[data_ptr])
            if memory[data_ptr] == 0:
                till()
                plant_info = []
                info_ptr = 0
            elif memory[data_ptr] == 1:
                harvest()
                plant_info = []
                info_ptr = 0
            elif memory[data_ptr] >= 4 and memory[data_ptr] < 8:
                move(moves[memory[data_ptr]])
                plant_info = []
                info_ptr = 0
            elif memory[data_ptr] >= 32 and memory[data_ptr] < 36:
                swap(swap_moves[memory[data_ptr]])
                plant_info = []
                info_ptr = 0
            elif memory[data_ptr] >= 64 and memory[data_ptr] < 67:
                use_item(items[memory[data_ptr]],1)
                plant_info = []
                info_ptr = 0
            elif memory[data_ptr] >= 128 and memory[data_ptr] < 135:
                plant(plants_write[memory[data_ptr]])
                plant_info = []
                info_ptr = 0
            ptr += 1
        elif code[ptr] == ',':
            if len(plant_info) == 0:
                plant_type = get_entity_type()
                water_level = get_water() * 4 // 1
                if water_level == 4:
                    water_level = 3
                tilled = 0
                if get_ground_type() == Grounds.Soil:
                    tilled = 1
                harvestable = 0
                if can_harvest():
                    harvestable = 1
                water_level_shifted = left_shift(water_level,5)
                plant_type_shifted = left_shift(plants_read[plant_type],2)
                first_byte = water_level_shifted + plant_type_shifted + left_shift(tilled,1) + harvestable
                plant_info.append(first_byte)
            elif len(plant_info) == 1:
                plant_type = get_entity_type()
                if plant_type in plants_with_companions:
                    companion, (x, y) = get_companion()
                    plant_info.append(left_shift(1,7) + plants_read[companion])
                    plant_info.append(128 + x)
                    plant_info.append(192 + y)
                elif plant_type in plants_with_values:
                    center = measure()
                    north = measure(North)
                    east = measure(East)
                    south = measure(South)
                    west = measure(West)
                    plant_info.append(center)
                    plant_info.append(32 + north)
                    plant_info.append(64 + east)
                    plant_info.append(96 + south)
                    plant_info.append(128 + west)
                elif plant_type == Entities.Pumpkin:
                    center = measure()
                    if center not in pumpkin_numbers:
                        pumpkin_numbers[center] = len(pumpkin_numbers)%256
                    plant_info.append(pumpkin_numbers[center])  
            #quick_print("Read: ", plant_info[info_ptr])
            memory[data_ptr] = plant_info[info_ptr]
            info_ptr = info_ptr + 1
            if len(plant_info) > 1 and info_ptr >= len(plant_info):
                plant_info = []
                info_ptr = 0
            ptr += 1
        

                
# simple carrot farm program in python:
#while True:
#    for x in range(8):
#        for y in range(8):
#            if get_ground_type() != Grounds.Soil:
#                till()
#                plant(Entities.Carrot)
#            elif can_harvest():
#                harvest()
#                plant(Entities.Carrot)
#            move(East)1
#        move(North)

# translated to brainfuck:

# # first generate standard outputs
# >>>>>>>                                # move to cell 7
# <[-]++++++++++++++++[>++++++++<-]>+++  # cell 7 = 128 (plant) plus 3 (carrot)
# >[-]+++++                              # cell 8 = 4 (move) plus 1 (East)
# >[-]++++                               # cell 9 = 4 (move) plus 0 (North)
# <<<                                    # go back to cell 6
# [-]+                                   # set to 1 (harvest)
# <                                      # go back to cell 5
# [-]                                    # set to 0 (till)
# <<<<<                                  # go back to 0 to start loop


# +[>++++++++[>,              # start outer infinite loop and inner 8x8 loop and read input into cell 2

# # check for value 19         #most expensive first
# >[-]>[-]<<                   # first clear helper cells
# [>+>+<<-]                    # move value to helper cells 1 and 2
# >>[<<+>>-]                   # move value back to value cell
# <-------------------         # subtract test number (19) from value cell
# [+++++++++++++++++++>-<[-]]  # if the value is not 0 revert value and pre negate the test flag
# >+                           # set flag to indicate loop
# [>>.>.<<<<<[-]>>[-]]         # print cell 6 (harvest) and 7 (plant) clear value then reset flag
# <<                           # return to value cell

# # check for value 4

# >[-]>[-]<<                   # first clear helper cells
# [>+>+<<-]                    # move value to helper cells 1 and 2
# >>[<<+>>-]                   # move value back to value cell
# <----                        # subtract test number (4) from value cell
# [++++>-1<[-]]                # if the value is not 0 revert value and pre negate the test flag
# >+                           # set flag to indicate loop
# [>.>>.<<<<<[-]>>[-]]         # print cell 5 (till) and 7 (plant) clear value then reset flag
# <<                           # return to value cell

# # check for value 5
# >[-]>[-]<<                   # first clear helper cells
# [>+>+<<-]                    # move value to helper cells 1 and 2
# >>[<<+>>-]                   # move value back to value cell
# <-----                       # subtract test number (5) from value cell
# [+++++>-1<[-]]               # if the value is not 0 revert value and pre negate the test flag
# >+                           # set flag to indicate loop
# [>.>>.<<<<<[-]>>[-]]         # print cell 5 (till) and 7 (plant) clear value then reset flag
# <<                           # return to value cell and end elif



# # Reset inner loop
# <                            # go to counter cell
# # output move east
# >>>>>>>.<<<<<<<              # output 5
# -                            # decrement counter
# ]<                           # end loop and go to outer loop

# reset outer loop
# >>>>>>>>>.<<<<<<<<<           # output 4
# ]                             # end outer infinite loop



code = ">>>>>>><[-]++++++++++++++++[>++++++++<-]>+++>[-]+++++>[-]++++<<<[-]+<[-]<<<<<+[>++++++++[>,>[-]>[-]<<[>+>+<<-]>>[<<+>>-]<-------------------[+++++++++++++++++++>-<[-]]>+[>>.>.<<<<<[-]>>[-]]<<>[-]>[-]<<[>+>+<<-]>>[<<+>>-]<----[++++>-<[-]]>+[>.>>.<<<<<[-]>>[-]]<<>[-]>[-]<<[>+>+<<-]>>[<<+>>-]<-----[+++++>-<[-]]>+[>.>>.<<<<<[-]>>[-]]<<<>>>>>>>.<<<<<<<-]<>>>>>>>>>.<<<<<<<<<]"
the_farmer_was_brainfucked(code)

