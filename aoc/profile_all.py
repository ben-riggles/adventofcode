from aoc.io import print_runtime
import cProfile
from importlib import import_module
from pathlib import Path
import sys


if __name__ == '__main__':
    py_files = list(Path('.').glob('**/*.py'))
    pythonpath = sys.path.copy()

    for f in py_files:
        if 'aoc' in str(f) or '2021' in str(f) or f.stem.startswith('_'):
            continue
        if 'day20' not in str(f):
            continue
        
        sys.path = [str(f.parent)] + pythonpath
        mod_name = str(f).replace('.py', '').replace('\\', '.')
        mod = import_module(mod_name)
        try:
            main_fn = getattr(mod, 'main')
        except AttributeError:
            continue

        pr = cProfile.Profile()
        pr.enable()
        main_fn()
        pr.disable()

        print_runtime()
        output = f.parent.joinpath(f'{f.stem}.pstats')
        pr.dump_stats(str(output))
