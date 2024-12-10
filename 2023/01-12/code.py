import re

def calculate(data):
    sum = 0
    for l in data.splitlines():
        numbers = re.findall(r"\d", l)
        sum += int(f'{numbers[0]}{numbers[-1]}')
    return sum


if __name__ == "__main__":
    with open('input') as f:
        data = f.read().strip()

    answer_1 = calculate(data)
    print(f"Answer 1: {answer_1}")

    data = (
        data.replace("one", "o1e")
        .replace("two", "t2o")
        .replace("three", "t3e")
        .replace("four", "f4r")
        .replace("five", "f5e")
        .replace("six", "s6x")
        .replace("seven", "s7n")
        .replace("eight", "e8t")
        .replace("nine", "n9e")
    )
    answer_2 = calculate(data)
    print(f"Answer 2: {answer_2}")


