# This runs the bytecode

# Libraries
import sys
from time import sleep
import time
#import importlib
#import pickle

# This allows for loops. The recursion limit is the number of times an 'infinite' loop can run before crashing.
if sys.maxsize > 2**32: # If your python is running in 64-bits
    sys.setrecursionlimit((2*64)-1)
elif sys.maxsize == 2**32: # If you python is running in 32-bits
    sys.setrecursionlimit((2*32)-1)
elif sys.maxsize < 2**32: # if your computer is from 1999
    sys.setrecursionlimit(1000000)

classes = {} # Container for anything defined at runtime

class error:
    def __init__(self, name: str, text: str):
        self.name = name
        self.text = text

    def __raise__(self):
        print(f'{self.name}: {self.text}')
        sleep(2)
        sys.exit(1)

class cFunction:  # Class function
    def __init__(self, name: str, code: list, value: any, methods: dict):
        self.name = name
        self.code = code # Bytecode 
        self.value = value # Value for datatypes
        self.methods = methods # Methods for classes

class externalFunction:  # create a builtin function that runs python code
    def __init__(self, name: str, code: str):
        self.name = name
        self.code = code # python code

class Integer(cFunction):
    def __init__(self, value: str = '0x0', refcount: int = 0):
        self.name = '8int'
        self.code = None # None, it's written here in python.
        self.value = value
        self.refcount = refcount

    def __int__(self):
        '''Returns a python integer for the value.'''
        return int(self.value, 16)
    
    def increment(self):
        self.value = hex(self.__int__() + 1)

    def decrement(self):
        self.value = hex(self.__int__() - 1)

    def __del__(self): # I have no idea what I was doing here
        #from random import randint
        #if refcount > 0:
        #  exec(f'{''.join((chr(randint(65, 90)) for x in [0] * 20))} = {self}') # WHAT DOES THIS MEAN????
        pass
    
def lineInterperet(line):
    global cFunction
    global instructionPointer

    cmd = line[0]
    attributes = line[1:]

    match cmd:
        case 'declare' | 0:
            name = attributes[0]
            _type =  attributes[1]

            match _type:
                case 'cFunc' | 'cFunction' | 'classFunction':
                    classes[name] = cFunction(name, None, None, None)

        case 'define' | 1:
            name = attributes[0]
            methods = attributes[1] # List of methods if a class
            data = attributes[2:]

            if not classes[name]:
                return error('NotFoundError', 'Tried to define an object that doesn\'t exist.')

            c = type(classes[name])
            match type(classes[name]):
                case c if c is cFunction:
                    classes[name] = cFunction(name, data, None, None)

                case _:
                    return error('TypeError', f'Tried to define a method of unknown type, {type(classes[name])}')

        case 'call' | 2:
            name = attributes[0]
            peramiters = attributes[1]

            if not classes[name]:
                return error('NotFoundError', 'Tried to call a cFunc that doesn\'t exist.')
            elif type(classes[name]) != cFunction:
                return error('WTFError', f'Tried to call a {type(classes[name])} as a function. WTF???')
            
            cFuncCall: cFunction = classes[name]
            if cFuncCall.code and cFuncCall.code != [[]]:
                miniInterperet(cFuncCall.code)

        case 'write' | 3:
            to = attributes[0]
            data = attributes[1]

            match to:
                case 'console':
                    if type(data) == str:
                        sys.stdout.write(data)

                case _:
                    pass

        case 'import' | 4:
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
            return error('InstructionError', 'Instruction doesn\'t exist.')


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
            sys.exit(0)

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
    #main()
    x = Integer('0x05')
    print(x.__int__())