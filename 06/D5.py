def turn_right(direction):
    directions = ['^', '>', 'v', '<']
    idx = directions.index(direction)
    return directions[(idx + 1) % 4]

def forward_pos(x, y, direction):
    if direction == '^':
        return x - 1, y
    elif direction == 'v':
        return x + 1, y
    elif direction == '<':
        return x, y - 1
    elif direction == '>':
        return x, y + 1
    else:
        raise ValueError("Invalid direction")

def build_transitions(grid):
    """
    Precompute transitions for each state: a state is (x, y, direction).
    We'll store two dictionaries:
      forward_next[(x,y,d)] = next_state if going forward is possible without obstruction
      turn_next[(x,y,d)] = next_state if forward is blocked or we choose to turn right.

    Note: "next_state" is always (nx, ny, nd) or special marker for 'exit' if leaving the map.
    """
    rows = len(grid)
    cols = len(grid[0])
    directions = ['^', '>', 'v', '<']

    forward_next = {}
    turn_next = {}

    # We consider each cell and direction
    for x in range(rows):
        for y in range(cols):
            for d in directions:
                fx, fy = forward_pos(x, y, d)

                # Check if forward cell is out of bounds
                if not (0 <= fx < rows and 0 <= fy < cols):
                    # Forward leads out of the map => forward leads to 'exit'
                    forward_next[(x, y, d)] = 'exit'
                else:
                    # Inside map
                    if grid[fx][fy] == '#':
                        # Forward is blocked by #, so forward action not possible
                        forward_next[(x, y, d)] = None  # indicates blocked forward
                    else:
                        # Forward is possible
                        forward_next[(x, y, d)] = (fx, fy, d)

                # Compute turn_right state:
                rd = turn_right(d)
                # After turning right, we do not move, we just change direction and then on next step attempt forward again.
                turn_next[(x, y, d)] = (x, y, rd)

    return forward_next, turn_next

def find_guard_start(grid):
    rows = len(grid)
    cols = len(grid[0])
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] in ['^', 'v', '<', '>']:
                return i, j, grid[i][j]
    raise ValueError("No guard start found")

def simulate(grid, forward_next, turn_next, add_obstruction=None):
    """
    Simulate guard movement with optional single obstruction at add_obstruction=(ox, oy).
    forward_next, turn_next are precomputed transitions without obstruction.
    If add_obstruction is set, that cell is considered blocked for forward attempts.

    Returns:
      visited: set of visited (x, y)
      exited: bool indicating if guard left the map
    """
    rows = len(grid)
    cols = len(grid[0])
    start_x, start_y, start_dir = find_guard_start(grid)

    x, y, d = start_x, start_y, start_dir
    # The visited set includes starting position
    visited = set()
    visited.add((x, y))

    seen_states = set()

    while True:
        # Check if outside map
        if not (0 <= x < rows and 0 <= y < cols):
            # Guard exited
            return visited, True

        state = (x, y, d)
        if state in seen_states:
            # Loop detected
            return visited, False
        seen_states.add(state)

        # Determine if forward is blocked due to obstruction
        fn = forward_next[state]  # forward attempt result
        if fn == 'exit':
            # Forward would go outside the map -> guard leaves if steps forward
            return visited, True
        elif fn is None:
            # Forward blocked by '#' from the original scenario
            blocked = True
        else:
            # fn is (fx, fy, fd), forward cell is free originally
            # Check if add_obstruction blocks it now
            if add_obstruction is not None:
                ox, oy = add_obstruction
                fx, fy, fd = fn
                if (fx, fy) == (ox, oy):
                    # This cell is now obstructed
                    blocked = True
                else:
                    blocked = False
            else:
                blocked = False

        if blocked:
            # turn right
            x, y, d = turn_next[state]
        else:
            # Move forward
            fx, fy, fd = fn
            x, y, d = fx, fy, fd
            # Check boundary again
            if not (0 <= x < rows and 0 <= y < cols):
                # Moved outside map, guard leaves
                return visited, True
            visited.add((x, y))

def main():
    # Read input
    with open('Input.txt', 'r') as f:
        grid = [line.rstrip('\n') for line in f]

    # Precompute transitions
    forward_next, turn_next = build_transitions(grid)

    # Part 1: Number of distinct visited cells without any additional obstruction
    visited_no_obst, exited = simulate(grid, forward_next, turn_next)
    part1_answer = len(visited_no_obst)
    print("Part 1 answer:", part1_answer)  # Should now match the expected 5534

    # Part 2: We try placing an obstruction on every '.' cell except guard start
    start_x, start_y, start_dir = find_guard_start(grid)

    # Collect all floor cells
    floor_cells = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (i, j) != (start_x, start_y) and grid[i][j] == '.':
                floor_cells.append((i, j))

    loop_positions_count = 0
    # Simulate for each candidate obstruction
    for cell in floor_cells:
        visited, exited = simulate(grid, forward_next, turn_next, add_obstruction=cell)
        if not exited:
            loop_positions_count += 1

    print("Part 2 answer:", loop_positions_count)

if __name__ == "__main__":
    main()
