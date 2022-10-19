import re


def validity_minmax(line: str) -> bool:
    m = re.match(r'(?P<min>.*)-(?P<max>.*) (?P<letter>.*): (?P<password>.*)', line)
    assert m is not None
    min, max, letter, password = m.groups()
    return int(min) <= password.count(letter) <= int(max)


def validity_position(line: str) -> bool:
    m = re.match(r'(?P<first>.*)-(?P<second>.*) (?P<letter>.*): (?P<password>.*)', line)
    assert m is not None
    first, second, letter, password = m.groups()
    return (password[int(first)-1] == letter) ^ (password[int(second)-1] == letter)


with open('2020/day02/data.txt') as f:
    data = f.read().splitlines()

validity = [validity_minmax(x) for x in data]
print(f'PART ONE: {sum(validity)}')

validity = [validity_position(x) for x in data]
print(f'PART TWO: {sum(validity)}')