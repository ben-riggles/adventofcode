import atexit
import inspect
from pathlib import Path
import os
import re
import time


def _data_file(filename) -> str:
    main_file = Path(inspect.stack()[2].filename)
    _print_header(main_file)
    return str(main_file.parent.joinpath(f'{filename}.txt'))

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


def _print_header(main_file: Path):
    try:
        main_file = main_file.relative_to(os.getcwd())
    except ValueError:
        pass
    info = re.match(r'(?P<year>\d+)\\day(?P<day>\d+)\\(?P<filename>.*).py', str(main_file)).groupdict()

    print(f'********************************************')
    print(f'** {info["year"]}/day{info["day"]}: {info["filename"].replace("_", " ").title()}')

def answer(part_no: int, result):
    words = {1: 'ONE', 2: 'TWO'}
    print(f'PART {words[part_no]}: {result}')

START_TIME = time.process_time()
@atexit.register
def print_runtime():
    elapsed = time.process_time() - START_TIME
    print(f'Time elapsed: {round(elapsed * 1000, 3)} ms')

def reset_timer():
    global START_TIME
    START_TIME = time.process_time()
