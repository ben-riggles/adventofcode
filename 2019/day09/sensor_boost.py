import aoc
from aoc.vm import IntcodeVM


@aoc.register(__file__)
def answers():
    intcode = list(map(int, aoc.read_data().split(',')))
    
    testVM = IntcodeVM(intcode)
    while testVM.running:
        out = testVM.run(1)
    yield out
    
    trueVM = IntcodeVM(intcode)
    while trueVM.running:
        out = trueVM.run(2)
    yield out 
    

if __name__ == '__main__':
    aoc.run()
