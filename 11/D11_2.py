import time
from collections import Counter, defaultdict
from functools import cache

# Function to split numbers based on rules
@cache
def split_number(n):
    if n == 0:
        return [1]
    n_str = str(n)
    if len(n_str) % 2 == 0:
        half = len(n_str) // 2
        return [int(n_str[:half]), int(n_str[half:])]
    return [2024 * n]

# Function to simulate blinks
def simulate_blinks(initial_stones, blinks):
    stone_counts = Counter(initial_stones)

    for _ in range(blinks):
        next_counts = defaultdict(int)
        for stone, count in stone_counts.items():
            for new_stone in split_number(stone):
                next_counts[new_stone] += count
        stone_counts = next_counts

    return sum(stone_counts.values())


def main():
        # Read input from input.txt
    # Initial stones
    # Read input from input.txt
    with open("11/input.txt", "r") as file:
        initial_stones = list(map(int, file.read().strip().split()))

    # Part 1: After 25 blinks
    result_25_blinks = simulate_blinks(initial_stones, 25)
    print(f"Number of stones after 25 blinks: {result_25_blinks}")

    # Part 2: After 75 blinks
    result_75_blinks = simulate_blinks(initial_stones, 75)
    print(f"Number of stones after 75 blinks: {result_75_blinks}")

    # Ranking: After 1000 blinks
    start = time.time()
    result_1000_blinks = simulate_blinks(initial_stones, 1000)
    print(f"Number of stones after 1000 blinks: {result_1000_blinks}")
    end = time.time()
    print("Time elapsed for 1000 blinks: ", end - start)

    # Ranking: After 10000 blinks
    start = time.time()
    result_1000_blinks = simulate_blinks(initial_stones, 1000)
    print(f"Number of stones after 10000 blinks: {result_1000_blinks}")
    end = time.time()
    print("Time elapsed for 10000 blinks: ", end - start)

if __name__ == "__main__":
    main()
