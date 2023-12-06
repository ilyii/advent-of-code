import time




if __name__ == "__main__":
    with open("input.txt") as f:
        data = f.read().strip()

    s1 = time.time()
    answer_1 = "TODO"
    s2 = time.time()
    print(f"Answer 1: {answer_1}")

    s3 = time.time()
    answer_2 = "TODO"
    s4 = time.time()
    print(f"Answer 2: {answer_2}")    
    
    print(f'Times: {(s2-s1)*1000:.4f}ms, {(s4-s3)*1000:.4f}ms')
