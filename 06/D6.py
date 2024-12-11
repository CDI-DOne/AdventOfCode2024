# Day 6 - Map traversal
def turn_right(direction):
    #Turning right
    directions = ['^', '>', 'v', '<']
    idx = directions.index(direction)
    return directions[(idx + 1) % 4]

def forward_pos(x, y, direction):
    #Moving 1 step forward
    if direction == '^':
        return x - 1, y
    elif direction ==  '>':
        return x, y + 1
    elif direction ==  'v':
        return x + 1, y
    elif direction == '<':
        return x, y - 1
    else: 
        raise ValueError("Invalid direction")
    
def map_transitions(grid):
    #two dicts are computed that store the next step // Next direction if turned
    #Dicts Format is (x,y,d) : (nx,ny,nd)
    rows = len(grid)
    cols = len(grid[0])

    forward_next = {}
    turn = {}
    directions = ['^', '>', 'v', '<']

    for x in range(rows):
        for y in range(cols):
            for d in directions:
                fx, fy  = forward_pos(x, y, d)

                if not (0 <= fx < rows and 0 <= fy < cols):
                    forward_next[(x, y, d)] = "exit"
                else: 
                    if grid[fx][fy] == "#":
                        forward_next[(x, y, d)] = None
                    else: 
                        forward_next[(x, y, d)] = (fx, fy, d)

                rd = turn_right(d)
                turn[(x, y, d)] = (x, y, rd)   

    return forward_next, turn


def find_guard(grid):
    rows = len(grid)
    cols = len(grid[0])
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] in ['^', 'v', '<', '>']:
                return i, j, grid[i][j]
    raise ValueError("No starting position in grid")

def traverse(grid, forward_next, turn, start_pos, add_obstruction = None):
    # We run through the course from the starting pos to see if there is a loop
    # Returns the visited cells and whether the guard exits the map
    rows = len(grid)
    cols = len(grid[0])
    
    x, y, d = start_pos

    visited = set()
    visited.add((x, y))

    seen_states = set()

    while True:
        if not (0 <= x < rows and 0 <= y < cols):
            #exit
            return visited, True
        
        state = (x, y, d)
        if state in seen_states:
            #loop
            return visited, False
        seen_states.add(state)
        
        fn = forward_next[state]
        if fn == "exit":
            return visited, True
        elif fn is None: 
            blocked = True 
        else:
            if add_obstruction is not None: 
                ox, oy = add_obstruction
                fx, fy, fd = fn 
                if (fx, fy) == (ox, oy):
                    blocked = True 
                else: 
                    blocked = False
            else: 
                blocked = False
        
        if blocked: 
            #blocked
            x, y, d = turn[(x, y, d)]
        else: 
            #move
            fx, fy, fd = fn
            x, y, d = fx, fy, fd
            # Check again if exit
            if not (0 <= x < rows and 0 <= y < cols):
                # exit
                return visited, True
            visited.add((x, y))


def main(): 
    with open('Input.txt', 'r') as f:
        grid = [line.rstrip('\n') for line in f]

        forward_next, turn = map_transitions(grid)
        start_pos = find_guard(grid)

        #P1
        visited_no_obstruction, exited = traverse(grid, forward_next, turn, start_pos)
        print("Part 1 answer:", len(visited_no_obstruction)) 

        #P2
        loop_count = 0
        for visited_cell in visited_no_obstruction:
            visited, exited = traverse(grid, forward_next, turn, start_pos, visited_cell)
            if not exited:
                loop_count += 1
        
        print("Part 2 answer:", loop_count)

if __name__ == "__main__":
    main()



# ###################
# def parse_map(input_map): 
#     grid = []
#     guard_pos = None
#     for y, line in enumerate(input_map.strip().split('\n')):
#         grid.append(line)
#         for x in range(len(line)): 
#             if line[x] in ['^', '>', 'v', '<']:
#                 guard_pos = (x, y)
#                 guard_dir = line[x]
#     return grid, guard_pos, guard_dir

# def move_guard(position, direction):
#     x, y = position
#     if direction == '^':
#         return (x, y - 1)
#     elif direction == 'v':
#         return (x, y + 1)
#     elif direction == '>':
#         return (x + 1, y)
#     elif direction == '<':
#         return (x - 1, y)

# def turn_right(direction):
#     if direction == '^':
#         return '>'
#     elif direction == '>':
#         return 'v'
#     elif direction == 'v':
#         return '<'
#     elif direction == '<':
#         return '^'

# def simulate_patrol(input_map):
#     grid, guard_position, guard_direction = parse_map(input_map)
#     visited_positions = set()
#     visited_positions.add(guard_position)

#     rows, cols = len(grid), len(grid[0])

#     while True:
#         next_position = move_guard(guard_position, guard_direction)
#         x, y = next_position

#         # Check if the guard is out of bounds
#         if not (0 <= x < cols and 0 <= y < rows):
#             break

#         # Check if there's an obstacle in front of the guard
#         if grid[y][x] == '#':
#             guard_direction = turn_right(guard_direction)
#         else:
#             # Move the guard forward
#             guard_position = next_position
#             visited_positions.add(guard_position)

#     return visited_positions


# with open('Input.txt', 'r') as file:
#     input_map = file.read()

# visited_positions = simulate_patrol(input_map)
# print("Number of distinct positions visited:", len(visited_positions))

# # grid, guard_pos, guard_dir = parse_map(input_map)
# # print(guard_pos)
# # print(guard_dir)
# # print(grid)