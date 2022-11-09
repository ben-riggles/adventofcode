import aoc


def play_game(starters: list[int], total_turns: int) -> int:
    asdf = starters.copy()

    ages = {}
    turn = 0
    value = 0
    next_turn = 0
    while turn < total_turns:
        try:
            value = asdf.pop(0)
        except IndexError:
            value = next_turn
            
        next_turn = turn - ages.get(value, turn)
        ages[value] = turn
        turn += 1
    return value

def main():
    starters = list(map(int, aoc.read_data().split(',')))
    part1 = play_game(starters, 2020)
    part2 = play_game(starters, 30_000_000)
    aoc.print_results(part1, part2)

if __name__ == '__main__':
    main()
    