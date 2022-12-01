import aoc


@aoc.register(__file__)
def answers():
    cals_per_elf = [tuple(map(int, x.splitlines())) for x in aoc.read_chunks()]
    sum_per_elf = sorted([sum(x) for x in cals_per_elf])
    yield sum_per_elf[-1]
    yield sum(sum_per_elf[-3:])

if __name__ == '__main__':
    aoc.run()
