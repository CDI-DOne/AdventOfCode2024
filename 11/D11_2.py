from collections import Counter

def simulate_blinks_optimized(initial_stones, blinks):
    stone_counts = Counter(initial_stones)

    for _ in range(blinks):
        new_stone_counts = Counter()

        for stone, count in stone_counts.items():
            if stone == 0:
                # Rule 1: 0 -> 1
                new_stone_counts[1] += count
            elif stone < 10:
                # Single-digit stones cannot be split
                new_stone_counts[stone * 2024] += count
            elif stone % 10 == 0:
                # Split the stone if even number of digits
                divisor = 10 ** (len(str(stone)) // 2)
                left = stone // divisor
                right = stone % divisor
                new_stone_counts[left] += count
                new_stone_counts[right] += count
            else:
                # Rule 3: Multiply the stone by 2024
                new_stone_counts[stone * 2024] += count

        stone_counts = new_stone_counts

    return sum(stone_counts.values())

# Initial stones
initial_stones = [2, 77706, 5847, 9258441, 0, 741, 883933, 12]

# Part 1: After 25 blinks
result_25_blinks = simulate_blinks_optimized(initial_stones, 25)
print(f"Number of stones after 25 blinks: {result_25_blinks}")

# Part 2: After 75 blinks
result_75_blinks = simulate_blinks_optimized(initial_stones, 75)
print(f"Number of stones after 75 blinks: {result_75_blinks}")

import time
start = time.time()

# Ranking: After 1000 blinks
result_1000_blinks = simulate_blinks_optimized(initial_stones, 1000)
print(f"Number of stones after 1000 blinks: {result_1000_blinks}")

end = time.time()
print("Time elapsed: ", end - start)
