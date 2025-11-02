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
# wwppppth (water level (0-.25, .25-.5, .5-.75, .75-1), plant type, tilled state, harvestable)
# second if companion:
# 00000xxx (plant)
# third if companion:
# 000xxxxx (X)
# fourth if companion:
# 000xxxxx (Y)
# second if measure cactus or sunflower:
# 0000xxxx (value center)
# third if measure cactus or sunflower
# 0000xxxx (value north)
# fourth if measure cactus or sunflower
# 0000xxxx (value east)
# fifth if measure cactus or sunflower
# 0000xxxx (value south)
# sixth if measure cactus or sunflower
# 0000xxxx (value west)
# second if measure pumpkin
# xxxxxxxx (counting 0 to 255 for every unique pumpkin, center)
# third if measure pumpkin
# xxxxxxxx (counting 0 to 255 for every unique pumpkin, north)
# fourth if measure pumpkin
# xxxxxxxx (counting 0 to 255 for every unique pumpkin, east)
# fifth if measure pumpkin
# xxxxxxxx (counting 0 to 255 for every unique pumpkin, south)
# sixth if measure pumpkin
# xxxxxxxx (counting 0 to 255 for every unique pumpkin, west)
# second if measure hedge (maze)
# 00xxxxxx (X)
# third if measure hedge (maze)
# 00xxxxxx (Y)
# fourth if measure hedge (maze)
# 0000xxxx (available moves bitmask) (North=1, East=2, South=4, West=8)
# second if measure empty tile (dinosaur)
# 0000xxxx (available moves bitmask) (North=1, East=2, South=4, West=8)

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
    plants_read = {None:0,Entities.Grass:1,Entities.Bush:2,Entities.Tree:3,Entities.Carrot:4,Entities.Pumpkin:5,Entities.Cactus:6,Entities.Sunflower:7,Entities.Dead_Pumpkin:8,Entities.Apple:9,Entities.Treasure:10,Entities.Hedge:11}
    items = {64:Items.Water,65:Items.Fertilizer,66:Items.Weird_Substance}
    plant_info = []
    info_ptr = 0
    plants_with_companions = {Entities.Grass,Entities.Bush,Entities.Tree,Entities.Carrot}
    plants_with_values = {Entities.Cactus,Entities.Sunflower}
    pumpkin_numbers = dict()
    bracket_partners = dict()
    while ptr < code_length:
        if code[ptr] == 'b':
            ptr += 1 #breakpoint
        if code[ptr] == '>':
            # hardcoded comparison because otherwise it takes a full minute
            if code[ptr+3] == '[' and code[ptr:ptr+63] == ">>>[-]>[-]<<[-]<<[>>>+<<[->>[-]>+<<<]>>[-<+>]>[-<<<+>>>]<<<-<-]":
                pos0 = 0
                pos1 = memory[data_ptr] - memory[data_ptr+1]
                if memory[data_ptr] > memory[data_ptr+1]:
                    pos3 = 1
                else:
                    pos3 = 0
                pos4 = 0
                pos5 = 0
                memory[data_ptr] = pos0
                memory[data_ptr+1] = pos1%256
                memory[data_ptr+2] = pos3
                memory[data_ptr+3] = pos4
                memory[data_ptr+4] = pos5
                ptr = ptr + 63
            else:
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
                memory[data_ptr] += 1
                ptr += 1
            memory[data_ptr] = memory[data_ptr] % 256
        elif code[ptr] == '-':
            while code[ptr] == '-':
                memory[data_ptr] -= 1
                ptr += 1
            memory[data_ptr] = memory[data_ptr] % 256
        elif code[ptr] == '[':
            if memory[data_ptr] == 0:
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
            else:
                if code[ptr+1] == '-' and code[ptr+2] == ']':
                    memory[data_ptr] = 0
                    ptr += 2
                elif code[ptr:ptr+19] == '[>+>+<<-]>>[<<+>>-]':
                    #copy value to next memory cell
                    memory[data_ptr + 1] = memory[data_ptr]
                    data_ptr += 2
                    ptr += 18
                    
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
                if plant_type == Entities.Hedge: #in mazes return chest coordinates and available moves
                    x = get_pos_x()
                    y = get_pos_y()
                    moves = 0
                    if can_move(North):
                        moves += 1
                    if can_move(East):
                        moves += 2
                    if can_move(South):
                        moves += 4
                    if can_move(West):
                        moves += 8
                    plant_info.append(left_shift(plants_read[plant_type],2))
                    plant_info.append(x)
                    plant_info.append(y)
                    plant_info.append(moves)
                elif plant_type == None: #when on an empty tile return move directions for use in dinosaur code
                    plant_info.append(0)
                    moves = 0
                    if can_move(North):
                        moves += 1
                    if can_move(East):
                        moves += 2
                    if can_move(South):
                        moves += 4
                    if can_move(West):
                        moves += 8
                    plant_info.append(moves)
                elif plant_type == Entities.Apple: #When on apple first return possible moves to emulate empty tile, then return next location
                    x, y = measure()
                    plant_info.append(left_shift(plants_read[plant_type],2))
                    moves = 0
                    if can_move(North):
                        moves += 1
                    if can_move(East):
                        moves += 2
                    if can_move(South):
                        moves += 4
                    if can_move(West):
                        moves += 8
                    plant_info.append(moves)
                    plant_info.append(x)
                    plant_info.append(y)
                else:
                    water_level = get_water() * 4 // 1
                    if water_level == 4:
                        water_level = 3
                    tilled = 0
                    if get_ground_type() == Grounds.Soil:
                        tilled = 1
                    harvestable = 0
                    if can_harvest():
                        harvestable = 1
                    water_level_shifted = left_shift(water_level,6)
                    plant_type_shifted = left_shift(plants_read[plant_type],2)
                    first_byte = water_level_shifted + plant_type_shifted + left_shift(tilled,1) + harvestable
                    plant_info.append(first_byte)
            elif len(plant_info) == 1:
                plant_type = get_entity_type()
                if plant_type in plants_with_companions:
                    companion, (x, y) = get_companion()
                    plant_info.append(plants_read[companion])
                    plant_info.append(x)
                    plant_info.append(y)
                elif plant_type in plants_with_values:
                    center = measure()
                    north = measure(North)
                    east = measure(East)
                    south = measure(South)
                    west = measure(West)
                    plant_info.append(center)
                    plant_info.append(north)
                    plant_info.append(east)
                    plant_info.append(south)
                    plant_info.append(west)
                elif plant_type == Entities.Pumpkin:
                    center = measure()
                    if center not in pumpkin_numbers:
                        pumpkin_numbers[center] = len(pumpkin_numbers)%256
                    plant_info.append(pumpkin_numbers[center])  
                    north = measure(North)
                    if north not in pumpkin_numbers:
                        pumpkin_numbers[north] = len(pumpkin_numbers)%256
                    plant_info.append(pumpkin_numbers[north])  
                    east = measure(East)
                    if east not in pumpkin_numbers:
                        pumpkin_numbers[east] = len(pumpkin_numbers)%256  
                    plant_info.append(pumpkin_numbers[east])  
                    south = measure(South)
                    if south not in pumpkin_numbers:
                        pumpkin_numbers[south] = len(pumpkin_numbers)%256  
                    plant_info.append(pumpkin_numbers[south])  
                    west = measure(West)
                    if west not in pumpkin_numbers: 
                        pumpkin_numbers[west] = len(pumpkin_numbers)%256  
                    plant_info.append(pumpkin_numbers[west])
            memory[data_ptr] = plant_info[info_ptr]
            info_ptr = info_ptr + 1
            if len(plant_info) > 1 and info_ptr >= len(plant_info):
                plant_info = []
                info_ptr = 0
            ptr += 1
        

