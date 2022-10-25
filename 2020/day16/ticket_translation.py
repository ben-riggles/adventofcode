from __future__ import annotations
from functools import reduce
import numpy as np
import re
from typing import Set, List


class Field:
    def __init__(self, name: str, values: Set[int]):
        self.name: str = name
        self.values: Set[int] = values
        self.idx: int = -1

    def __eq__(self, other: Field) -> bool:
        return self.name == other.name

    def match(self, other: Set[int]) -> bool:
        return other <= self.values

    @staticmethod
    def parse(field_str: str) -> Field:
        m = re.match(r'(?P<name>.*): (?P<min_a>.*)-(?P<max_a>.*) or (?P<min_b>.*)-(?P<max_b>.*)', field_str)
        result = m.groupdict()

        set_a = set(range(int(result['min_a']), int(result['max_a']) + 1))
        set_b = set(range(int(result['min_b']), int(result['max_b']) + 1))
        return Field(name=result['name'], values=set_a | set_b)


class Ticket:
    def __init__(self, values: List[int]):
        self.values = values

    def error_rate(self, valid_values: Set[int]) -> int:
        return sum(x for x in self.values if x not in valid_values)

    @staticmethod
    def parse(ticket_str: str) -> Ticket:
        values = [int(x) for x in ticket_str.split(',')]
        return Ticket(values)


with open('2020/day16/data.txt') as f:
    fields, my_ticket, tickets = f.read().split('\n\n')

fields = fields.splitlines()
my_ticket = my_ticket.splitlines()[1]
tickets = tickets.splitlines()[1:]

fields = [Field.parse(f) for f in fields]
valid_values = set.union(*[x.values for x in fields])

tickets = [Ticket.parse(t) for t in tickets]
error = sum(t.error_rate(valid_values) for t in tickets)
print(f'PART ONE: {error}')


valid_tickets = [t for t in tickets if t.error_rate(valid_values) == 0]
value_grid = np.array([t.values for t in valid_tickets]).T
ticket_fields = {idx: set(x) for idx, x in enumerate(value_grid)}


def next_field(fields: List[Field], current: Field) -> Field | None:
    curr_idx = fields.index(current)
    next_idx = curr_idx + 1
    while next_idx != curr_idx:
        next_idx %= len(fields)
        if fields[next_idx].idx < 0:
            return fields[next_idx]
        next_idx += 1
    return None

field = fields[0]
while field is not None:
    matches = [idx for idx, x in ticket_fields.items() if field.match(x)]
    if len(matches) == 0:
        raise Exception('We failed')
    elif len(matches) == 1:
        field.idx = matches[0]
        ticket_fields.pop(field.idx)
    field = next_field(fields, field)

my_ticket = Ticket.parse(my_ticket)
departure_fields = [f for f in fields if f.name.startswith('departure')]
departure_values = [my_ticket.values[f.idx] for f in departure_fields]
my_departure = reduce(lambda x,y: x*y, departure_values)
print(f'PART TWO: {my_departure}')
