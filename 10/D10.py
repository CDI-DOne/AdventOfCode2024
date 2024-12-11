def parse_map(file_path):
    """Reads the input file and parses the topographic map."""
    with open(file_path, 'r') as f:
        return [list(map(int, line.strip())) for line in f.readlines()]

def is_valid_move(height, current_height):
    """Checks if the move is valid based on the height constraint."""
    return height == current_height + 1

def dfs(map_data, x, y, current_height, visited):
    """Performs a depth-first search to find all reachable 9s from a trailhead."""
    if (x, y) in visited:
        return 0
    visited.add((x, y))
    
    rows, cols = len(map_data), len(map_data[0])
    if map_data[x][y] == 9:
        return 1  # Reached a 9
    
    score = 0
    # Explore up, down, left, and right
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols and is_valid_move(map_data[nx][ny], current_height):
            score += dfs(map_data, nx, ny, map_data[nx][ny], visited)
    
    return score

def calculate_trailhead_scores(map_data):
    """Calculates the score for each trailhead and returns the total score."""
    rows, cols = len(map_data), len(map_data[0])
    total_score = 0
    
    for x in range(rows):
        for y in range(cols):
            if map_data[x][y] == 0:  # Trailhead
                visited = set()
                total_score += dfs(map_data, x, y, 0, visited)
    
    return total_score

if __name__ == "__main__":
    map_data = parse_map("Input.txt")
    total_score = calculate_trailhead_scores(map_data)
    print("Sum of the scores of all trailheads:", total_score)
