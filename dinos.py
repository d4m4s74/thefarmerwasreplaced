from utils import goto_no_wrap, sum

global apples
apples = []



def goto_no_wrap_measure(x, y, apple=None):
    if apple:
        if x != apple[0] and y != apple[1]:
            goto_no_wrap(x,y)
            return 0, None
        next = None
        found = 0
        minx = min(x, get_pos_x())
        maxx = max(x, get_pos_x())
        miny = min(y, get_pos_y())
        maxy = max(y, get_pos_y())
        if x == get_pos_x() and y == get_pos_y():
            m = measure()
            if m:
                next = m
            return found, next
        elif apple == (x,y):
            before = (get_pos_x(), get_pos_y())
            goto_no_wrap(x, y)
            if before == (get_pos_x(), get_pos_y()):
                return found, next
            m = measure()
            if m:
                found += 1
                next = m
            return found, next
        elif (apple[0] == x and apple[1] >= miny and apple[1] <= maxy) or (apple[1] == y and apple[0] >= minx and apple[0] <= maxx):
            while (apple[0] == x and apple[1] >= miny and apple[1] <= maxy) or (apple[1] == y and apple[0] >= minx and apple[0] <= maxx):
                if apple == (x,y):
                    goto_no_wrap(x, y)
                    m = measure()
                    if m:
                        found += 1
                        next = m
                    return found, next
                before = (get_pos_x(), get_pos_y())
                goto_no_wrap(apple[0], apple[1])
                if before == (get_pos_x(), get_pos_y()):
                    return found, next
                m = measure()
                if m:
                    found += 1
                    next = m
                    apple = m
            if x == get_pos_x() and y == get_pos_y():
                return found, next
            else:
                goto_no_wrap(x,y)
            return found, next
        else:
            goto_no_wrap(x,y)
            return 0, apple
    else:
        x_pos = get_pos_x()
        y_pos = get_pos_y()
        dx = (x - x_pos)
        dy = (y - y_pos) 
        found = 0
        next = None
        while dx > 0:
            m = measure()
            if m:
                found += 1
                next = m
                nfound, next = goto_no_wrap_measure(x, y, next)
                found += nfound
                return found, next
            move(East)
            dx -= 1
        while dx < 0:
            m = measure()
            if m:
                found += 1
                next = m
                nfound, next = goto_no_wrap_measure(x, y, next)
                found += nfound
                return found, next
            move(West)
            dx += 1
        while dy > 0:
            m = measure()
            if m:
                found += 1
                next = m    
                nfound, next = goto_no_wrap_measure(x, y, next)
                found += nfound
                return found, next
            move(North)
            dy -= 1
        while dy < 0:
            m = measure()
            if m:
                found += 1
                next = m
                nfound, next = goto_no_wrap_measure(x, y, next)
                found += nfound
                return found, next
            move(South)
            dy += 1
        m = measure()
        if m:
            found += 1
            next = m
            nfound, next = goto_no_wrap_measure(x, y, next)
            found += nfound
            return found, next
        return found, next

def attempt_goto_no_wrap(x,y):
    goto_no_wrap(x,y)
    return get_pos_x() == x and get_pos_y() == y

    
def attempt_goto_no_wrap_measure(x,y, apple=None):
    found, next = goto_no_wrap_measure(x,y, apple)
    return get_pos_x() == x and get_pos_y() == y, found, next


def check_can_move():
    return can_move(East) or can_move(North) or can_move(West) or can_move(South)


ws = get_world_size()
#threshold = ws * 3
def next_direction(direction):
    if direction == East:
        return North
    elif direction == North:
        return West
    elif direction == West:
        return South
    else:
        return East
