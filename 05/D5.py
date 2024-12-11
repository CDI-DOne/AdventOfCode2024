def read_input(filename):
    with open(filename, 'r') as f: 
        return [line.strip() for line in f.readlines() if line.strip()]
    
def parse_rules(rules_lines): 
    rules = []
    for line in rules_lines: 
        x, y = line.split('|')
        rules.append((int(x), int(y)))
    return rules

def parse_lines(lines): 
    return [list(map(int, line.split(','))) for line in lines]

def is_correct(line, rules): 
    page_position = {page: i for i, page in enumerate(line)}
    for x, y in rules: 
        if x in page_position and y in page_position: 
            if page_position[x] > page_position[y]: 
                return False 
    return True 

def find_midpage(line): 
    mid = len(line)//2
    return line[mid]

def correct_update(update, rules):
    from functools import cmp_to_key
    def compare(x, y):
        for rule_x, rule_y in rules:
            if rule_x == x and rule_y == y:
                return -1
            elif rule_x == y and rule_y == x:
                return 1
        return 0
    return sorted(update, key=cmp_to_key(compare))


def main(): 
    rules = read_input('Rules.txt')
    lines = read_input('Input.txt')
    
    rules = parse_rules(rules)
    lines = parse_lines(lines)

    sum_1 = 0
    sum_2 = 0
    for line in lines: 
        if is_correct(line, rules): 
            sum_1 += find_midpage(line)
        else: 
            corrected = correct_update(line, rules)
            sum_2 += find_midpage(corrected)
    
    print('Midpages sum up to: ', sum_1)
    print('Corrected Midpages sum up to: ', sum_2)

if __name__ == "__main__":
    main()

