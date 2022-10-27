from __future__ import annotations
import itertools
import re
from typing import List, Set, Dict, Generator, Iterator


class RuleSet:
    def __init__(self, rules: List[int]):
        self.rules = rules

    def __repr__(self):
        return f'RuleSet({" ".join([str(x) for x in self.rules])})'

    def matches(self, rules: Dict[int, Rule], message: str) -> Generator[str]:
        yield from self._matches(rules, message)

    def _matches(self, rules: Dict[int, Rule], message: str, _match: str = '', idx: int = 0) -> Generator[str]:
        try:
            rule = rules[self.rules[idx]]
        except IndexError:
            yield _match
            return

        for match in rule.matches(rules, message):
            _message = message[len(match):]
            yield from self._matches(rules, _message, _match=_match + match, idx=idx+1)

    @staticmethod
    def from_string(_str: str) -> RuleSet:
        rules = [int(x) for x in _str.strip().split(' ')]
        return RuleSet(rules)


class Rule:
    def __init__(self, num:int, letter: str = None, rule_sets: List[RuleSet] = None):
        self.id = num
        self.letter = letter
        self.rule_sets = rule_sets

    def __repr__(self):
        return f'Rule({self.id})'

    def match(self, rules: Dict[int, Rule], message: str) -> bool:
        for m in self.matches(rules, message):
            if m == message:
                return True
        return False

    def matches(self, rules: Dict[int, Rule], message: str) -> Generator[str]:
        if self.letter is not None:
            if message.startswith(self.letter):
                yield self.letter
            return

        for rule_set in self.rule_sets:
            for match in rule_set.matches(rules, message):
                yield match

    @staticmethod
    def from_string(rule_str: str) -> Rule:
        rule_id, rule_str = rule_str.split(':')
        rule_id = int(rule_id)
        rule_str = rule_str.strip()

        m = re.match(r'\"(?P<letter>[a-z])\"', rule_str)
        if m is not None:
            return Rule(rule_id, letter=m.group('letter'))
            
        rule_sets = rule_str.split('|')
        rule_sets = [RuleSet.from_string(_set) for _set in rule_sets]
        return Rule(rule_id, rule_sets=rule_sets)


with open('2020/day19/data.txt') as f:
    rules, messages = f.read().split('\n\n')

rules = [Rule.from_string(line) for line in rules.split('\n')]
rules = {rule.id: rule for rule in rules}
messages = messages.split('\n')

valid_messages = [msg for msg in messages if rules[0].match(rules, msg)]
print(f'PART ONE: {len(valid_messages)}')

rules[8] = Rule.from_string('8: 42 | 42 8')
rules[11] = Rule.from_string('11: 42 31 | 42 11 31')
valid_messages = [msg for msg in messages if rules[0].match(rules, msg)]
print(f'PART TWO: {len(valid_messages)}')
