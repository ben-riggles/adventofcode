from ast import literal_eval
import re
from typing import Dict


def line_to_dict(line: str) -> Dict[str, str]:
    line = '{"' + line.replace('\n', '","').replace(':', '":"').replace(' ', '","') + '"}'
    return literal_eval(line)


REQUIRED_FIELDS = {'ecl', 'pid', 'eyr', 'hcl', 'byr', 'iyr', 'hgt'}
def check_fields(passport: Dict[str, str]) -> bool:
    return passport.keys() >= REQUIRED_FIELDS


EYE_COLORS = {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}
def check_data(passport: Dict[str, str]) -> bool:
    try:
        if not 1920 <= int(passport['byr']) <= 2002: return False
        if not 2010 <= int(passport['iyr']) <= 2020: return False
        if not 2020 <= int(passport['eyr']) <= 2030: return False

        height, unit = int(passport['hgt'][:-2]), passport['hgt'][-2:]
        if unit not in ['cm', 'in']: return False
        if unit == 'cm' and not 150 <= height <= 193: return False
        if unit == 'in' and not 59 <= height <= 76: return False

        if not re.match(r'#[0-9a-f]{6}$', passport['hcl']): return False
        if not passport['ecl'] in EYE_COLORS: return False
        if not re.match(r'[0-9]{9}$', passport['pid']): return False
    except (KeyError, ValueError, TypeError, IndexError):
        return False
    return True


with open('2020/day04/data.txt') as f:
    passports = [line_to_dict(line) for line in f.read().split('\n\n')]

valid_passports = [x for x in passports if check_fields(x)]
print(f'PART ONE: {len(valid_passports)}')

valid_passports = [x for x in valid_passports if check_data(x)]
print(f'PART TWO: {len(valid_passports)}')