# carrot code
#code = ">>>>>>><[-]++++++++++++++++[>++++++++<-]>+++>[-]+++++>[-]++++<<<[-]+<[-]<<<<<+[>++++++++[>,>[-]>[-]<<[>+>+<<-]>>[<<+>>-]<-------------------[>-<[-]]>+[>>.>.<<<<<[-]>>[-]]<<>[-]>[-]<<[>+>+<<-]>>[<<+>>-]<----[>-<[-]]>+[>.>>.<<<<<[-]>>[-]]<<>[-]>[-]<<[>+>+<<-]>>[<<+>>-]<-----[>-<[-]]>+[>.>>.<<<<<[-]>>[-]]<<<>>>>>>>.<<<<<<<-]<>>>>>>>>>.<<<<<<<<<]"
# cactus code
code = ">>>>>>>>>>>><[-]++++++++++++++++[>++++++++<-]>+++++>[-]+++++++++++++++++++++++++++++++++>[-]++++++++++++++++++++++++++++++++>[]+++++>[-]++++<<<<<[-]+<[-]<<<<<<<<<<>++++++++[>++++++++[>>>>>>>>.>>.>>>.<<<<<<<<<<<<<-]>>>>>>>>>>>>>>.<<<<<<<<<<<<<<<-]<+[>++++++++[>+[->>>>>>>[-]<<<<<<+++++++[>,,>,,<>>>[-]>[-]<<[-]<<[>>>+<<[->>[-]>+<<<]>>[-<+>]>[-<<<+>>>]<<<-<-]>>[>>>+>>>>.<<<<<<<[-]]>>>>>>>>>.<<<<<<<<<<<<-]>>>>>>>>>>>>.<<<<<<[<<<<<<<+>>>>>>>[-]]<<<<<<<]>>>>>>>>>>>>>>.<<<<<<<<<<<<<<<-]++++++++[>+[->>>>>>>[-]<<<<<<+++++++[>,,>,<>>>[-]>[-]<<[-]<<[>>>+<<[->>[-]>+<<<]>>[-<+>]>[-<<<+>>>]<<<-<-]>>[>>>+>>>>>.<<<<<<<<[-]]>>>>>>>>>>.<<<<<<<<<<<<<-]>>>>>>>>>>>>>.<<<<<<<[<<<<<<<+>>>>>>>[-]]<<<<<<<]>>>>>>>>>>>>>.<<<<<<<<<<<<<<-]>>>>>>>>>>.<<<<<<<<<<++++++++[>++++++++[>>>>>>>>>>.>>>.<<<<<<<<<<<<<-]>>>>>>>>>>>>>>.<<<<<<<<<<<<<<<-]<]"
the_farmer_was_brainfucked(code)

