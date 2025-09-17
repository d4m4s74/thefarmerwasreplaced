from helper import goto_no_wrap
num_weird_substance = get_world_size() * num_unlocked(Unlocks.Mazes)
directions = [North,East,South,West]
opposites = {North:South,South:North,East:West,West:East}

def is_direction_towards_target(cur,target,direction):
    cx, cy = cur
    tx, ty = target
    if direction == North:
        return cy  < ty 
    elif direction == East:
        return cx < tx
    if direction == South:
        return cy  > ty 
    elif direction == West:
        return cx > tx

def opposite_direction(d):
    return opposites[d]
    
def distance(source, target):
    return abs(source[0] - target[0]) + abs(source[1] - target[1])

def next_location(yx,d):
	if directions[d] == North:
		return xy[0], xy[1]+1
	if directions[d] == South:
		return xy[0], xy[1]-1
	if directions[d] == East:
		return xy[0]+1, xy[1]
	if directions[d] == West:
		return xy[0]-1, xy[1]
        

def traverse_maze():
	neighbors = {(get_pos_x(), get_pos_y()):dict()}
	direction = 0
	chest = None
	#first traversal
	visited = set()
	doors = []
	for i in range(get_world_size()):
			row = []
			for j in range(get_world_size()):
				row.append(set())
			doors.append(row)
	while len(visited) < get_world_size()*get_world_size():
		prev = get_pos_x(), get_pos_y()
		visited.add(prev)
		if get_entity_type() == Entities.Treasure:
			chest = prev
		
		while not move(directions[direction]):
			direction = (direction + 1) % 4
		doors[prev[1]][prev[0]].add(directions[direction])
		cur = get_pos_x(), get_pos_y()
		doors[cur[1]][cur[0]].add(directions[(direction + 2) % 4])
		if cur not in neighbors:
			neighbors[cur] = {prev:directions[direction]}
		else:
			neighbors[cur][prev] = directions[direction]
		neighbors[prev][cur] = directions[(direction + 2) % 4]
		direction = (direction - 1) % 4
	return doors, neighbors, chest
	
def find_path_dfs(neighbors,start,end,last = None, visited = set()):
	visited.add(end)
	if start == end:
		return []
	minsteps = 1000000
	steps = []
	for n in neighbors[end]:
		if n != last and n not in visited:
			path = find_path(neighbors, start, n ,end, visited)
			if path != None and minsteps > len(path):
				minsteps = len(path)
				steps = path + [neighbors[end][n]]
	if minsteps != 1000000:
		return steps
	return None
    
def find_path_bfs(neighbors,start,end):
    move_stack = [(end,[])]
    visited = {end}
    cur = (end,[])
    while len(move_stack) > 0:
        cur = move_stack.pop(0)
        for n in neighbors[cur[0]]:
            if n not in visited:
                if n == start:
                    return [neighbors[cur[0]][n]] + cur[1]
                visited.add(n)
                move_stack.append((n,[neighbors[cur[0]][n]] + cur[1]))
                
def find_path_bibfs(neighbors,start,end):
    move_stack_backward = [(end,None)]
    move_stack_forward = [(start,None)]
    visited_backward = {end:[]}
    visited_forward = {start:[]}
    while True:
        #backwards
        cur_back = move_stack_backward.pop(0)
        for n in neighbors[cur_back[0]]:
            if n not in visited_backward:
                if n in visited_forward:
                    #quick_print(visited_forward[n], [neighbors[cur_back[0]][n]], cur_back[1])
                    #reverse forward path and add to backwards path
                    forward_path = visited_forward[n]
                    path = (neighbors[cur_back[0]][n], cur_back[1])
                    while forward_path:
                        path = (forward_path[0], path)
                        forward_path = forward_path[1]
                    return path
                visited_backward[n] = ((neighbors[cur_back[0]][n]), cur_back[1])
                move_stack_backward.append((n,visited_backward[n]))
        #forward
        cur_forward = move_stack_forward.pop(0)
        for n in neighbors[cur_forward[0]]:
            if n not in visited_forward:
                if n in visited_backward:
                    #quick_print(cur_forward[1] , visited_backward[n])
                    #reverse forward path and add to backwards path
                    forward_path = cur_forward[1]
                    path = (opposites[neighbors[cur_forward[0]][n]], visited_backward[n])
                    while forward_path:
                        path = (forward_path[0], path)
                        forward_path = forward_path[1]
                    
                    return path
                visited_forward[n] = ((opposites[neighbors[cur_forward[0]][n]]), cur_forward[1])
                move_stack_forward.append((n,visited_forward[n]))
                

                
def find_path_astar(neighbors,start,end):
	if start == end:
		return None
    high_stack = ((end,None),None)
    low_stack = None
    visited = {end}
    cur = (end,None)
    while True:
        if not high_stack:
            high_stack = low_stack
            low_stack = None
        cur = high_stack[0]
        high_stack = high_stack[1]
        for n in neighbors[cur[0]]:
            if n not in visited:
                if n == start:
                    return (neighbors[cur[0]][n], cur[1])
                visited.add(n)
                if distance(start,cur[0]) > distance(start,n):
                    high_stack = ((n,((neighbors[cur[0]][n], cur[1]))), high_stack)
                else:
                    low_stack = ((n,((neighbors[cur[0]][n], cur[1]))), low_stack)

	
        
def follow_ll_path(path, neighbors = None, doors = None):
	if not neighbors:
		while path != None:
            d = path[0]
            path = path[1]
			move(d)
	else:
		removed = 0	
		while path:
            d = path[0]
            path = path[1]
			x = get_pos_x()
			y = get_pos_y()
			for e in directions:
				if e not in doors[y][x] and move(e):
					newx, newy = get_pos_x(), get_pos_y()
					neighbors[(newx,newy)][(x,y)] = e
					neighbors[(x,y)][newx,newy] = opposites[e]
					doors[y][x].add(e)
					doors[newy][newx].add(opposites[e])
					#quick_print("Added", (x,y), (newx,newy))
					move(opposites[e]) 
					removed += 1
			move(d)
		return removed

def mazes(num):
	while (num_items(Items.Gold) < num):
		plant(Entities.Bush)
		use_item(Items.Weird_Substance, num_weird_substance)
		doors, neighbors, chest = traverse_maze()
		#quick_print(neighbors)
		chests = 0
		removed = 0
		while True:
			if chests > 262:
				goto_no_wrap(chest[0],chest[1])
				path = find_path_astar(neighbors,(get_pos_x(),get_pos_y()),chest)
			elif removed < 31:
				path = find_path_bibfs(neighbors,(get_pos_x(),get_pos_y()),chest)
			else:
				path = find_path_astar(neighbors,(get_pos_x(),get_pos_y()),chest)
            if removed < 46:
                removed += follow_ll_path(path,neighbors,doors)
            else:
                while path != None:
                    d = path[0]
                    path = path[1]
                    move(d)
			#quick_print(path)

			chest = measure()
			if not chest:
				break
			use_item(Items.Weird_Substance, num_weird_substance)
			chests += 1
		#quick_print(removed)
		harvest()
		
mazes(300000)
