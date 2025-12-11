import aoc
from collections import defaultdict


def parse_connection(connection: str) -> tuple[str, frozenset[str]]:
    _in, _out = connection.split(':')
    _out = frozenset(x.strip() for x in _out.split())
    return _in, _out

def count_paths(connections: dict[str, frozenset[str]], start: str, end: str, required: set[str] = set()) -> int:
    cache = defaultdict(lambda: defaultdict(int))
    
    def __find_paths(device: str) -> dict[frozenset, int]:
        if device in cache:
            return cache[device]
        
        result = defaultdict(int)
        reqs = frozenset(required & {device,})
        if device == end:
            result[reqs] = 1
        else:
            for output in connections[device]:
                for k, v in __find_paths(output).items():
                    result[frozenset(k | reqs)] += v

        cache[device] = result
        return result
    
    paths = __find_paths(start)
    return paths[frozenset(required)]


@aoc.register(__file__)
def answers():
    connections = dict(parse_connection(x) for x in aoc.read_lines())
    yield count_paths(connections, 'you', 'out')
    yield count_paths(connections, 'svr', 'out', required={'dac', 'fft'})

if __name__ == '__main__':
    aoc.run()