def dinos(num, timing=True):
    #start_time = get_time()
    global apples
    apples = []
    found = 0
    ws = get_world_size()
    clear()
    change_hat(Hats.Dinosaur_Hat)
    apple = measure()
    #apples.append(apple)

    # timing instrumentation (optional)
    #if timing:
    #    stats = []
    #    prev_apple_count = 0
    #    last_time = get_time()
    #    # event markers for thresholds (label, time, apples_collected)
    #    events = []
    #else:
    #    stats = None
    #    prev_apple_count = 0
    #    last_time = 0.0
    #    events = None

    def _check_apple_times(prev_count, last_t, stats_list):
        # consume any newly appended apples and record deltas
        while len(apples) > prev_count:
            t = get_time()
            stats_list.append(t - last_t)
            last_t = t
            prev_count += 1
        return prev_count, last_t, stats_list

    # small helper to consistently apply goto_no_wrap_measure results
    def _apply_goto_result(dino_length, apple, found_cnt, nxt):
        if found_cnt:
            dino_length += found_cnt
        # prefer explicit returned next; record it, otherwise fallback to measure() and record
        if nxt:
            apple = nxt
            # avoid duplicate consecutive entries
            #if apples[-1] != nxt:
            #    apples.append(nxt)
        else:
            m = measure()
            if m:
                apple = m
                #if apples[-1] != m:
                #    apples.append(m)
        return dino_length, apple

    #def manhattan_distance(a, b):
    #    return abs(a[0] - b[0]) + abs(a[1] - b[1])
   # 
   # def get_possible_moves():
   #     possible_moves = []
   #     if can_move(North):
   #         possible_moves.append(North)
   #     if can_move(East):
   #         possible_moves.append(East)
   #     if can_move(South):
   #         possible_moves.append(South)
   #     if can_move(West):
   #         possible_moves.append(West)
   #     return possible_moves
    
#    def save_yourself():
#        possible_moves = get_possible_moves()
#        success = False
#        found = 0
#        next = None
#        if East in possible_moves:
#            success = attempt_goto_no_wrap(ws-1, get_pos_y())
#            if success:
#                found, next = goto_no_wrap_measure(ws-1, ws-1)
#        elif not success and North in possible_moves:
#            success = attempt_goto_no_wrap(get_pos_x(), ws-1)
#            if success:
#                found, next = goto_no_wrap_measure(0, ws-1)
#        elif not success and West in possible_moves:
#            success = attempt_goto_no_wrap(0, get_pos_y())
#            if success:
#                found, next = goto_no_wrap_measure(0,0)
#        elif not success and South in possible_moves:
#            success = attempt_goto_no_wrap(get_pos_x(), 0)
#            if success:
#                found, next = goto_no_wrap_measure(ws-1,0)
#        return found, next
    
