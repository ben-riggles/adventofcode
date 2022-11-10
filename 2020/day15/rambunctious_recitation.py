import aoc


def play_game(starters: list[int], total_turns: int) -> int:
    ages = [0] * total_turns
    for turn, n in enumerate(starters[:-1], 1):
        ages[n] = turn

    prev = starters[-1]
    for turn in range(len(starters), total_turns):
        value = turn - ages[prev]
        if value == turn:
            value = 0
        
        ages[prev] = turn
        prev = value
    return value


def main():
    aoc.setup(__file__)
    starters = list(map(int, aoc.read_data().split(',')))
    aoc.answer(1, play_game(starters, 2020))
    aoc.answer(2, play_game(starters, 30_000_000))

if __name__ == '__main__':
    main()
