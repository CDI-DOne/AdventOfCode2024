def parse_button_line(line):
    """
    Parse a line in the format "Button X: X+<val>, Y+<val>"
    Returns (x_val, y_val) as integers.
    """
    right_part = line.split(":")[1].strip()
    x_str, y_str = [part.strip() for part in right_part.split(",")]
    x_val = int(x_str[1:])  # skip 'X', leaving "+94" -> int(94)
    y_val = int(y_str[1:])  # skip 'Y', leaving "+34" -> int(34)
    return x_val, y_val


def parse_prize_line(line, offset=0):
    """
    Parse a line in the format "Prize: X=<val>, Y=<val>"
    Returns (Px, Py) integers with offset applied.
    """
    # Example: "Prize: X=8400, Y=5400"
    right_part = line.split(":")[1].strip()
    x_str, y_str = [part.strip() for part in right_part.split(",")]
    Px = int(x_str[2:]) + offset  # skip 'X=' -> '8400'
    Py = int(y_str[2:]) + offset  # skip 'Y=' -> '5400'
    return Px, Py


def read_machine_data(lines, offset=0):
    """
    Given three lines describing one machine:
    Format:
      Button A: X+94, Y+34
      Button B: X+22, Y+67
      Prize: X=8400, Y=5400

    Returns (Ax, Ay, Bx, By, Px, Py).
    Offset is added to the prize coordinates.
    """
    lineA, lineB, lineP = [l.strip() for l in lines]

    Ax, Ay = parse_button_line(lineA)
    Bx, By = parse_button_line(lineB)
    Px, Py = parse_prize_line(lineP, offset=offset)

    return Ax, Ay, Bx, By, Px, Py


def solve_linear_system(Ax, Ay, Bx, By, Px, Py):
    """
    Solve the linear system:
      a*Ax + b*Bx = Px
      a*Ay + b*By = Py
    for integers a,b >=0.
    Returns (a, b) if a solution exists, otherwise None.
    """
    det = Ax * By - Ay * Bx
    if det == 0:
        return None

    numerator_a = Px * By - Py * Bx
    numerator_b = Ax * Py - Ay * Px

    # Check for integral solutions
    if numerator_a % det != 0 or numerator_b % det != 0:
        return None

    a = numerator_a // det
    b = numerator_b // det

    if a < 0 or b < 0:
        return None

    return a, b


def solve_machine(Ax, Ay, Bx, By, Px, Py):
    """
    Solve:
      a*Ax + b*Bx = Px
      a*Ay + b*By = Py
    for nonnegative integers a,b. Minimize cost=3a+b.
    Returns minimal cost or None if no solution exists.
    """
    det = Ax * By - Ay * Bx

    if det != 0:
        # Directly solve the system
        result = solve_linear_system(Ax, Ay, Bx, By, Px, Py)
        if result is None:
            return None
        a, b = result
        return 3 * a + b
    else:
        raise ValueError("Determinant is 0")


if __name__ == "__main__":
    # The main logic to read input, solve each machine, and print result.
    # Assumes an input file "input.txt" in the same directory.
    OFFSET = 10000000000000
    with open("input.txt", "r") as f:
        raw_lines = [line for line in f if line.strip() != ""]

    # Each machine is represented by exactly 3 lines.
    machines = [raw_lines[i:i+3] for i in range(0, len(raw_lines), 3)]

    results = []
    for machine_lines in machines:
        Ax, Ay, Bx, By, Px, Py = read_machine_data(machine_lines, offset=OFFSET)
        cost = solve_machine(Ax, Ay, Bx, By, Px, Py)
        if cost is not None:
            results.append(cost)

    # Print the sum of minimal costs for all solvable machines
    total_cost = sum(results) if results else 0
    print(total_cost)
