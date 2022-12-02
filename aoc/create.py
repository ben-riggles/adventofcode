import argparse
from pathlib import Path
import shutil


def create(year: int, day: int, name: str):
    year_dir = Path.cwd().joinpath(str(year))
    year_md = year_dir.joinpath('README.md')
    if not year_dir.exists():
        year_dir.mkdir()
        template_init = Path.cwd().joinpath('aoc/template_init.py')
        dest_init = year_dir.joinpath('__init__.py')
        shutil.copy(str(template_init), str(dest_init))

        template_md = Path.cwd().joinpath('aoc/template_readme_year.md')
        shutil.copy(str(template_md), str(year_md))
        with open(str(year_md), mode='r+') as f:
            contents = f.read().replace('<<year>>', str(year))
            f.seek(0)
            f.write(contents)
        

    day_str = '{:02d}'.format(day)
    day_dir = year_dir.joinpath(f'day{day_str}')
    if day_dir.exists():
        raise Exception('Day already exists')
    day_dir.mkdir()

    with open(year_md, 'r+') as f:
        lines = f.read().splitlines()
        idx = next(i for i, x in enumerate(lines) if f'badge/{day_str}' in x)
        lines[idx] = f'[{lines[idx]}](day{day_str})'.replace('gray', 'green')
        f.seek(0)
        f.writelines('\n'.join(lines) + '\n')


    small_file = day_dir.joinpath('small.txt')
    data_file = day_dir.joinpath('data.txt')
    with open(small_file, mode='w') as f: pass
    with open(data_file, mode='w') as f: pass

    template_py = Path.cwd().joinpath('aoc/template_py.py')
    py_file = f'{name}.py'
    dest_py = day_dir.joinpath(py_file)
    shutil.copy(str(template_py), str(dest_py))

    day_md = day_dir.joinpath('README.md')
    template_md = Path.cwd().joinpath('aoc/template_readme_day.md')
    shutil.copy(str(template_md), str(day_md))
    with open(str(day_md), mode='r+') as f:
        contents = f.read().replace('<<year>>', str(year)).replace('<<day>>', str(day))
        contents = contents.replace('<<py_file>>', py_file).replace('<<title>>', name.replace('_', ' ').title())
        f.seek(0)
        f.write(contents)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a new Advent of Code folder and associated files')
    parser.add_argument('-y', '--year', help='The year to place the new files under', required=True, type=int)
    parser.add_argument('-d', '--day', help='The day to place the new files under', required=True, type=int)
    parser.add_argument('-n', '--name', help='The name of the new file', required=True)
    #args = vars(parser.parse_args())
    #create(**args)
    create(2024, 1, 'tester')
