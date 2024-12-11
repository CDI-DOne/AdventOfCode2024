from collections import Counter

def simulate_blinks(initial_stones, blinks):
    """ Process all the stones for a given number of blinks"""
    stone_counts = Counter(initial_stones)

    for i in range(blinks):
        new_stone_counts = Counter()

        for stone, count in stone_counts.items():
            if stone == 0: 
                new_stone_counts[1] += count
            elif len(str(stone)) % 2 == 0: 
                num_str = str(stone)
                mid = len(num_str) // 2
                left = int(num_str[:mid])
                right = int(num_str[mid:])   
                new_stone_counts[left] += count
                new_stone_counts[right] += count
            else: 
                new_stone_counts[stone * 2024] += count
        
        stone_counts = new_stone_counts

    return sum(stone_counts.values())

def main():
    # Read input from input.txt
    with open("input.txt", "r") as file:
        initial_stones = list(map(int, file.read().strip().split()))

    # Part 1 
    result1 = simulate_blinks(initial_stones, 25)
    print("Part 1: ", result1)

    # Part 2
    result2 = simulate_blinks(initial_stones, 75)
    print("Part 2: ", result2)



if __name__ == "__main__":
    main()
