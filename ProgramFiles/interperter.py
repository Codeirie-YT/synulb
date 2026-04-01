# This runs the bytecode

# Libraries
import sys
from time import sleep
import time
from cFuncAndBuiltins import *
from compiler import token
from helper import *
#import importlib
#import pickle



classes = {} # Container for anything defined at runtime
variables = {} # name: storage

#class error:
#    def __init__(self, name: str, text: str):
#        self.name = name
#        self.text = text

#    def __raise__(self):
#        print(f'{self.name}: {self.text}')
#        sleep(2)
#        sys.exit(1)

def getInstanceOf(name):
    match name:
        # Every builtin has three names:
        # The informal name, which is used to actually identify builtins,
        # The formal name, which is used for errors,
        # and the specific name, which is completly optional
        case 'cFunc' | 'cFunction' | 'classFunction':
            return cFunction(name, None, None, None)

        case 'int' | 'Integer' | 'int32':
            return Integer(undefined())
        
        case 'char' | 'Character' | 'uint8':
            return Character(undefined())

def getItem(name):
    if name in classes.keys():
        return classes[name]
    elif name in variables.keys():
        return variables[name]
    else:
        error(f'{name} does not exist.', 6)

def itemExists(name):
    return True if name in classes.keys() or name in variables.keys() else False
    
def lineInterperet(line):
    '''Interperets one line of code'''
    
    global cFunction
    global instructionPointer
    try:
        cmd = line[0]
        attributes = line[1:]
    except TypeError:
        error('Expected a line of code, got token instead.', 1)

    match cmd:
        case 'declare':
            name = attributes[0]
            _type =  attributes[1]

            if type(_type[0]) is token:
                _type = _type[0].value

            match _type:
                case 'cFunc' | 'cFunction' | 'classFunction':
                    classes[name] = getInstanceOf('cFunc')

                case _:
                    variables[name] = getInstanceOf(_type)

        case 'define':
            name = attributes[0]
            methods = attributes[1] # List of methods if a class
            data = attributes[2:]

            if not itemExists(name):
                error(f'Tried to define \'{name}\', which doesn\'t exist.', 6)
            
            if not name in classes.keys():
                c = type(variables[name])
            else:
                c = type(classes[name])
            
            if c is cFunction:
                classes[name].code = data

            elif c is Integer:
                variables[name].value = hex(int(data[0][0].value))

            else:
                error(f'Tried to define a method of unknown type, {type(classes[name])}', 3)

        case 'call':
            name = attributes[0]
            peramiters = attributes[1]

            if not classes[name]:
                error('Tried to call a cFunc that doesn\'t exist.', 6)
            elif type(classes[name]) != cFunction:
                error(f'{type(classes[name])} type is not callable.', 3)
            
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

                    elif type(data) == token: # oh boy
                        match data.type:
                            case '<word>':
                                lineInterperet(['write', 'console', getItem(data.value)])
                            case _:
                                error(f'Expected a printable object when writing to the console, instead got a token of type {data.type} and a value {data.value}', 1)

                    elif type(data) == list:
                        for item in data:
                            lineInterperet(['write', 'console', item])

                    elif type(data) == Integer:
                        sys.stdout.write(str(data.__int__()))

                    elif type(data) == Character:
                        sys.stdout.write(data.__char__())

                    else:
                        print(data)
                        sleep(10)

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
            error('Instruction doesn\'t exist.', 6)


def Interperet(bytecode: list, clock, start):
    #if type(bytecode) == tuple:
    #    error("IOERROR", "Error occured when trying to read .dat (bytecode) file.")
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