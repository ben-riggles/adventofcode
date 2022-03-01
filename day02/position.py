with open('day02/planned_course.txt') as f:
    commands = f.read().splitlines()

horizontal = 0
depth = 0
aim = 0

for cmd in commands:
    order, value = cmd.split()
    value = int(value)

    if order == 'forward':
        horizontal += value
        depth += aim * value
    elif order == 'up':
        aim -= value
    elif order == 'down':
        aim += value

print(horizontal, depth)
print(horizontal * depth)
