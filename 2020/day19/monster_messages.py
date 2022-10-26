from __future__ import annotations
import itertools
import re
from typing import List, Set, Dict


RuleSet = List[int]

class Rule:
    def __init__(self, num:int, letter: str = None, rule_sets: List[RuleSet] = None):
        self.id = num
        self.letter = letter
        self.rule_sets = rule_sets
        self._memory = None

    def valid_messages(self, rules: Dict[int, Rule]) -> Set[str]:
        if self._memory is not None:
            return self._memory

        if self.letter is not None:
            self._memory = {self.letter}
            return self._memory

        valids = [Rule._valid_messages(rules, rule_set) for rule_set in self.rule_sets]
        self._memory = set.union(*valids)
        return self._memory

    @staticmethod
    def _valid_messages(rules: Dict[int, Rule], rule_set: RuleSet) -> Set[str]:
        valids = {''}
        for rule_id in rule_set:
            _msgs = rules[rule_id].valid_messages(rules)
            valids = {''.join(x) for x in (itertools.product(valids, _msgs))}
        return valids

    @staticmethod
    def from_string(rule_str: str) -> Rule:
        rule_id, rule_str = rule_str.split(':')
        rule_id = int(rule_id)
        rule_str = rule_str.strip()

        m = re.match(r'\"(?P<letter>[a-z])\"', rule_str)
        if m is not None:
            return Rule(rule_id, letter=m.group('letter'))
            
        rule_sets = rule_str.split('|')
        rule_sets = [[int(x) for x in _set.strip().split(' ')] for _set in rule_sets]
        return Rule(rule_id, rule_sets=rule_sets)


with open('2020/day19/data.txt') as f:
    rules, messages = f.read().split('\n\n')

rules = [Rule.from_string(line) for line in rules.split('\n')]
rules = {rule.id: rule for rule in rules}
messages = set(messages.split('\n'))

valid_rule0_msgs = rules[0].valid_messages(rules)
valid_messages = messages.intersection(valid_rule0_msgs)
print(f'PART ONE: {len(valid_messages)}')
