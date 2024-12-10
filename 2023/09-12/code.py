import time
import sys


def calculate(X, p2=False):
    if all(x==0 for x in X):
        return 0
    D = []
    for i in range(len(X)-1):
        D.append(X[i+1]-X[i])
    
    if p2:
        return X[0] + (-1)*calculate(D,p2=True)
    return X[-1] + calculate(D)


def manage(data, p2=False):
    data = [[int(x) for x in row.split()] for row in data.splitlines()]
    return sum([calculate(row, p2) for row in data])



if __name__ == "__main__":
    with open("input.txt") as f:
        data = f.read().strip()

    s1 = time.time()
    answer_1 = manage(data)
    s2 = time.time()
    print(f"Answer 1: {answer_1}")

    s3 = time.time()
    answer_2 = manage(data, True)
    s4 = time.time()
    print(f"Answer 2: {answer_2}")    
    
    print(f'Times: {(s2-s1)*1000:.4f}ms, {(s4-s3)*1000:.4f}ms')
