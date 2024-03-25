import time

def hand2hex(hand):
    """
    Translate the alphabetical cards to hex numbers according to their value.
    """
    translation_mapping = {'T': 'A', 
                           'J': 'B', 
                           'Q': 'C', 
                           'K': 'D', 
                           'A': 'E'}
    translated_hand = ''.join(translation_mapping.get(card, card) for card in hand)
    return translated_hand

def p2_translation(hand):
    """
    Normally: 2, 3, 4, 5, 6, 7, 8, 9, T, J, Q, K, A
    Special: J, 2, 3, 4, 5, 6, 7, 8, 9, T, Q, K, A
    """
    translation_mapping_2 = {   '2': 'J',
                                '3': '2',
                                '4': '3',
                                '5': '4',
                                '6': '5',
                                '7': '6',
                                '8': '7',
                                '9': '8',
                                'T': '9',
                                'J': 'T',
                                'Q': 'Q',
                                'K': 'K',
                                'A': 'A'}
    translated_hand = ''.join(translation_mapping_2.get(card, card) for card in hand)
    return translated_hand



def rank_hand(hand):
    """
    Every card in the hand gets the count of its occurences in the hand. Therefore, every hand type has a different value.
        Eligible values: [5, 7, 9, 11, 13, 17, 25]
        Example: AKK12 -> [1,2,2,1,1] -> 1+2+2+1+1 = 7 [one pair]
    """
    return sum(hand.count(element) for element in hand)

def part1(hands): 
    """
    Determine the hand types and sort same types by their hex value. 
    """
    ranks = dict(sorted({hand: rank_hand(hand) for hand in hands}.items(), key=lambda x: x[1]))
    hands = [sorted([hand for hand, rank in ranks.items() if rank == r], key=lambda x: int(hand2hex(x), 15)) for r in sorted(set(ranks.values()))]
    
    # Flatten the list
    hands = [hand for rank in hands for hand in rank]
    
    return hands

def part2(hands):
    ranks = {}
    for hand in hands:
        js = hand.find("J")
        num_j = hand.count("J")
        if num_j > 0:
            cs = {element: hand.count(element) for element in hand}
            
            cs["J"] = 0
            
            cs = dict(sorted(cs.items(), key=lambda x: x[1]))
            del cs["J"]
            ks, vs = list(cs.keys()), list(cs.values())
            if len(ks) == 0:
                cs = {"A": num_j}
            else:
                vs[-1] += num_j
                cs = dict(list(zip(ks, vs))            )
            
            new_hand = "".join([k*v for k, v in cs.items()])
            rank = rank_hand(new_hand)
        else:
            rank = rank_hand(hand)
        ranks[hand] = rank

    
    hands = [sorted([hand for hand, rank in ranks.items() if rank == r], key=lambda x: int(hand2hex(p2_translation(x)), 15)) for r in sorted(set(ranks.values()))]
    hands = [hand for rank in hands for hand in rank]
    return hands

def calculate(data):
    hands = [x.split()[0] for x in data.splitlines()]
    bids = {x.split()[0]: int(x.split()[1]) for x in data.splitlines()}
    hands_p1 = part1(hands)
    hands_p2 = part2(hands)
    
    p1 = sum((i + 1) * bids[hand] for i, hand in enumerate(hands_p1))

    p2 = sum((i + 1) * bids[hand] for i, hand in enumerate(hands_p2))

    return p1, p2
    


if __name__ == "__main__":
    with open("input.txt") as f:
        data = f.read().strip()

    s1 = time.time()
    answer_1 = calculate(data)[0]
    s2 = time.time()
    print(f"Answer 1: {answer_1}")

    s3 = time.time()
    answer_2 = calculate(data)[1]
    s4 = time.time()
    print(f"Answer 2: {answer_2}")    
    
    print(f'Times: {(s2-s1)*1000:.4f}ms, {(s4-s3)*1000:.4f}ms')
