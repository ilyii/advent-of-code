import re
import time
from collections import defaultdict


def calculate(data):

    
    total = 0
    num_cards = defaultdict(int)
    for i, line in enumerate(data):
        num_cards[i] += 1
        id, wins, cands = re.split(': | \| ', line)
        id = int(re.findall('\d+', id)[0])
        wins, cands = wins.split(), cands.split()
        intersection = len(list(set(cands) & set(wins)))

        # Part 1
        if intersection > 0:          
            total += 2**(intersection-1)
        
        # Part 2
        for card in range(id, id+intersection):
            num_cards[card] += num_cards[i]



    return total, sum(num_cards.values())



if __name__ == "__main__":
    """
    Part 1:
        1. Split the input into the id (scorecard number), wins (winning numbers) and candidates (drawn numbers). 
        2. Create 2 sets (as it seems, the numbers are drawn without replacement) and find the intersection.
        3. Calculate the points for each score with the formula 2^(intersection-1) and sum them up.

    Part 2:
        1. + 2. is the identical to part 1.
        3. Create a dictionary to track the count of each scorecard. The count is calculated by using the following idea:
            - The number of matches between wins and candidates is the number of subsequent scorecards that are drawn additionally (e.g. Scorecard 1 has 3 Matches -> Draw 2,3,4 additionally).
            - Since every scorecard can cause additional draws, one needs to add the count of the current scorecard to the count of its subsequent scorecards according to its number of matches.
            - In addition, every scorecard is at least drawn once, so the count of the current scorecard is increased by 1.

    """
    with open("input.txt") as f:
        data = f.read().strip()

    s1 = time.time()
    answer_1, answer_2 = calculate(data.splitlines())
    s2 = time.time()
    print(f"Answer 1: {answer_1}")
    print(f"Answer 2: {answer_2}")
    print(f"Took {(s2-s1)*1000:.4f} ms.")  
