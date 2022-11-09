import inspect
from pathlib import Path


def _data_file(filename) -> str:
    main_file = Path(inspect.stack()[2].filename)
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
