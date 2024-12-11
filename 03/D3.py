with open('D3.txt', 'r') as file:
    data = file.read().replace('\n', '')

str = "mul(,)"

str_do = "do()"
str_dont = "don't()"
flag_do = True

i, j, k = 0, 0, 0
int1, int2 = 0, 0
sum = 0
flag = False
for s in data: 
    if s == str_do[j]: 
        j+= 1
        if j == len(str_do): 
            flag_do = True 
            j = 0
    else: 
        j = 0 
    
    if s == str_dont[k]: 
        k += 1
        if k == len(str_dont): 
            flag_do = False 
            k = 0 
    else: 
        k = 0

    if s == str[i] and i < 4: 
        i += 1
    elif i == 4 or i == 5 or i == 6: 
        pass
    else:
        i = 0

    if flag_do: 
        if i == 4: 
            if  s == "(" and not flag: 
                flag = True 
            elif s.isnumeric(): 
                int1 = 10 * int1 + int(s)
            elif int1 != 0 and s == str[i]:
                i += 1
                flag = False
            else: 
                i = 0
                int1 = 0
                flag = False
        
        if i == 5:
            if  s == "," and not flag: 
                flag = True 
            elif s.isnumeric(): 
                int2 = 10 * int2 + int(s)
            elif int2 != 0 and s == str[i]:
                i += 1
                flag = False
            else: 
                i = 0
                int1 = 0
                int2 = 0
                flag = False
        
        if i == 6: 
            sum += int1 * int2
            i = 0 
            int1 = 0 
            int2 = 0

print("the expected sum is: ", sum)

