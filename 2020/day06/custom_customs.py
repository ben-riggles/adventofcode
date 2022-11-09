import aoc


def main():
    groups = [[set(x) for x in chunk.split('\n')] for chunk in aoc.read_chunks()]
    part1 = sum((len(set.union(*x)) for x in groups))
    part2 = sum((len(set.intersection(*x)) for x in groups))
    aoc.print_results(part1, part2)

if __name__ == '__main__':
    main()
