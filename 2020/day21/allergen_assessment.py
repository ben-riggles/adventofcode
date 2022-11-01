from __future__ import annotations
from typing import Set, Tuple


def parse(food_str: str) -> Tuple[Set[str], Set[str]]:
    ingredients, allergens = food_str[:-1].split('(')
    ingredients = ingredients.strip().split(' ')
    allergens = [x.strip() for x in allergens.replace('contains', '').split(',')]
    return set(ingredients), set(allergens)


with open('2020/day21/data.txt') as f:
    foods = [parse(line) for line in f.read().splitlines()]

allergen_dict = {}
for ingredients, _allergens in foods:
    for allergen in _allergens:
        allergen_dict[allergen] = allergen_dict.get(allergen, ingredients) & ingredients

all_ingredients = set.union(*[f[0] for f in foods])
possible_allergens = set.union(*[v for v in allergen_dict.values()])
non_allergens = all_ingredients - possible_allergens
counter = sum([len(food[0] & non_allergens) for food in foods])
print(f'PART ONE: {counter}')


solved = {}
while allergen_dict:
    solved_allergens = [k for k,v in allergen_dict.items() if len(v) == 1]
    for allergen in solved_allergens:
        ingredient = allergen_dict.pop(allergen)
        solved[allergen] = list(ingredient)[0]
        allergen_dict = {k: v - ingredient for k, v in allergen_dict.items()}

dangerous = [solved[x] for x in sorted(solved.keys())]
print(f'PART TWO: {",".join(dangerous)}')
