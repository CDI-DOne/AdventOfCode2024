def read_grid(filename):
    with open(filename, 'r') as f:
        grid = [line.rstrip('\n') for line in f]
    return grid

def parse_antennas(grid):
    """Read antennas into dictionary of frequeny: [(x1, y1), (x2, y2), ..]"""
    antennas = {}
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] != ".":
                if grid[x][y] in antennas:
                    antennas[grid[x][y]].append((x, y))
                else:
                    antennas[grid[x][y]] = [(x, y)]
    return antennas

def is_within_bounds(position, grid):
    """Checks if a position is within the grid bounds."""
    x, y = position
    return 0 <= x < len(grid) and 0 <= y < len(grid[0])

def extend_antinodes(antinodes, start, fx, fy, grid, direction):
    """Extends antinodes in a given direction until out of bounds."""
    x, y = start
    k = 3
    while True:
        antinode = (x + direction * k * fx, y + direction * k * fy)
        if not is_within_bounds(antinode, grid):
            break
        antinodes.add(antinode)
        k += 1

def calculate_antinodes(grid, antennas):
    antinodes = set()
    antinodes_2 = set()

    # Iterate over each antenna
    for antenna, locations in antennas.items():
        for i in range(len(locations)):
            for j in range(i + 1, len(locations)):
                x1, y1 = locations[i]
                x2, y2 = locations[j]
                
                # Calculate the vector between two antennas
                fx, fy = x2 - x1, y2 - y1

                # Calculate initial antinode positions
                antinode1 = (x1 + 2 * fx, y1 + 2 * fy)
                antinode2 = (x2 - 2 * fx, y2 - 2 * fy)

                # Check bounds and add valid antinodes
                if is_within_bounds(antinode1, grid):
                    antinodes.add(antinode1)
                    antinodes_2.add(antinode1)

                if is_within_bounds(antinode2, grid):
                    antinodes.add(antinode2)
                    antinodes_2.add(antinode2)

                # Part 2: Include antenna locations and extend antinodes
                antinodes_2.add((x1, y1))
                antinodes_2.add((x2, y2))
                extend_antinodes(antinodes_2, (x1, y1), fx, fy, grid, direction=1)
                extend_antinodes(antinodes_2, (x2, y2), fx, fy, grid, direction=-1)

    return len(antinodes), len(antinodes_2)


def main():
    grid = read_grid('Input.txt')
    antennas = parse_antennas(grid)
    p1, p2 = calculate_antinodes(grid, antennas)
    print("P1:", p1)
    print("P2:", p2)

if __name__ == "__main__":
    main()
