def parse_map(filename): 
    with open(filename, 'r') as f: 
        return [list(map(int, line.strip())) for line in f.readlines()]
    
def is_valid_step(current_height, next_height): 
    return next_height == current_height + 1

def dfs_hikes(grid, x, y, current_height, visited, path): 
    if (x, y) in visited: 
        return []
    visited.add((x, y))
    path.append((x, y))

    if grid[x][y] == 9: 
        trail = [tuple(path)]
        visited.remove((x, y))
        path.pop()
        return trail 
    
    trails = []
    rows, cols = len(grid), len(grid[0])
    for dx, dy in [(-1, 0), (0, 1), (0, -1), (1, 0)]: 
        nx, ny = x + dx, y + dy 
        if 0 <= nx < rows and 0 <= ny < cols and is_valid_step(current_height, grid[nx][ny]): 
            trails += dfs_hikes(grid, nx, ny, grid[nx][ny], visited, path)

    visited.remove((x, y))
    path.pop()
    return trails 

def calculate_trailhead_scores_and_ratings(map_data):
    """Calculates the score and rating for each trailhead."""
    rows, cols = len(map_data), len(map_data[0])
    total_score = 0
    total_rating = 0
    
    for x in range(rows):
        for y in range(cols):
            if map_data[x][y] == 0:  # Trailhead
                visited = set()
                path = []
                trails = dfs_hikes(map_data, x, y, 0, visited, path)
                trail_endings = {trail[-1] for trail in trails}
                total_score += len(trail_endings)  # Score: distinct end points at height 9
                total_rating += len(trails)       # Rating: total distinct trails
    
    return total_score, total_rating

if __name__ == "__main__":
    map_data = parse_map("Input.txt")
    total_score, total_rating = calculate_trailhead_scores_and_ratings(map_data)
    print("Sum of the scores of all trailheads:", total_score)
    print("Sum of the ratings of all trailheads:", total_rating)