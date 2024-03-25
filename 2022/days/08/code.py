from time import perf_counter as pfc
import re

def solution(inp):
    # part 1
    inp = inp.readlines()
    for i in range(len(inp)):
        inp[i] = [c for c in inp[i][:-1]]
    #print(inp)
    visible = 0
    for i,row in enumerate(inp):
        if i == 0 or i == len(inp)-1:
            visible += len(row)-2
        for j, val in enumerate(row):
            if j == 0 or j == len(row) - 1:
                visible += 1
            elif 0 < i < len(inp)-1:
                if not False in [val > z for z in inp[i][:j]] or not False in [val > z for z in inp[i][j+1:]] or not False in [val > z for z in [inp[z][j] for z in range(i)]] or not False in [val > z for z in [inp[z][j] for z in range(i+1, len(inp[0]))]]:
                    visible += 1

    #print(visible)
    # part 2
    best_score = 0
    directions = [(-1,0),(0,1),(1,0),(0,-1)]
    for i,row in enumerate(inp):
        for j, val in enumerate(row):
            score = 1
            for (direction_row,direction_col) in directions:                        
                distance = 1
                cur_row = i+direction_row
                cur_col = j+direction_col
                while True:
                    if not (0<=cur_row<len(row) and 0<=cur_col<len(inp)):
                        distance -= 1
                        break

                    if inp[cur_row][cur_col]>=inp[i][j]:
                        break
                    distance += 1
                    cur_row += direction_row
                    cur_col += direction_col
                score *= distance
            best_score = score if score > best_score else best_score

        

    print(best_score)        

    

    return


if __name__ == "__main__":
    start = pfc()
    data = open("input.txt")
    #data = open("input.txt")
    solution(data)
    print(f"Time elapsed: {pfc()-start}s")
