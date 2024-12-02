import aoc


def is_safe(report: list[int], ignore_one: bool = False):
    def _check_level(idx: int, previous: int = None, direction: bool = None, ignore_used: bool = False) -> bool:
        try:
            value = report[idx]
        except IndexError:
            return True
        
        if ignore_one and not ignore_used and _check_level(idx+1, previous, direction, True):
            return True
        
        if previous is None:
            return _check_level(idx+1, value, None, ignore_used)
        
        diff = previous - value
        dir = diff > 0
        if (direction is None or direction == dir) and 1 <= abs(diff) <= 3:
            return _check_level(idx+1, value, dir, ignore_used)
        
        return False
        
    return _check_level(0)

@aoc.register(__file__)
def answers():
    reports = [list(map(int, x.split())) for x in aoc.read_lines()]

    # Part One
    safe_reports = [is_safe(x) for x in reports]
    yield sum(safe_reports)

    # Part Two
    safe_reports = [is_safe(x, ignore_one=True) for x in reports]
    yield sum(safe_reports)

if __name__ == '__main__':
    aoc.run()
