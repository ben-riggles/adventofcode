from __future__ import annotations
import aoc
from collections import Counter
from dataclasses import dataclass


@dataclass
class File:
    name: str
    size: int

class Directory:
    TOP_LEVEL: Directory = None

    def __init__(self, name: str, parent: Directory = None):
        self.name = name
        self.parent = parent
        self.content = {}

    def __repr__(self):
        return f'Directory({self.name})'

    def __getitem__(self, key: str):
        if key == '..':
            return self.parent
        elif key == '/':
            return Directory.TOP_LEVEL
        elif key not in self.content:
            self.content = Directory(name=key, parent=self)
        return self.content[key]

    def __setitem__(self, key: str, value):
        self.content[key] = value

    def add_content(self, content: list[str]):
        for line in content:
            a, b = line.split()
            if a == 'dir' and b not in self.content:
                self.content[b] = Directory(name=b, parent=self)
            else:
                self.content[b] = File(name=b, size=int(a))
        return self

    @property
    def full_name(self) -> str:
        if self == Directory.TOP_LEVEL:
            return '/'

        ancestor = self.parent
        retval = self.name
        while ancestor is not Directory.TOP_LEVEL:
            retval = f'{ancestor.name}/{retval}'
            ancestor = ancestor.parent
        return f'/{retval}'

    @property
    def size(self) -> int:
        return sum(x.size for x in self.content.values())

Directory.TOP_LEVEL = Directory(name='/')



def build_tree(commands: list[str]) -> dict:
    cwd = Directory.TOP_LEVEL

    for cmd in commands:
        if cmd.startswith('cd'):
            cwd = cwd[cmd.split()[-1]]
        elif cmd.startswith('ls'):
            cwd = cwd.add_content(cmd.splitlines()[1:])
    return Directory.TOP_LEVEL

def directory_sizes(folder: Directory) -> Counter[str]:
    retval = Counter({folder.full_name: folder.size})
    for child in folder.content.values():
        if isinstance(child, File):
            continue
        retval.update(directory_sizes(child))
    return retval


@aoc.register(__file__)
def answers():
    terminal = aoc.read_data().split('$ ')
    directory_tree = build_tree(terminal)
    sizes = directory_sizes(directory_tree)
    yield sum([x for x in sizes.values() if x <= 100_000])

    unused_space = 70_000_000 - sizes['/']
    needed_space = 30_000_000 - unused_space
    yield min([x for x in sizes.values() if x >= needed_space])

if __name__ == '__main__':
    aoc.run()
