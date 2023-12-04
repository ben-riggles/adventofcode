import aoc
from collections import defaultdict

@aoc.register(__file__)
def answers():
    cards = aoc.read_lines()

    score = 0
    copies = {x+1: 1 for x in range(len(cards))}
    for card in cards:
        card_id, numbers = card.split(': ')
        card_id = int(card_id.split()[1])

        winning, mine = numbers.split(' | ')
        winning = {int(x) for x in winning.strip().split()}
        mine = {int(x) for x in mine.strip().split()}

        num_matches = len(winning & mine)
        if num_matches:
            score += 2**(num_matches - 1)

            for new_copy in range(card_id + 1, card_id + num_matches + 1):
                if new_copy <= len(cards):
                    copies[new_copy] += copies[card_id]
    yield int(score)
    yield sum(copies.values())

if __name__ == '__main__':
    aoc.run()
