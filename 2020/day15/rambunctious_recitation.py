from lib2to3.pgen2.token import NUMBER


AGES = {}


with open('2020/day15/data.txt') as f:
    starters = [int(x) for x in f.read().split(',')]

NUMBER_OF_TURNS = 30000000

turn = 0
value = 0
next_turn = 0
while turn < NUMBER_OF_TURNS:
    try:
        value = starters.pop(0)
    except IndexError:
        value = next_turn
        
    next_turn = turn - AGES.get(value, turn)
    AGES[value] = turn
    turn += 1
print(f'PART ONE: {value}')
    