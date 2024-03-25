from time import perf_counter as pfc


def solution(inp):
    # part 1
    data = [e.replace("\n","")for e in inp.readlines()]
    #print(data)
    elves_calories = []
    current = 0
    for elem in data:
        if elem == "":
            elves_calories.append(current)
            current = 0
        else:
            current += int(elem)


    print(max(elves_calories))
    # part 2
    elves_calories.sort(reverse=True)
    print(elves_calories[0]+elves_calories[1]+elves_calories[2])
    #first = elves_calories.index(max(elves_calories)) +1
    #elves_calories.remove(max(elves_calories))
    #second = elves_calories.index(max(elves_calories)) +1
    #elves_calories.remove(max(elves_calories))
    #third = elves_calories.index(max(elves_calories)) +1

    #print(first, second, third)

if __name__ == "__main__":
    start = pfc()
    data = open("input.txt")
    solution(data)
    print(f"Time elapsed: {pfc()-start:.4f}s")
