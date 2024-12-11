def possible_combinations(line, p2,  target = None): 
    # Calculate all the possible combinations for the line input
    current_combinations = set()
    past_combinations = set()

    past_combinations.add(line[0])
    for i in range(1,len(line)): 
        for num in past_combinations:
            current_combinations.add(num * line[i])
            current_combinations.add(num + line[i])
            if p2: current_combinations.add(int(str(num) + str(line[i])))
        past_combinations = current_combinations
        current_combinations = set()
    
    return target in past_combinations

sum_1, sum_2 = 0, 0
lines = 0 
data = {}
with open("Input.txt", "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        left, right = line.split(':')
        target = int(left.strip())
        numbers = list(map(int, right.split()))
        
        if possible_combinations(numbers, False,  target): 
            sum_1 += target

        if possible_combinations(numbers, True,  target): 
            sum_2 += target

        lines += 1
        if target in data: 
            print("theres multiple keys")
        else: 
            data[target] = 1

        
print("The first part answer is: ", sum_1)
print("The second part answer is: ", sum_2)
print(lines)