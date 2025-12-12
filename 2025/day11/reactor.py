import aoc
import functools


def parse_connection(connection: str) -> tuple[str, frozenset[str]]:
    _in, _out = connection.split(':')
    _out = frozenset(x.strip() for x in _out.split())
    return _in, _out

def count_paths(connections: dict[str, frozenset[str]], start: str, end: str, required: set[str] = set()) -> int:
    @functools.cache
    def __paths(device: str, reqs: frozenset[str]) -> dict[frozenset, int]:
        reqs -= {device}
        if device == end:
            return 0 if reqs else 1
        return sum(__paths(x, reqs) for x in connections[device])
    
    return __paths(start, frozenset(required))


@aoc.register(__file__)
def answers():
    connections = dict(parse_connection(x) for x in aoc.read_lines())
    yield count_paths(connections, 'you', 'out')
    yield count_paths(connections, 'svr', 'out', required={'dac', 'fft'})

if __name__ == '__main__':
    aoc.run()
