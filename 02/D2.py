import pandas as pd
import math

# Read the Excel file
df = pd.read_excel('D2.xlsx', header=None)

values = df.values.tolist()

# Replace this with your actual data as a list of lists
# # Example input:
# values = [
#     [7, 6, 4, 2, 1],
#     [1, 2, 7, 8, 9],
#     [9, 7, 6, 2, 1],
#     [1, 3, 2, 4, 5],
#     [8, 6, 4, 4, 1],
#     [1, 3, 6, 7, 9]
# ]

def remove_trailing_nan(lst):
    # Remove trailing NaN values
    while len(lst) > 0 and (isinstance(lst[-1], float) and math.isnan(lst[-1])):
        lst.pop()
    return lst

def is_strictly_monotonic(lst, min_diff=1, max_diff=3):
    """Check if the list is strictly monotonic."""
    increasing = True
    decreasing = True
    for i in range(len(lst) - 1):
        diff = lst[i + 1] - lst[i]
        if not (min_diff <= diff <= max_diff):
            increasing = False
        if not (min_diff <= -diff <= max_diff):
            decreasing = False
        # Early exit: if neither increasing nor decreasing is possible
        if not increasing and not decreasing:
            return False
    return True

# Count the number of safe reports
safe_reports_count = 0

for record in values:
    if is_strictly_monotonic(record):
        safe_reports_count += 1

print("Number of safe records without dampener:", safe_reports_count)

############################

def is_safe_with_dampener_2(lst, min_diff=1, max_diff=3):
    lst = remove_trailing_nan(lst)  # Remove trailing NaN values
    n = len(lst)
    
    if n <= 2:  # Short lists are always monotonic
        return True

    violations = 0
    direction = None  # Track the direction of the sequence ('increasing' or 'decreasing')

    for i in range(1, n):
        diff = lst[i] - lst[i - 1]

        if direction is None:
            if diff > 0:
                direction = 'increasing'
            elif diff < 0:
                direction = 'decreasing'
            else:
                violations += 1
        else:
            if direction == 'increasing' and not (min_diff <= diff <= max_diff):
                violations += 1
            elif direction == 'decreasing' and not (min_diff <= -diff <= max_diff):
                violations += 1

    return violations == 0

def is_safe_with_dampener(lst, min_diff=1, max_diff=3):
    """Check if the list is monotonic or can be made monotonic by removing one element."""
    lst = remove_trailing_nan(lst)  # Remove trailing NaN values
    n = len(lst)
    
    if n <= 2:
        return True

    if is_strictly_monotonic(lst, min_diff, max_diff):
        return True

    for i in range(n):
        modified_lst = lst[:i] + lst[i+1:]
        if is_strictly_monotonic(modified_lst, min_diff, max_diff):
            return True

    return False

# Count the number of safe reports with the Problem Dampener
safe_reports_count = sum(1 for record in values if is_safe_with_dampener(record))

print("Number of safe records with dampener:", safe_reports_count)
