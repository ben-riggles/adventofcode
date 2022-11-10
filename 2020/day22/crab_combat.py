from __future__ import annotations
import aoc
from dataclasses import dataclass, field
import re


@dataclass
class Player:
    id: int
    deck: list[int] = field(default_factory=list)

    @property
    def empty(self) -> bool:
        return len(self.deck) == 0

    def draw(self) -> int:
        return self.deck.pop(0)

    def top(self, amt: int) -> list[int]:
        return self.deck[:amt]

    def collect(self, cards: list[int]):
        self.deck.extend(cards)

    def score(self):
        return sum([(idx+1) * x for idx, x in enumerate(reversed(self.deck))])

    @staticmethod
    def from_string(player_str: str) -> Player:
        lines = player_str.splitlines()
        pid = re.match(r'Player (.*):', lines[0])[1]
        deck = [int(x) for x in lines[1:]]
        return Player(id=int(pid), deck=deck)

@dataclass
class Combat:
    p1: Player
    p2: Player

    def __iter__(self):
        return self

    def __next__(self):
        if self.p1.empty or self.p2.empty:
            raise StopIteration
        return self.p1.draw(), self.p2.draw()

    def play(self) -> Player:
        for card1, card2 in self:
            if card1 > card2:
                self.p1.collect([card1, card2])
            else:
                self.p2.collect([card2, card1])
        return self.p1 if self.p2.empty else self.p2


class RecursionError(Exception):
    def __init__(self):
        super().__init__('Game ended due to recursion')

@dataclass
class RecursiveCombat(Combat):
    memory: list = field(default_factory=list)
    
    def __next__(self):
        if (self.p1.deck, self.p2.deck) in self.memory:
            raise RecursionError()
        self.memory.append((self.p1.deck.copy(), self.p2.deck.copy()))
        return super().__next__()

    def play(self):
        try:
            for card1, card2 in self:
                if card1 <= len(self.p1.deck) and card2 <= len(self.p2.deck):
                    p1top, p2top = self.p1.top(card1), self.p2.top(card2)
                    sub_game = RecursiveCombat(p1=Player(1, p1top), p2=Player(2, p2top))
                    winner = sub_game.play().id
                elif card1 > card2:
                    winner = 1
                else:
                    winner = 2
                
                if winner == 1:
                    self.p1.collect([card1, card2])
                else:
                    self.p2.collect([card2, card1])
        except RecursionError:
            return self.p1
        return self.p1 if self.p2.empty else self.p2


def main():
    aoc.setup(__file__)
    player_data = aoc.read_chunks()

    p1, p2 = (Player.from_string(block) for block in player_data)
    winner1 = Combat(p1, p2).play()
    aoc.answer(1, winner1.score())

    p1, p2 = (Player.from_string(block) for block in player_data)
    winner2 = RecursiveCombat(p1, p2).play()
    aoc.answer(2, winner2.score())

if __name__ == '__main__':
    main()
