import inspect
from pathlib import Path
import os
import re


def print_results(part1, part2):
    main_file = Path(inspect.stack()[2].filename)
    try:
        main_file = main_file.relative_to(os.getcwd())
    except ValueError:
        pass
    info = re.match(r'(?P<year>\d+)\\day(?P<day>\d+)\\(?P<filename>.*).py', str(main_file)).groupdict()
    print(f'********************************************')
    print(f'** {info["year"]}/day{info["day"]}: {info["filename"].replace("_", " ").title()}')
    print(f'PART ONE: {part1}')
    print(f'PART TWO: {part2}')