from time import perf_counter as pfc


def solution(inp):
    data = [e.replace("\n","") for e in inp.readlines()]
    #print(data)
    summation = 0
    for line in data:
        if len(line) < 1:
            continue
        half1 = set(line[:int(len(line)/2)])
        half2 = set(line[int(len(line)/2):])
        #print(half1, half2)
        char = list(half1.intersection(half2))

        char = list(half1.intersection(half2))[0]

        summation += ord(char)-38 if 65 <= ord(char) <= 90 else ord(char)-96
    # part 1
    print(summation)
    # part 2
    summation = 0
    for i in range(100):
        f,s,t = set(data[i*3]),set(data[i*3+1]), set(data[i*3+2])
        #print(f,s,t)
        i1 = f.intersection(s)
        char = list(i1.intersection(t))[0]
        summation += ord(char) - 38 if 65 <= ord(char) <= 90 else ord(char) - 96
    print(summation)
    return


if __name__ == "__main__":
    start = pfc()
    data = open("input.txt")
    solution(data)
    print(f"Time elapsed: {pfc()-start}s")