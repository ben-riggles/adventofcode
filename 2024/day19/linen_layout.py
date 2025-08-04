import aoc
import functools


def arrangements(design: str, patterns: list[str]) -> int:
    @functools.cache
    def _can_build(design: str):
        count = 1 if design in patterns else 0
        for p in (x for x in patterns if design.startswith(x)):
            count += _can_build(design[len(p):])
        return count
    return _can_build(design)


@aoc.register(__file__)
def answers():
    patterns, designs = aoc.read_chunks()
    patterns = [x.strip() for x in patterns.split(',')]
    designs = designs.splitlines()

    result = [arrangements(x, patterns) for x in designs]
    yield sum(True for x in result if x > 0)
    yield sum(result)

if __name__ == '__main__':
    aoc.run()
