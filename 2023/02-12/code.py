import re

CONSTRAINTS = {
    'red': 12,
    'green': 13,
    'blue': 14
}

def count(data):
    sum = 0
    power = 0
    for line in data.splitlines():
        id = re.findall(r'(\w+)\s+(\d+)', line)[0][1]
        rgb = re.findall(r'(\d+)\s+(\w+)', line)
        max = {
            'red': 0,
            'green': 0,
            'blue': 0
        }
        for m in rgb:
            count, color = m
            count = int(count)        
            if count > CONSTRAINTS[color]:            
                break
        else:
            sum += int(id)

        for m in rgb:
            count, color = m
            count = int(count)
            if max[color] < count:
                max[color] = count      
        power += max['red']*max['green']*max['blue']

    return sum, power


if __name__ == "__main__":
    with open("input") as f:
        data = f.read().strip()

    answer_1 = count(data)[0]
    print(f"Answer 1: {answer_1}")

    answer_2 = count(data)[1]
    print(f"Answer 2: {answer_2}")

