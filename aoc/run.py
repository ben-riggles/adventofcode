import argparse
import cProfile
from pathlib import Path

from aoc.io import set_main_file
from aoc.register import registered_functions


NUM_WORDS = {1: 'ONE', 2: 'TWO'}
def run(profile: bool = False):
    for func, filename in registered_functions().items():
        set_main_file(filename)

        if profile:
            pr = cProfile.Profile()
            pr.enable()
        
        for i, answer in enumerate(func()):
            print(f'PART {NUM_WORDS[i+1]}: {answer}')

        if profile:
            pr.disable()
            f = Path(filename)
            output = f.parent.joinpath(f'{f.stem}.pstats')
            pr.dump_stats(str(output))
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run advent of code files')
    parser.add_argument('-y', '--year', help='The year to run', type=int)
    parser.add_argument('-p', '--profile', help='Profile the run', default=False, action='store_true')
    args = vars(parser.parse_args())

    if (year := args.pop('year')) is not None:
        __import__(year)
    else:
        __import__('2020')
    run(**args)
