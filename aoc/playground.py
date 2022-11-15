import functools
import re
import time


ALL_FNS = []
from aoc.io import MAIN_FILE

def register(filename):
    def _register(func):
        @functools.wraps(func)
        def wrapper():
            info = re.match(r'.*\\(?P<year>\d+)\\day(?P<day>\d+)\\(?P<filename>.*).py', filename).groupdict()
            print(f'********************************************')
            print(f'** {info["year"]}/day{info["day"]}: {info["filename"].replace("_", " ").title()}')

            MAIN_FILE = filename

            start = time.process_time()
            for i, answer in enumerate(func()):
                print(f'PART {i}: {answer}')
            end = time.process_time()

            print(f'Time elapsed: {round((end - start) * 1000, 3)} ms')
        ALL_FNS.append(func)
        return wrapper
    return _register