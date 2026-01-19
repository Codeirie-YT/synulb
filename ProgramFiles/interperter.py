# This runs the bytecode

# Libraries
import sys
from time import sleep
import time
from cFuncAndBuiltins import *
from compiler import token
#import importlib
#import pickle

# This allows for loops. The recursion limit is the number of times an 'infinite' loop can run before crashing.
# update: what the fuck
if sys.maxsize > 2**32: # If your python is running in 64-bits
    sys.setrecursionlimit((2*64)-1)
elif sys.maxsize == 2**32: # If you python is running in 32-bits
    sys.setrecursionlimit((2*32)-1)
elif sys.maxsize < 2**32: # if your computer is from 1999
    sys.setrecursionlimit(1000000)

classes = {} # Container for anything defined at runtime
variables = {} # name: storage

class error:
    def __init__(self, name: str, text: str):
        self.name = name
        self.text = text

    def __raise__(self):
        print(f'{self.name}: {self.text}')
        sleep(2)
        sys.exit(1)


def lineInterperet(line):
    global cFunction
    global instructionPointer

    cmd = line[0]
    attributes = line[1:]

    match cmd:
        case 'declare':
            name = attributes[0]
            _type =  attributes[1]

            if type(_type[0]) is token:
                _type = _type[0].value

            match _type:
                case 'cFunc' | 'cFunction' | 'classFunction':
                    classes[name] = cFunction(name, None, None, None)

                case 'int' | 'Integer':
                    variables[name] = Integer(undefined())

        case 'define':
            name = attributes[0]
            methods = attributes[1] # List of methods if a class
            data = attributes[2:]

            if not name in classes.keys() and not name in variables.keys():
                error('NotFoundError', f'Tried to define \'{name}\', which doesn\'t exist.')
            
            try:
                if not name in classes.keys():
                    c = type(variables[name])
                else:
                    c = type(classes[name])
                match c:
                    case _ if c is cFunction:
                        classes[name].code = data

                    case _ if c is Integer:
                        variables[name].value = hex(int(data[0][0].value))

                    case _:
                        error('TypeError', f'Tried to define a method of unknown type, {type(classes[name])}')
                    
            except KeyError:
                error('NotFoundError', f'Tried to define \'{name}\', which doesn\'t exist.')

        case 'call':
            name = attributes[0]
            peramiters = attributes[1]

            if not classes[name]:
                error('NotFoundError', 'Tried to call a cFunc that doesn\'t exist.')
            elif type(classes[name]) != cFunction:
                error('TypeError', f'{type(classes[name])} type is not callable.')
            
            cFuncCall: cFunction = classes[name]
            if cFuncCall.code and cFuncCall.code != [[]]:
                miniInterperet(cFuncCall.code)

        case 'write':
            to = attributes[0]
            data = attributes[1]

            match to:
                case 'console':
                    if type(data) == str:
                        sys.stdout.write(data)
                    elif type(data) == list:
                        sys.stdout.write(data[0])

                case _:
                    pass

        case 'import':
            file = attributes[0]
            try:
                file = open(f'{file}.py', 'r')
                exec(file.read())
                file.close()
            except Exception as e:
                print(e)

        case _:
            if builtins[cmd]:
                exec(builtins[cmd])
                return 0
            error('InstructionError', 'Instruction doesn\'t exist.')


def Interperet(bytecode: list, clock, start):
    if type(bytecode) == tuple:
        error("IOERROR", "Error occured when trying to read .dat (bytecode) file.")
    global instuctionPointer
    instructionPointer = 0

    global builtins # Builtin Functions and imported functions
    builtins = {}


    while True:
        try:
            LIvalue = lineInterperet(bytecode[instructionPointer])
        except IndexError:
            if clock:
                print(f'\n\nProgram finished in {(time.perf_counter_ns() - start) / (10**6)}ms.')
            #sys.exit(0)
            return

        if type(LIvalue) == error:
            LIvalue.__raise__()

        instructionPointer += 1

def miniInterperet(bytecode: list): # for running functions
    ip = 0

    while True:
        try:
            LIvalue = lineInterperet(bytecode[0][ip])
        except IndexError:
            return 0

        if type(LIvalue) == error:
            LIvalue.__raise__()

        ip += 1

def main():
    exeTime = True
    if exeTime:
        start = time.perf_counter_ns()
    # Get bytecode from example.bytecode using json
    frame = [
        ['declare', 'setup', 'cFunction'],
        ['declare', 'main', 'cFunction'],
        ['call', 'setup', [None]],
        ['call', 'main', [None]]
    ]

    hello_world = [
        ['declare', 'setup', 'cFunction'],
        ['declare', 'main', 'cFunction'],
        ['define', 'setup', None, [
        ]],
        ['call', 'setup', [None]],
        ['define', 'main', None, [
            ['write', 'console', "Hello, World!"],
        ]],
        ['call', 'main', [None]]
    ]


    hello_world_test = [
        ['write', 'console', "Hello, World!"]
    ]

    import_test = [
        ['declare', 'setup', 'cFunction'],
        ['declare', 'main', 'cFunction'],
        ['define', 'setup', None, [
            ['import', 'math']
        ]],
        ['call', 'setup', [None]],
        ['define', 'main', None, [
            ['math.saypi', None]
        ]],
        ['call', 'main', [None]]
    ]
    
    
    Interperet(hello_world, exeTime, start)

if __name__ == '__main__':
    main()