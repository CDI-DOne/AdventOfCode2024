from itertools import product
import math

def parse_input(file_path):
    with open(file_path, "r") as f:
        lines = f.read().strip().split("\n\n")

    machines = []
    for machine in lines:
        lines = machine.split("\n")
        a_x, a_y = map(int, [lines[0].split()[2][2:].rstrip(','), lines[0].split()[3][2:].rstrip(',')])
        b_x, b_y = map(int, [lines[1].split()[2][2:].rstrip(','), lines[1].split()[3][2:].rstrip(',')])
        prize_x, prize_y = map(int, [lines[2].split()[1][2:].rstrip(','), lines[2].split()[2][2:].rstrip(',')])
        # Adjust prize coordinates
        prize_x += 10000000000000
        prize_y += 10000000000000
        machines.append(((a_x, a_y), (b_x, b_y), (prize_x, prize_y)))
    return machines

def gcd_extended(a, b):
    """Returns gcd(a, b) and the coefficients of Bezout's identity."""
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = gcd_extended(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y

def solve_diophantine(a, b, c):
    """Solve a linear Diophantine equation ax + by = c."""
    gcd, x, y = gcd_extended(a, b)
    if c % gcd != 0:
        return None  # No solution

    # Scale solution to make it valid for c
    x *= c // gcd
    y *= c // gcd
    a //= gcd
    b //= gcd

    # Adjust x and y to be non-negative
    k = -x // b if x < 0 else (y // a if y < 0 else 0)
    x += k * b
    y -= k * a

    if x < 0 or y < 0:
        return None  # No valid non-negative solution

    return x, y

def solve_machine(a, b, prize):
    """Solve a single machine for the minimum tokens or determine if it's unsolvable."""
    a_x, a_y = a
    b_x, b_y = b
    p_x, p_y = prize

    x_solution = solve_diophantine(a_x, b_x, p_x)
    y_solution = solve_diophantine(a_y, b_y, p_y)

    if not x_solution or not y_solution:
        return math.inf, -1, -1

    x_a, x_b = x_solution
    y_a, y_b = y_solution

    # Iterate over possible adjustments to find a valid and minimal solution
    min_tokens = math.inf
    best_a = -1
    best_b = -1

    for k_x in range(-100, 101):  # Adjust range as needed for flexibility
        adj_x_a = x_a + k_x * b_x
        adj_x_b = x_b - k_x * a_x

        for k_y in range(-100, 101):
            adj_y_a = y_a + k_y * b_y
            adj_y_b = y_b - k_y * a_y

            if adj_x_a == adj_y_a and adj_x_b == adj_y_b and adj_x_a >= 0 and adj_x_b >= 0:
                tokens = 3 * adj_x_a + adj_x_b
                if tokens < min_tokens:
                    min_tokens = tokens
                    best_a = adj_x_a
                    best_b = adj_x_b

    if min_tokens == math.inf:
        return math.inf, -1, -1

    return min_tokens, best_a, best_b



def main():
    machines = parse_input("input.txt")
    total_tokens = 0
    prizes_won = 0

    for i, (a, b, prize) in enumerate(machines):
        tokens, a_count, b_count = solve_machine(a, b, prize)
        if tokens < math.inf:
            print(f"Machine {i+1}: Win with {tokens} tokens (A: {a_count}, B: {b_count})")
            total_tokens += tokens
            prizes_won += 1
        else:
            print(f"Machine {i+1}: Cannot win.")

    print(f"\nPrizes won: {prizes_won}")
    print(f"Total tokens spent: {total_tokens}")

if __name__ == "__main__":
    main()
