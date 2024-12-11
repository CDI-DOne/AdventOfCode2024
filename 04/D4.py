def count_xmas_patterns(grid):
    rows, cols = len(grid), len(grid[0])
    count = 0

    def is_valid_pattern(x, y):
        """
        Check if there's an X-MAS pattern centered at grid[x][y].
        """
        if x - 1 < 0 or x + 1 >= rows or y - 1 < 0 or y + 1 >= cols:
            return False

        # Top-left MAS
        top_left = grid[x - 1][y - 1] + grid[x][y] + grid[x + 1][y + 1]
        # Bottom-left MAS
        bottom_left = grid[x + 1][y - 1] + grid[x][y] + grid[x - 1][y + 1]

        # A valid pattern must have MAS or SAM on both diagonals
        valid = {"MAS", "SAM"}
        return top_left in valid and bottom_left in valid

    for x in range(1, rows - 1):  # Skip edges (no room for diagonals)
        for y in range(1, cols - 1):
            if is_valid_pattern(x, y):
                count += 1

    return count

# Read the grid from the text file
filename = "grid.txt"
with open(filename, "r") as file:
    grid = [list(line.strip()) for line in file]

# Count occurrences of the X-MAS pattern
result = count_xmas_patterns(grid)
print(f"The X-MAS pattern appears {result} times in the grid.")
