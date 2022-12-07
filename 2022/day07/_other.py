from __future__ import annotations
import aoc
from collections import defaultdict


def cd(paths: dict, cwd: tuple, folder: str) -> tuple:
    if folder == '..': return cwd[:-1]
    if folder == '/': return tuple()

    paths[cwd].append(folder)
    return cwd + (folder,)

def ls(paths: dict, cwd: tuple, lines: str) -> tuple:
    for line in lines:
        a, _ = line.split()
        if 'dir' not in a:
            paths[cwd].append(int(a))
    return cwd

def build_tree(commands: list[str]) -> dict:
    paths = defaultdict(list)
    cwd = tuple()
    for cmd in commands:
        if cmd.startswith('cd'):
            cwd = cd(paths, cwd, cmd.split()[-1])
        elif cmd.startswith('ls'):
            cwd = ls(paths, cwd, cmd.splitlines()[1:])
    return paths

def size_report(paths: dict, folder: str) -> int:
    retval = 0
    for child in paths[folder]:
        if isinstance(child, int):
            retval += child
        else:
            retval += size_report(paths, folder + (child,))
    return retval


@aoc.register(__file__)
def answers():
    commands = aoc.read_data().split('$ ')
    path_tree = build_tree(commands)

    sizes = {folder: size_report(path_tree, folder) for folder in path_tree.keys()}
    yield sum(x for x in sizes.values() if x <= 100_000)

    needed_space = 30_000_000 - (70_000_000 - sizes[tuple()])
    yield min(x for x in sizes.values() if x >= needed_space)

if __name__ == '__main__':
    aoc.run()
