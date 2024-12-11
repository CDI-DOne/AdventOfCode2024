def Read_File(file_name):
    with open(file_name, 'r') as data:
        x = [int(i) for i in data.read().replace("\n", "")]

    return x
import time
x = Read_File('Input.txt')

# x = [ int(i) for i in "2333133121414131402" ]
start = time.time()
sum = 0
idx = 0
j = len(x) - 1
for i in range(len(x)):
  if i%2 == 0:
    id = i/2
    progression_sum = (x[i] * (2*idx + x[i] - 1))/2
    sum += id * progression_sum
    idx += x[i]
  else:
    while x[i] > 0:
      diff = min(x[i], x[j])
      x[i] -= diff
      x[j] -= diff
      id = j/2
      progression_sum = (diff * (2*idx + diff - 1))/2
      sum += id * progression_sum
      idx += diff
      if x[j] == 0:
        j -= 2
  if i == j:
    break
print(sum)
end = time.time()
print("Time elapsed: ", end - start)

x = Read_File('Input.txt')
start = time.time()
sum = 0
j = len(x) - 1
y = []
idx = 0
for i in range(len(x)):
  y.append((idx, idx+x[i]))
  idx += x[i]
  
while j >= 0:
  for i in range(1, j, 2):
    if (y[i][1] - y[i][0]) >= x[j]:
      id = j/2
      progression_sum = (x[j] * (2 * y[i][0] + x[j] - 1))/2
      y[i] = (y[i][0] + x[j], y[i][1])
      x[j] = 0
      sum += id*progression_sum
      break
    if i + 1 == j:
      id = j/2
      progression_sum = (x[j] * (2 * y[i + 1][0] + x[j] - 1))/2
      sum += id* progression_sum
  j -= 2

end = time.time()
print(sum)
print("Time elapsed: ", end - start)