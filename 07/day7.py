from itertools import product

# with open("Input.txt", 'r') as file:
#     data = [line.strip() for line in file]
#     data = [{int(data[i].split(":")[0]):list(map(int, data[i].split(":")[1].strip().split(" ")))} for i, _ in enumerate(data)]
#     data = {k: v for d in data for k, v in d.items()}

# valid_equations = []
# print(len(data))
# for i in data:
#     result = i
#     vals = data[i]

valid_equations = []
with open("Input.txt", "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        left, right = line.split(':')
        target = int(left.strip())
        numbers = list(map(int, right.split()))

        available_operator_spaces = len(numbers) - 1

        # Generate all possible combinations of + and *
        combinations = list(product(['+', '*'], repeat=available_operator_spaces))
        combinations = [list(c) for c in combinations]
        
        for c in combinations:
            equation = str(numbers[0])
            for iv, v in enumerate(numbers[1:]):
                equation = '(' + equation + c[iv] + str(v) + ')'
                equ = eval(equation)
            if eval(equation) == target:
                valid_equations.append(target)
                #print(equation)
                #print(result)
                break
            
final_sum = sum(valid_equations)
print(f'final sum: {final_sum}')
