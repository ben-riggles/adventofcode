import aoc


def read_rotation(rotation: str) -> int:
    direction, value = rotation[0], int(rotation[1:])
    return value if direction == 'R' else -value

def password_one(rotations: list[int], start: int) -> int:
    dial, zeros = start, 0
    for rotation in rotations:
        dial = (dial + rotation) % 100
        if dial == 0:
            zeros += 1
    return zeros

def password_two(rotations: list[int], start: int) -> int:
    dial, zeros = start, 0
    for rotation in rotations:
        if dial == 0 and rotation < 0:
            dial = 100

        full_cycles, remainder = divmod(abs(rotation), 100)
        zeros += full_cycles
        dial += remainder if rotation > 0 else -remainder
        if dial <= 0 or dial >= 100:
            zeros += 1
        dial %= 100
    return zeros


@aoc.register(__file__)
def answers():
    rotations = [read_rotation(x) for x in aoc.read_lines()]
    yield password_one(rotations, start=50)
    yield password_two(rotations, start=50)

if __name__ == '__main__':
    aoc.run()
