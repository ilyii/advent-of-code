import time
from collections import defaultdict
import re
import math

def parse(data):
    data = data.splitlines()
    instructions = data[0].strip()
    network = defaultdict(list)
    for line in data[2:]:
        line = line.split(" = ")
        network[line[0]] = re.findall(r"\w+", line[1])

    return instructions, network


def navigate(instructions, network, p2_flag=False):

    s = [k for k in network.keys() if k.endswith("A")] if p2_flag else ["AAA"]
    criterion = "Z" if p2_flag else "ZZZ"

    res = [] 
    for current in s:
        steps = 0
        while True:
            ins = instructions[steps % len(instructions)]
            if ins == "L":
                current = network[current][0]
            elif ins == "R":
                current = network[current][1]
            
            steps += 1
            if current.endswith(criterion):
                res.append(steps)
                break

        
    if p2_flag:        
        common_multiple = res[0]
        for elem in res[1:]:
            common_multiple = common_multiple * elem // math.gcd(common_multiple, elem)
        return common_multiple
    else:
        return res[0]



    
def manage(data, p2_flag=False):
    instructions, network = parse(data)
    
    result = navigate(instructions, network, p2_flag)
    return result


if __name__ == "__main__":
    with open("input.txt") as f:
        data = f.read().strip()

    s1 = time.time()
    answer_1 = manage(data)
    s2 = time.time()
    print(f"Answer 1: {answer_1}")

    s3 = time.time()
    answer_2 = manage(data, p2_flag=True)
    s4 = time.time()
    print(f"Answer 2: {answer_2}")    
    
    print(f'Times: {(s2-s1)*1000:.4f}ms, {(s4-s3)*1000:.4f}ms')

    