#    def find_lost_apple():
#        found, next = goto_no_wrap_measure(0,0)
#        if found:
#            return found, next
#        while not found:
#            if get_pos_y() == ws-1:
#                found, next = goto_no_wrap_measure(ws-1,ws-1)
#                if next:
#                    return found, next
#                found, next = goto_no_wrap_measure(0,0)
#                if next:
#                    return found, next
#            found, next = goto_no_wrap_measure(ws-1, get_pos_y())
#            if next:
#                return found, next
#            move(North)
#            next = measure()
#            if next:
#                found += 1
#                apples.append(next)
#                return found, next
#
#            found, next = goto_no_wrap_measure(1, get_pos_y())
#            if next:
#                found += 1
#                apples.append(next)
#                return found, next
#            move(North)
#            next = measure()
#            if next:
#                found += 1
#                apples.append(next)
#            
#        return found, next



    while num_items(Items.Bone) <num:
        found = 0
        dino_length = 1
        hamiltonian_switch_threshold = ws*2.84375 // 1 #optimized based on testing: 91 for 32x32
        #hamiltonian_switch_threshold = ws*2.53125 // 1 #back to 81 for leaderboard testing

        corner_threshold_following_wall = ws-1 // 1
        corner_threshold_leaving_wall = ws/2 + ws*0.375 // 1  # Threshold 28 formula: high performance edge collection
        # Pre-calculate inverted thresholds used in loops
        inverted_corner_threshold_following_wall = ws - corner_threshold_following_wall
        inverted_corner_threshold_leaving_wall = ws - corner_threshold_leaving_wall
        # Pre-calculate wall boundaries used frequently in loops
        max_wall = ws - 1
        # Pre-calculate hamiltonian shortcut positions
        inner_edge_right = ws - 2  # Used for shortcut movements from left side
    
        #if timing:
        #    print("Running with corner_threshold_leaving_wall at " + str(corner_threshold_leaving_wall))

        while dino_length < hamiltonian_switch_threshold:
            # ensure apple is valid before indexing
            #if timing:
            #    prev_apple_count, last_time, stats = _check_apple_times(prev_apple_count, last_time, stats)
                    
            # Bottom edge section
            if get_pos_y() == 0:
                while get_pos_x() != max_wall:
                    if dino_length > hamiltonian_switch_threshold or apple[0] < inverted_corner_threshold_following_wall or apple[1] > corner_threshold_leaving_wall: #If the apple is outside the threshold
                        #Just go to next section
                        if apple[1] == 0:
                            found, next = goto_no_wrap_measure(max_wall, 0, apple)
                            dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                        goto_no_wrap(max_wall, 0)
                    else:
                        while apple[0] >= get_pos_x() and apple[1] < corner_threshold_leaving_wall and apple[0] != max_wall: #While the apple is inside the threshold and at same x as or east from the drone
                            if get_pos_y() == apple[1]: #If you're at the same height as the apple, move towards it
                                success, found, next = attempt_goto_no_wrap_measure(apple[0],apple[1],apple)
                                dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                                if not success: #If you can't move towards the apple it's encircled by the tail. Go to the end of the section.
                                    goto_no_wrap(get_pos_x(), 0)
                                    goto_no_wrap(0, 0)
                                    break
                            elif get_pos_x() == apple[0] and apple[0] != max_wall: #If we're above or below the apple. move towards it:
                                success, found, next = attempt_goto_no_wrap_measure(get_pos_x(),apple[1],apple) #try to move to the same y coordinate as the apple
                                dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                                if not success: #If that fails the apple isn encircled. End the section.
                                    success2, found, next = attempt_goto_no_wrap_measure(max_wall, get_pos_y(), apple) #try to cut the corner
                                    dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                                    if not success2:
                                        goto_no_wrap(get_pos_x(),0) #if it fails go down and right
                                        goto_no_wrap(max_wall, 0)
                                    break
                            elif apple[0] != max_wall: #try to move to the same X coordinate as the apple
                                if get_pos_y() != apple[1]:
                                    success = attempt_goto_no_wrap(apple[0], get_pos_y())
                                    if not success:
                                        if apple[1] < get_pos_y(): #If the apple is below, go down to it and try again:
                                            found, next = goto_no_wrap_measure(get_pos_x(), apple[1], apple)
                                        else: #If apple is above it's encircled by the tail. Go to the end of the section.
                                            goto_no_wrap(get_pos_x(), 0)
                                            goto_no_wrap(0, 0)
                                            break
                                else:
                                    success, found, next = attempt_goto_no_wrap_measure(apple[0],get_pos_y(),apple) 
                                    dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                                    if not success: #If you can't reach, there is a tail blocking the way
                                        if apple[1] < get_pos_y(): #If the apple is below, go down to it and try again:
                                            found, next = goto_no_wrap_measure(get_pos_x(), apple[1], apple)
                                        else: #If apple is above it's encircled by the tail. Go to the end of the section.
                                            goto_no_wrap(get_pos_x(), 0)
                                            goto_no_wrap(0, 0)
                                            break
                        #after the while go to the final edge
                        success, found, next = attempt_goto_no_wrap_measure(max_wall,get_pos_y(),apple) #Try to move to the next edge
                        dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                        if not success: #if we can't. Go down and right.
                            goto_no_wrap(get_pos_x(),0)
                            goto_no_wrap(max_wall, 0)
                            dino_length, apple = _apply_goto_result(dino_length, apple, found, next)

            
         
                    
            # Right edge section
            if get_pos_x() == max_wall:
                while get_pos_y() != max_wall:
                    if apple[0] < inverted_corner_threshold_leaving_wall or apple[1] < inverted_corner_threshold_following_wall: #If the apple is outside the threshold
                        #Just go to next section
                        if apple[0] == max_wall:
                            found, next = goto_no_wrap_measure(max_wall,max_wall, apple)
                            dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                        goto_no_wrap(max_wall,max_wall)
                    else:
                        while apple[1] >= get_pos_y() and apple[0] > inverted_corner_threshold_leaving_wall and apple[1] != max_wall: #while the apple is inside the threshold or at the xame y or above the drone
                            if get_pos_x() == apple[0]: #If you're in the same column as the apple move towards it
                                success, found, next = attempt_goto_no_wrap_measure(apple[0],apple[1],apple)
                                dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                                if not success: #If you can't move towards the apple it's encircled by the tail. Go to the end of the section.
                                    goto_no_wrap(0, get_pos_y())
                                    goto_no_wrap(0, max_wall)
                                    break
                            elif get_pos_y() == apple[1] and apple[1] != max_wall: #If we're left or right of the apple, move towards it.
                                success, found, next = attempt_goto_no_wrap_measure(apple[0],get_pos_y(),apple) #try to move to the same y coordinate as the apple
                                dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                                if not success: #If that fails the apple isn encircled. End the section.
                                    success2, found, next = attempt_goto_no_wrap_measure(get_pos_x(), max_wall, apple) #try to cut the corner
                                    dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                                    if not success2:
                                        goto_no_wrap(max_wall, get_pos_y()) #if it fails go right and up
                                        goto_no_wrap(max_wall, max_wall)
                                    break
                            elif apple[1] != max_wall: #try to move to the same Y coordinate as the apple
                                if get_pos_x() != apple[0]:
                                    success = attempt_goto_no_wrap(get_pos_x(), apple[1])
                                    if not success:
                                        if apple[0] < get_pos_x(): #If the apple is left, go left to it and try again:
                                            found, next = goto_no_wrap_measure(apple[0], get_pos_y(), apple)
                                            dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                                        else: #If apple is right it's encircled by the tail. Go to the end of the section.
                                            goto_no_wrap(max_wall, get_pos_y())
                                            goto_no_wrap(max_wall, max_wall)
                                            break
                                else:
                                    success, found, next = attempt_goto_no_wrap_measure(get_pos_x(),apple[1],apple) 
                                    dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                                    if not success: #If you can't reach, there is a tail blocking the way
                                            if apple[0] > get_pos_x(): #If the apple is right, go right to it and try again:
                                                found, next = goto_no_wrap_measure(apple[0], get_pos_y(), apple)
                                                dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                                            else: #If apple is below it's encircled by the tail. Go to the end of the section.
                                                goto_no_wrap(max_wall, get_pos_y())
                                                goto_no_wrap(max_wall, max_wall)
                                                break
                        #after the while go to the final edge
                        success, found, next = attempt_goto_no_wrap_measure(get_pos_x(),max_wall,apple) #Try to move to the next edge
                        dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                        if not success: #if we can't. Go down and right.
                            goto_no_wrap(max_wall, get_pos_y())
                            goto_no_wrap(max_wall, max_wall)

            # Top edge section
            if get_pos_y() == max_wall:
                while get_pos_x() != 0:
                    if apple[0] > corner_threshold_following_wall or apple[1] < inverted_corner_threshold_leaving_wall: #If the apple is outside the threshold
                        if apple[1] == max_wall:
                            found, next = goto_no_wrap_measure(0,max_wall, apple)
                            dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                        #Just go to next section
                        goto_no_wrap(0,max_wall)
                    else:
                        while apple[0] <= get_pos_x() and apple[1] > inverted_corner_threshold_leaving_wall and apple[0] != 0: #While the apple is inside the threshold and at same x as or west from the drone
                            if get_pos_y() == apple[1]: #If you're at the same height as the apple, move towards it
                                success, found, next = attempt_goto_no_wrap_measure(apple[0],apple[1],apple)
                                dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                                if not success: #If you can't move towards the apple it's encircled by the tail. Go to the end of the section.
                                    goto_no_wrap(get_pos_x(), max_wall)
                                    goto_no_wrap(max_wall, max_wall)
                                    break
                            elif get_pos_x() == apple[0] and apple[0] != 0: #If we're above or below the apple. move towards it:
                                success, found, next = attempt_goto_no_wrap_measure(get_pos_x(),apple[1],apple) #try to move to the same y coordinate as the apple
                                dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                                if not success: #If that fails the apple isn encircled. End the section.
                                    success2, found, next = attempt_goto_no_wrap_measure(0, get_pos_y(), apple) #try to cut the corner
                                    dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                                    if not success2:
                                        goto_no_wrap(get_pos_x(),max_wall) #if it fails go down and right
                                        goto_no_wrap(0, max_wall)
                                    break
                            elif apple[0] != 0: #try to move to the same X coordinate as the apple
                                if get_pos_y() != apple[1]:
                                    success = attempt_goto_no_wrap(apple[0], get_pos_y())
                                    if not success:
                                        if apple[1] > get_pos_y(): #If the apple is above, go up to it and try again:
                                            found, next = goto_no_wrap_measure(get_pos_x(), apple[1], apple)
                                        else: #If apple is below it's encircled by the tail. Go to the end of the section.
                                            goto_no_wrap(get_pos_x(), max_wall)
                                            goto_no_wrap(0, max_wall)
                                            break
                                else:
                                    success, found, next = attempt_goto_no_wrap_measure(apple[0],get_pos_y(),apple) 
                                    dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                                    if not success: #If you can't reach, there is a tail blocking the way
                                        if apple[1] > get_pos_y(): #If the apple is above, go up to it and try again:
                                            found, next = goto_no_wrap_measure(get_pos_x(), apple[1], apple)
                                            dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                                        else: #If apple is below it's encircled by the tail. Go to the end of the section.
                                            goto_no_wrap(get_pos_x(), max_wall)
                                            goto_no_wrap(0, max_wall)
                                            break
                        #after the while go to the final edge
                        success, found, next = attempt_goto_no_wrap_measure(0,get_pos_y(),apple) #Try to move to the next edge
                        dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                        if not success: #if we can't. Go down and right.
                            goto_no_wrap(get_pos_x(),max_wall)
                            goto_no_wrap(0, max_wall)
            
            # Left edge section
            if get_pos_x() == 0:
                while get_pos_y() != 0:
                    if apple[0] > corner_threshold_leaving_wall or apple[1] > corner_threshold_following_wall: #If the apple is outside the threshold
                        #Just go to next section
                        if apple[0] == 0:
                            found, next = goto_no_wrap_measure(0,0, apple)
                            dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                        goto_no_wrap(0,0)
                    else:
                        while apple[1] <= get_pos_y() and apple[0] < corner_threshold_leaving_wall and apple[1] != 0: #while the apple is inside the threshold or at the xame y or above the drone
                            if get_pos_x() == apple[0]: #If you're in the same column as the apple move towards it
                                success, found, next = attempt_goto_no_wrap_measure(apple[0],apple[1],apple)
                                dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                                if not success: #If you can't move towards the apple it's encircled by the tail. Go to the end of the section.
                                    goto_no_wrap(0, get_pos_y())
                                    goto_no_wrap(0, 0)
                                    break
                            elif get_pos_y() == apple[1] and apple[1] != 0: #If we're left or right of the apple, move towards it
                                success, found, next = attempt_goto_no_wrap_measure(apple[0],get_pos_y(),apple) #try to move to the same y coordinate as the apple
                                dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                                if not success: #If that fails the apple isn encircled. End the section.
                                    success2, found, next = attempt_goto_no_wrap_measure(get_pos_x(), 0, apple) #try to cut the corner
                                    dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                                    if not success2:
                                        goto_no_wrap(0, get_pos_y()) #if it fails go left and down
                                        goto_no_wrap(0, 0)
                                    break
                            elif apple[1] != 0: #try to move to the same Y coordinate as the apple
                                if get_pos_x() != apple[0]:
                                    success = attempt_goto_no_wrap(get_pos_x(), apple[1]) 
                                    if not success:
                                        if apple[0] > get_pos_x(): #If the apple is right, go right to it and try again:
                                            found, next = goto_no_wrap_measure(apple[0], get_pos_y(), apple)
                                            dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                                        else: #If apple is left it's encircled by the tail. Go to the end of the section.
                                            goto_no_wrap(0, get_pos_y())
                                            goto_no_wrap(0, 0)
                                            break
                                else:
                                    success, found, next = attempt_goto_no_wrap_measure(get_pos_x(),apple[1],apple) 
                                    dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                                    if not success: #If you can't reach, there is a tail blocking the way
                                        if apple[0] < get_pos_x(): #If the apple is left, go right to it and try again:
                                            found, next = goto_no_wrap_measure(apple[0], get_pos_y(), apple)
                                            dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                                        else: #If apple is below it's encircled by the tail. Go to the end of the section.
                                            goto_no_wrap(0, get_pos_y())
                                            goto_no_wrap(0,0)
                                            break
                    #after the while go to the final edge
                    success, found, next = attempt_goto_no_wrap_measure(get_pos_x(),0,apple) #Try to move to the next edge
                    dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                    if not success: #if we can't. Go down and right.
                        goto_no_wrap(0, get_pos_y())
                        goto_no_wrap(0, 0)

        # If the dino it too long to circle, switch to hamiltonian with shortcuts
        # First do one half loop to avoid getting stuck on the earlier shortcuts
        #found, next = goto_no_wrap_measure(ws-1, 0, apple)
        #dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
        #found, next = goto_no_wrap_measure(ws-1, ws-1, apple)
        #dino_length, apple = _apply_goto_result(dino_length, apple, found, next)    
        threshold_multiplier =  ws/2-1  #8 + (random() * 12)
        no_south_shortcuts = False
        no_shortcuts_threshold = 1024 - 31*threshold_multiplier # attempt when 8 lines remaining
        no_north_shortcuts = False
        no_switching_sides = False
        skipped = 0
        #if timing:
        #    events.append(("Start hamiltonian loop at threshold " + str(hamiltonian_switch_threshold) + " with switching threshold at " + str(threshold_multiplier), get_time() - start_time, 0))
        while check_can_move():
            #outline. written at 5 am:
            #two separate functions or loops. North loop and south loop
            #quick example code: 
            #while x != 0 and y != ws-1:
            #things moving north
            #while x != ws - 1 and y != 0:
            #things moving south
            #
            # Even east to west
            # odd west to east
            # no collisions possible.
            # Move of edge of center, check if you can move. Otherwise follow path in named direction
            # No AI suggestions past this point
            if (not no_south_shortcuts) and dino_length > no_shortcuts_threshold: 
                #if timing:
                #    events.append(("Disabling shortcuts at " + str(threshold_multiplier) + " rows", get_time() - start_time, 0))
                no_south_shortcuts = True
                no_north_shortcuts = True
                no_switching_sides = True
            

            if get_pos_y() == 0:
                found, next = goto_no_wrap_measure(max_wall, get_pos_y(), apple)
                dino_length, apple = _apply_goto_result(dino_length, apple, found, next)

            left_shortcut_failed = False
            while get_pos_x() != 0 and get_pos_y() != max_wall:
                north_shortcut_failed = False
                if not no_north_shortcuts:
                    if apple[0] != 0 and apple[1] %2 == 1 and apple[1] > get_pos_y():
                        #go to odd point next to odd apple
                        found, next = goto_no_wrap_measure(get_pos_x(),apple[1], apple)
                        dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                        if not get_pos_y() == apple[1]:
                            north_shortcut_failed = True
                        else:
                            if apple[0] == max_wall: #if we're already there, we're done
                                m = measure()
                                dino_length, apple = _apply_goto_result(dino_length, apple, 1, m)
                                continue
                            else:
                                found, next = goto_no_wrap_measure(apple[0], apple[1], apple) #go to apple
                                dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                            if apple[1] <= get_pos_y(): #if the next one spawned in line or down, move all the way west
                                found, next = goto_no_wrap_measure(1,get_pos_y(), apple)
                                dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                                if not no_switching_sides and get_pos_x() == 1 and can_move(West): #try a shortcut
                                    move(West)
                                    m = measure()
                                    if m:
                                        dino_length, apple = _apply_goto_result(dino_length, apple, 1, m)
                                    break
                                else:
                                    left_shortcut_failed = True #otherwise standard movement
                                    move(North)
                                    m = measure()
                                    if m:
                                        dino_length, apple = _apply_goto_result(dino_length, apple, 1, m)
                                    found, next = goto_no_wrap_measure(max_wall,get_pos_y(), apple)
                                    dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                                    move(North)
                                    m = measure()
                                    if m:
                                        dino_length, apple = _apply_goto_result(dino_length, apple, 1, m)

                    elif get_pos_x() == max_wall and apple[0] != 0 and apple[1] %2 == 0 and apple[1]-1 > get_pos_y():
                        #go to odd point closest to even apple.
                        found, next = goto_no_wrap_measure(get_pos_x(),apple[1]-1, apple)
                        dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                        if not get_pos_y() == apple[1]-1:
                            north_shortcut_failed = True
                        else:

                            found, next = goto_no_wrap_measure(apple[0], get_pos_y(), apple) #go to apple X, no measuring necessary
                            dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                            move(North)
                            m = measure()
                            if m:
                                dino_length, apple = _apply_goto_result(dino_length, apple, 1, m)
                            found, next = goto_no_wrap_measure(max_wall,get_pos_y(), apple) #go back east
                            dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                            move(North)
                            m = measure()
                            if m:
                                dino_length, apple = _apply_goto_result(dino_length, apple, 1, m)
                    elif get_pos_x() == max_wall and get_pos_y() != max_wall and north_shortcut_failed: #If we can't go up we do one normal movement
                        found, next = goto_no_wrap_measure(1,get_pos_y(), apple)
                        dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                        move(North)
                        m = measure()
                        if m:
                            dino_length, apple = _apply_goto_result(dino_length, apple, 1, m)
                        found, next = goto_no_wrap_measure(max_wall,get_pos_y(), apple)
                        dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                        move(North)
                        m = measure()
                        if m:
                            dino_length, apple = _apply_goto_result(dino_length, apple, 1, m)
                    elif not no_switching_sides and get_pos_x() == max_wall and apple[1] < get_pos_y():  #try a left shortcut if apple is south
                        found, next = goto_no_wrap_measure(1, get_pos_y(), apple)
                        dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                        if can_move(West):
                            move(West)
                            m = measure()
                            if m:
                                dino_length, apple = _apply_goto_result(dino_length, apple, 1, m)
                            move(South)
                            m = measure()
                            if m:
                                dino_length, apple = _apply_goto_result(dino_length, apple, 1, m)
                            break
                        else:
                            left_shortcut_failed = True #switch to standard movement
                            move(North)
                            m = measure()
                            if m:
                                dino_length, apple = _apply_goto_result(dino_length, apple, 1, m)
                            found, next = goto_no_wrap_measure(max_wall, get_pos_y(), apple)
                            dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                            move(North)
                            m = measure()
                            if m:
                                dino_length, apple = _apply_goto_result(dino_length, apple, 1, m)

                    if get_pos_x() == max_wall and left_shortcut_failed:
                        found, next = goto_no_wrap_measure(max_wall,max_wall, apple)
                        dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                        if get_pos_y() == max_wall:
                            break
                #normal left/right movement
                if not check_can_move():
                    break
                if get_pos_y() % 2 == 0:
                    move(North)
                    m = measure()
                    if m:
                        dino_length, apple = _apply_goto_result(dino_length, apple, 1, m)
                if get_pos_y() == max_wall: #switch to the south loop
                    found, next = goto_no_wrap_measure(0, max_wall, apple)
                    dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                    move(South)
                    m = measure()
                    if m:
                        dino_length, apple = _apply_goto_result(dino_length, apple, 1, m)
                    break
                found, next = goto_no_wrap_measure(1,get_pos_y(), apple)
                dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                move(North)
                m = measure()
                if m:
                    dino_length, apple = _apply_goto_result(dino_length, apple, 1, m)
                found, next = goto_no_wrap_measure(max_wall,get_pos_y(), apple)
                dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                move(North)
                m = measure()
                if m:
                    dino_length, apple = _apply_goto_result(dino_length, apple, 1, m)
            if get_pos_y() == max_wall: #switch to the south loop
                found, next = goto_no_wrap_measure(0, max_wall, apple)
                dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                move(South)
                m = measure()
                if m:
                    dino_length, apple = _apply_goto_result(dino_length, apple, 1, m)

            right_shortcut_failed = False

            while get_pos_x() != max_wall and get_pos_y() != 0:
                south_shortcut_failed = False
                if not no_south_shortcuts:
                    if get_pos_x() == 0 and apple[0] != max_wall and apple[1] != 0 and apple[1] %2 == 0 and apple[1] < get_pos_y():
                        #go to even point next to even apple
                        found, next = goto_no_wrap_measure(get_pos_x(),apple[1], apple)
                        dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                        if not get_pos_y() == apple[1]:
                            south_shortcut_failed = True
                        else:
                            if apple[0] == 0: #if we're already there, we're done
                                m = measure()
                                dino_length, apple = _apply_goto_result(dino_length, apple, 1, m)
                                continue
                            else:
                                found, next = goto_no_wrap_measure(apple[0], apple[1], apple) #go to apple
                                dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                            if apple[1] >= get_pos_y(): #if the next one spawned in line or up, move all the way east
                                found, next = goto_no_wrap_measure(inner_edge_right,get_pos_y(), apple)
                                dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                                if not no_switching_sides and can_move(East): #try a shortcut
                                    move(East)
                                    m = measure()
                                    if m:
                                        dino_length, apple = _apply_goto_result(dino_length, apple, 1, m)
                                    break
                                else:
                                    right_shortcut_failed = True #otherwise standard movement
                                    move(South)
                                    m = measure()
                                    if m:
                                        dino_length, apple = _apply_goto_result(dino_length, apple, 1, m)
                                    found, next = goto_no_wrap_measure(0,get_pos_y(), apple)
                                    dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                                    move(South)
                                    m = measure()
                                    if m:
                                        dino_length, apple = _apply_goto_result(dino_length, apple, 1, m)

                    elif get_pos_x() == 0 and apple[0] != max_wall and apple[1] != 0 and apple[1] %2 == 1 and apple[1]+1 < get_pos_y():
                        #go to even point closest to odd apple.
                        found, next = goto_no_wrap_measure(get_pos_x(),apple[1]+1, apple)
                        dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                        if not get_pos_y() == apple[1]+1:
                            south_shortcut_failed = True
                        else:
                            if apple[0] == 0: #if we're already there, we're done
                                m = measure()
                                dino_length, apple = _apply_goto_result(dino_length, apple, 1, m)
                                continue
                            else:
                                found, next = goto_no_wrap_measure(apple[0], get_pos_y(), apple)
                                dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                                move(South)
                                m = measure()
                                if m:
                                    dino_length, apple = _apply_goto_result(dino_length, apple, 1, m)
                                found, next = goto_no_wrap_measure(0,get_pos_y(), apple) #go back west
                                dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                                move(South)
                                m = measure()
                                if m:
                                    dino_length, apple = _apply_goto_result(dino_length, apple, 1, m)
                    elif get_pos_x() == 0 and get_pos_y() != 0 and south_shortcut_failed: #If we can't go down we do one normal movement
                        found, next = goto_no_wrap_measure(inner_edge_right,get_pos_y(), apple)
                        dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                        move(South)
                        m = measure()
                        if m:
                            dino_length, apple = _apply_goto_result(dino_length, apple, 1, m)
                        found, next = goto_no_wrap_measure(0,get_pos_y(), apple)
                        dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                        move(South)
                        m = measure()
                        if m:
                            dino_length, apple = _apply_goto_result(dino_length, apple, 1, m)
                    elif not no_switching_sides and get_pos_x() == 0 and apple[1] > get_pos_y():  #try a right shortcut if apple is north
                        found, next = goto_no_wrap_measure(inner_edge_right, get_pos_y(), apple)
                        dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                        if can_move(East):
                            move(East)
                            m = measure()
                            if m:
                                dino_length, apple = _apply_goto_result(dino_length, apple, 1, m)
                            move(North)
                            m = measure()
                            if m:
                                dino_length, apple = _apply_goto_result(dino_length, apple, 1, m)
                            break
                        else:
                            right_shortcut_failed = True #switch to standard movement
                            move(South)
                            m = measure()
                            if m:
                                dino_length, apple = _apply_goto_result(dino_length, apple, 1, m)
                            found, next = goto_no_wrap_measure(0,get_pos_y(), apple)
                            dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                            move(South)
                            m = measure()
                            if m:
                                dino_length, apple = _apply_goto_result(dino_length, apple, 1, m)
                    if get_pos_x() == 0 and right_shortcut_failed:
                        found, next = goto_no_wrap_measure(0, 0, apple)
                        dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                        if get_pos_y() == 0:
                            break
                #normal right/left movement
                if not check_can_move():
                    break
                
                if get_pos_y() % 2 == 1:
                    move(South)
                    m = measure()
                    if m:
                        dino_length, apple = _apply_goto_result(dino_length, apple, 1, m)
                if get_pos_y() == 0: #switch to the north loop
                    found, next = goto_no_wrap_measure(0, max_wall, apple)
                    dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                    move(North)
                    m = measure()
                    if m:
                        dino_length, apple = _apply_goto_result(dino_length, apple, 1, m)
                    break
                found, next = goto_no_wrap_measure(inner_edge_right,get_pos_y(), apple)
                dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                move(South)
                m = measure()
                if m:
                    dino_length, apple = _apply_goto_result(dino_length, apple, 1, m)
                found, next = goto_no_wrap_measure(0,get_pos_y(), apple)
                dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                move(South)
                m = measure()
                if m:
                    dino_length, apple = _apply_goto_result(dino_length, apple, 1, m)
            if get_pos_y() == 0: #switch to the north loop
                found, next = goto_no_wrap_measure(0, max_wall, apple)
                dino_length, apple = _apply_goto_result(dino_length, apple, found, next)
                move(North)
                m = measure()
                if m:
                    dino_length, apple = _apply_goto_result(dino_length, apple, 1, m)

        change_hat(Hats.Straw_Hat)
        # print timing summary before exiting dinos() loop
        # final flush of any remaining appended apples
        #if timing:
        #    #prev_apple_count, last_time, stats = _check_apple_times(prev_apple_count, last_time, stats)
        #    # print threshold event timeline and timing summary (only when enabled)
        #    if timing:
        #        if events:
        #            for ev in events:
        #                quick_print("EVENT", ev[0], "time=", ev[1], "apples=", ev[2])
        #        if stats:
        #            # assume every timing entry is a float; compute totals/min/max directly
        #            total = 0.0
        #            count = 0
        #            mn = stats[0]
        #            mx = stats[0]
        #            for v in stats:
        #                total += v
        #                if v < mn:
        #                    mn = v
        #                if v > mx:
        #                    mx = v
        #                count += 1
        #            if count > 0:
        #                avg = total / count
        #                quick_print("TIMING apples=", count, "total=", total, "avg=", avg, "min=", mn, "max=", mx)
        #            else:
        #                quick_print("TIMING: no numeric stats collected")
        
        
            
            
if __name__ == "__main__":
    # disable timing for leaderboard / direct runs
    #for _ in range(1000):
       dinos(num_items(Items.Bone)+1, False)