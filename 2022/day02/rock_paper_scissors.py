import aoc
from enum import Enum, IntEnum
import numpy as np


class Option(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    def __int__(self):
        return self.value

    def __gt__(self, other):
        return self == other >> 1

    def __lt__(self, other):
        return self == other << 1

    def __lshift__(self, amt: int):
        retval = self
        for _ in range(amt):
            match (retval):
                case Option.ROCK: retval = Option.SCISSORS
                case Option.PAPER: retval = Option.ROCK
                case Option.SCISSORS: retval = Option.PAPER
        return retval

    def __rshift__(self, amt: int):
        retval = self
        for _ in range(amt):
            match (retval):
                case Option.ROCK: return Option.PAPER
                case Option.PAPER: return Option.SCISSORS
                case Option.SCISSORS: return Option.ROCK
        return retval

class Outcome(IntEnum):
    WIN = 6
    DRAW = 3
    LOSS = 0


@aoc.register(__file__)
def answers():
    rounds = np.array([x.split(' ') for x in aoc.read_lines()])
    
    choices = np.where((rounds == 'A') | (rounds == 'X'), Option.ROCK, -1)
    choices = np.where((rounds == 'B') | (rounds == 'Y'), Option.PAPER, choices)
    choices = np.where((rounds == 'C') | (rounds == 'Z'), Option.SCISSORS, choices)
    
    outcomes = np.where(choices[:,1] > choices[:,0], Outcome.WIN, Outcome.LOSS)
    outcomes = np.where(choices[:,1] == choices[:,0], Outcome.DRAW, outcomes)
    yield sum(outcomes) + sum(choices[:,1].astype(int))

    choices[:,1] = np.where(rounds[:,1] == 'X', choices[:,0] << 1, -1)
    choices[:,1] = np.where(rounds[:,1] == 'Y', choices[:,0], choices[:,1])
    choices[:,1] = np.where(rounds[:,1] == 'Z', choices[:,0] >> 1, choices[:,1])

    outcomes = np.where(choices[:,1] > choices[:,0], Outcome.WIN, Outcome.LOSS)
    outcomes = np.where(choices[:,1] == choices[:,0], Outcome.DRAW, outcomes)
    yield sum(outcomes) + sum(choices[:,1].astype(int))

if __name__ == '__main__':
    aoc.run()
