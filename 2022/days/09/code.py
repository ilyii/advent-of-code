from time import perf_counter as pfc

GRID = [[".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", "."],
        ["s", ".", ".", ".", ".", "."]]

HEAD = "H"
TAIL = "T"
START = "s"

DIR = {
    "L": (-1, 0),
    "R": (1, 0),
    "U": (0, 1),
    "D": (0, -1),
}


def read_file(file_path):
    with open(file_path, encoding="utf-8") as f:
        return f.read()


def draw_grid(h_pos, t_pos):
    GRID[t_pos[0]][t_pos[1]] = TAIL
    GRID[h_pos[0]][h_pos[1]] = HEAD
    print(u'\u2500' * 10)
    print('\n'.join(''.join(row) for row in GRID))
    print(u'\u2500' * 10)
    return GRID


def move_head(position:tuple, direction:str, amount:int):
    #print(position, direction, amount)
    head_pos = (int(position[0]) + int(DIR[direction][1])*int(amount),int(position[1]) + int(DIR[direction][0])*int(amount))

    print(head_pos)
    return head_pos


def move_tail(head_pos):
    pass


def init():
    #for row in GRID:
        #if START in row:
            # position = col, row
            #head_pos = (GRID.index(row), row.index(START))
            #tail_pos = (GRID.index(row), row.index(START))
    return (0,0),(0,0)#head_pos, tail_pos


def solve(inp):
    data = inp.splitlines()
    # print(data)
    # part 1
    visited = set()
    HEAD_POS, TAIL_POS = init()
    draw_grid(HEAD_POS, TAIL_POS)
    for move in data:
        direction = move.split(" ")[0]
        amount = move.split(" ")[1]
        # print(direction,"x", amount)
        HEAD_POS = move_head(HEAD_POS, direction, amount)

    res1 = 0
    # part 2

    res2 = 0
    return f"The solution of part 1 is {res1}.\n The solution of part 2 is {res2}."


if __name__ == "__main__":
    start = pfc()
    solution = solve(read_file("input.txt"))
    print(f"Time elapsed: {pfc() - start}s")
    print(solution)
