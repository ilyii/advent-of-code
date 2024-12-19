from time import perf_counter as pfc


def solution(inp):
    data = [e.replace("\n","").split(" ")for e in inp.readlines()]
    print(data)
    # part 1
    # A 65 = Rock = X 88
    # B 66 = Paper = Y 89
    # C 67 = Scissor = Z 90
    summation = 0
    for round in data:
        enemies_choice = round[0]
        my_choice = round[1]
        summation += ord(my_choice)-87
        if ord(my_choice) - ord(enemies_choice) in [24,21]:
            summation+=6
        elif ord(my_choice) - ord(enemies_choice) in [23]:
            summation+=3
        elif ord(my_choice) - ord(enemies_choice) in [22,25]:
            summation+=0

    print(summation)
    # part 2
    # A 65 = Rock
    # B 66 = Paper
    # C 67 = Scissor
    # X 88 = Loss
    # Y 89 = Draw
    # Z 90 = Win
    summation = 0
    for round in data:
        enemies_choice = round[0]
        result = round[1]
        if result == "X":
            summation+=0
            summation+= (ord(enemies_choice)+22)-87 if enemies_choice != "A" else (ord(enemies_choice)+25)-87
        elif result == "Y":
            summation +=3
            summation += ord(enemies_choice) - 64
        elif result == "Z":
            summation +=6
            summation += (ord(enemies_choice)+24)-87 if enemies_choice != "C" else (ord(enemies_choice)+21)-87

    print(summation)


if __name__ == "__main__":
    start = pfc()
    data = open("input.txt")
    solution(data)
    print(f"Time elapsed: {pfc()-start}s")
