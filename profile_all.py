from pathlib import Path
import os

py_files = list(Path('.').glob('**/*.py'))

for f in py_files:
    if 'profile_all' in str(f) or '2021' in str(f):
        continue
    output = f.parent.joinpath(f'{f.stem}.pstats')
    print(f'**** {str(f)}')
    os.system(f'python -m cProfile -o {output.as_posix()} {f.as_posix()}')
