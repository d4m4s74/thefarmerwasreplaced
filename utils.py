ws = get_world_size()

def sum(seq):
    total = 0
    for v in seq:
        total += v
    return total

def sleep(ticks):
   offset = 3 # due to needed operations
   for i in range(ticks - offset):
      pass

def goto(x=0, y=0, s=ws):
    dx=(x-get_pos_x())%s
    dy=(y-get_pos_y())%s
    if dx<s//2:
        for i in range(dx):
            move(East)
    else:
        for i in range(s-dx):
            move(West)
    if dy<s//2:
        for i in range(dy):
            move(North)
    else:
        for i in range(s-dy):
            move(South)
    
def prep(ground, crop = None, fertilize = False):
    manual = []
    measurements = []
    drones = []
    goto(0,0)
    def plant_row():
        row = []
        for j in range(ws):
            if get_ground_type() != ground:
                till()
            if crop:
                harvest()
                plant(crop)
                row.append(measure())
                if fertilize:
                    use_item(Items.Fertilizer)
                if get_water() < 0.5:
                    use_item(Items.Water)
            move(East)
        return row
    for i in range(ws):
        if num_drones() == max_drones():
            manual.append((i,plant_row()))
        else:
            drones.append(spawn_drone(plant_row))
        move(North)
    for drone in drones:
        measurements.append(wait_for(drone))
    for row, values in manual:
        measurements.insert(row,values)
    return measurements
    
def goto_no_wrap(x, y): #in case I forgot to remove apple in di
    dx = (x - get_pos_x())
    dy = (y - get_pos_y()) 
    while dx > 0:
        move(East)
        dx -= 1
    while dx < 0:
        move(West)
        dx += 1
    while dy > 0:
        move(North)
        dy -= 1
    while dy < 0:
        move(South)
        dy += 1

