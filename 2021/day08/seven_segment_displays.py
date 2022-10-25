from enum import Enum, auto

class Position(Enum):
    TOP = auto()
    TOP_RIGHT = auto()
    BOT_RIGHT = auto()
    BOTTOM = auto()
    BOT_LEFT = auto()
    TOP_LEFT = auto()
    MIDDLE = auto()

class Display:
    def __init__(self, input_str):
        input, output = input_str.split('|')

        self.output = [set(x) for x in output.strip().split()]
        self.positions = self.determine_pos(input.strip().split())
        print(self.positions)

    @staticmethod
    def determine_pos(inputs):
        inputs = sorted(inputs, key=len)
        inputs = [set(x) for x in inputs]

        (top,) = inputs[1] - inputs[0]   # The two shortest are 1 and 7
        mid_tLeft = inputs[2] - inputs[0]   # The diff between 1 and 4
        mid_bot = (inputs[3] & inputs[4] & inputs[5]) - set(top)   # Top, middle, bottom are common between 2, 3, and 5
        (mid,) = mid_tLeft & mid_bot
        (tLeft,) = mid_tLeft - set(mid)
        (bot,) = mid_bot - set(mid)
        five = [x for x in inputs[3:6] if tLeft in x][0]   # Five is only of 2, 3, 5 missing the top left
        (bRight,) = five - {top, tLeft, mid, bot}
        (tRight,) = inputs[0] - set(bRight)
        (bLeft,) = inputs[-1] - {top, tLeft, mid, bot, bRight, tRight}

        return {
            Position.TOP: top,
            Position.TOP_RIGHT: tRight,
            Position.BOT_RIGHT: bRight,
            Position.BOTTOM: bot,
            Position.BOT_LEFT: bLeft,
            Position.TOP_LEFT: tLeft,
            Position.MIDDLE: mid
        }

    def determine_letter(self, output):
        if len(output) == 2:
            return 1
        elif len(output) == 3:
            return 7
        elif len(output) == 4:
            return 4
        elif len(output) == 5:
            if self.positions[Position.TOP_LEFT] in output:
                return 5
            elif self.positions[Position.BOT_LEFT] in output:
                return 2
            else:
                return 3
        elif len(output) == 6:
            if self.positions[Position.MIDDLE] not in output:
                return 0
            elif self.positions[Position.BOT_LEFT] in output:
                return 6
            else:
                return 9
        else:
            return 8

    def display_value(self):
        digits = [str(self.determine_letter(x)) for x in self.output]
        return int(''.join(digits))


with open('2021/day08/display_signals.txt') as f:
    signals = f.read().splitlines()

# Part 1
print('---------- Part 1 ----------')
count = 0
for signal in signals:
    outputs = signal.split('|')[1].strip().split()
    targets = sum([1 for x in outputs if len(x) in [2, 4, 3, 7]])
    count += targets

print(f'{count=}')


# Part 2
print('---------- Part 2 ----------')
displays = [Display(x).display_value() for x in signals]
print(displays)
print(sum(displays))
