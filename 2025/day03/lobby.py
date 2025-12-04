import aoc


def turn_on(bank: str, count: int) -> int:
    joltage = ''
    for i in range(count-1, 0, -1):
        digit = max(bank[:-(i)])
        joltage += digit
        bank = bank[bank.index(digit)+1:]
    joltage += max(bank)
    return int(joltage)


@aoc.register(__file__)
def answers():
    banks = aoc.read_lines()
    yield sum(turn_on(x, count=2) for x in banks)
    yield sum(turn_on(x, count=12) for x in banks)

if __name__ == '__main__':
    aoc.run()
