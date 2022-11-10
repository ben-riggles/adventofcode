import aoc


def main():
    aoc.setup(__file__)
    groups = [[set(x) for x in chunk.split('\n')] for chunk in aoc.read_chunks()]
    aoc.answer(1, sum((len(set.union(*x)) for x in groups)))
    aoc.answer(2, sum((len(set.intersection(*x)) for x in groups)))

if __name__ == '__main__':
    main()
