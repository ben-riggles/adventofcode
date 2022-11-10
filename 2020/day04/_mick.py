import re

with open("2020/day04/data.txt", "r") as f:
    passports = [p.replace('\n', ' ') for p in f.read().split('\n\n')]

dictionary = [d.split() for d in passports]
dictionary = [{y.split(":")[0]: y.split(":")[1] for y in x} for x in dictionary]
CREDENTIALS = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
COUNT = 0

def passport_check(list):
    precheck = []

    for entry in list:
        if entry.keys() >= CREDENTIALS:
            precheck.append(entry)

    return precheck


def passport_validate(passport):
    height_reg = re.compile("1[5-8]\dcm|19[0-3]cm|59in|6\din|7[0-6]in")
    eye_color = {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}
    hair_color = re.compile("#[0-9aA-fF]{6}$")
    passport_id = re.compile("[0-9]{9}$")

    if int(passport["byr"]) not in range(1920, 2003): return False
    if int(passport["iyr"]) not in range(2010, 2021): return False
    if int(passport["eyr"]) not in range(2020, 2031): return False
    if not bool(re.match(height_reg, passport["hgt"])): return False
    if not bool(re.match(hair_color, passport["hcl"])): return False
    if passport["ecl"] not in eye_color: return False
    if not bool(re.match(passport_id, passport["pid"])): return False

    return True

precheck = passport_check(dictionary)

for i in precheck:
    if passport_validate(i):
        COUNT += 1

print(COUNT)