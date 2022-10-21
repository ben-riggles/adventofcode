import numpy as np


with open('2020/day13/data.txt') as f:
    init_time, schedule = f.read().splitlines()

init_time = int(init_time)
bus_ids = np.array(schedule.split(','))
bus_ids = bus_ids[bus_ids != 'x'].astype(int)

distances = bus_ids - (init_time % bus_ids)
idx = np.where(distances == min(distances))
nearest_bus = bus_ids[idx][0]
wait_time = distances[idx][0]
print(f'PART ONE: {nearest_bus * wait_time}')
