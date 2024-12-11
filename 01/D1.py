import pandas as pd

# Read the Excel file
dataframe1 = pd.read_excel('Input1.xlsx', header=None)

# Extract columns into arrays
array1 = dataframe1.iloc[:, 0].to_list()  # First column - Left
array2 = dataframe1.iloc[:, 1].to_list()  # Second column - Right

# Sort both arrays
array1.sort()
array2.sort()

sum = 0
# Calculate the total distance
# total_distance = sum(abs(l - r) for l, r in zip(sorted_col1, sorted_col2))

for i in range(len(array1)):
    sum += abs(array1[i] - array2[i])

# Print the result
print("Total distance:", sum)

######### Part 2

sum = 0
dict2 = {}

# Create Map of frequency
for i in range(len(array2)): 
    if array2[i] in dict2: 
        dict2[array2[i]] += 1
    else:
        dict2[array2[i]] = 1

# Calculate the total score
for i in range(len(array1)): 
    if array1[i] in dict2: 
        sum += array1[i] * dict2[array1[i]]

print("Total distance: ", sum)