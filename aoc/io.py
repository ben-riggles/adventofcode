import atexit
from pathlib import Path
import os
import re
import time


START_TIME = None
MAIN_FILE = None

def setup(f: str):
    info = re.match(r'.*\\(?P<year>\d+)\\day(?P<day>\d+)\\(?P<filename>.*).py', f).groupdict()
    print(f'********************************************')
    print(f'** {info["year"]}/day{info["day"]}: {info["filename"].replace("_", " ").title()}')

    global START_TIME, MAIN_FILE
    START_TIME = time.process_time()
    MAIN_FILE = f

def _data_file(filename) -> str:
    return str(Path(MAIN_FILE).parent.joinpath(f'{filename}.txt'))

def read_data(filename='data') -> str:
    with open(_data_file(filename)) as f:
        data = f.read()
    return data

def read_lines(filename='data') -> list[str]:
    with open(_data_file(filename)) as f:
        data = f.read().splitlines()
    return data

def read_chunks(filename='data') -> list[str]:
    with open(_data_file(filename)) as f:
        data = f.read().split('\n\n')
    return data

NUM_WORDS = {1: 'ONE', 2: 'TWO'}
def answer(part_no: int, result):
    print(f'PART {NUM_WORDS[part_no]}: {result}')

@atexit.register
def print_runtime():
    elapsed = time.process_time() - START_TIME
    print(f'Time elapsed: {round(elapsed * 1000, 3)} ms')
