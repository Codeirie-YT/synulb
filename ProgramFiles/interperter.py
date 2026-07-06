# This runs the bytecode

# Libraries
import sys
from time import sleep
import time
from cFuncAndBuiltins import *
from compiler import token
from helper import *
from sys import stdin, stdout
from io import TextIOWrapper
#import importlib
#import pickle

stdout = TextIOWrapper(stdout.buffer, stdout.encoding, line_buffering=False, write_through=False)

classes = {
    'console': mergeio(stdin, stdout)
} 
# Container for anything defined at runtime
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
        
        case 'str' | 'String' | 'pyStrWrapper':
            return String(undefined())
        
        case 'bool' | 'Boolean' | 'pyBoolWrapper':
            return Boolean(undefined())
        
        case _:
            cfunc = getItem(name)
            return cFunction(f'{name}Instance', cfunc.code, cfunc.value, cfunc.methods)

def getObject(_token):
    if type(_token) is not token:
        error(f"Tried to create an object from a token but got {str(_token)} instead.", 1)
    else:
        inst = getInstanceOf(_token.type[1:-1])
        if _token.type == '<bool>':
            match _token.value:
                case 'true':
                    inst.value = True
                
                case 'false':
                    inst.value = False
                
                case _:
                    error(f'{_token.value} is not a value.', 3)
        
        elif _token.type == '<str>':
            replace = {
                r'\n': '\n',
                r'\t': '\t'
            }

            for excape, unicode in replace.items():
                _token.value = _token.value.replace(excape, unicode)

            inst.value = _token.value

        elif _token.type == '<int>':
            inst.value = hex(int(_token.value))[2:]
        else:
            inst.value = _token.value

    return inst

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

            if type(_type) is token:
                pass
            elif type(_type[0]) is token:
                _type = _type[0].value

            match _type:
                case 'cFunc' | 'cFunction' | 'classFunction':
                    classes[name] = getInstanceOf('cFunc')

                case _:
                    variables[name] = getInstanceOf(_type.value)

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

            elif cFunction in c.__bases__:
                variables[name].value = getObject(data[0]).value

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
            data = attributes[1] # [<data>, <flush>=true]

            if len(data) > 1:
                flush = bool(getObject(data[1]))
            else:
                flush = True

            data = data[0]

            to = getItem(to)

            # Write Data
            if type(data) == token:
                match data.type:
                    case '<word>':
                        lineInterperet(['write', attributes[0], [getItem(data.value)]])
                    case _:
                        to.write(str(getObject(data)))
                        #error(f'Expected a writable object when writing, instead got a token of type {data.type} and a value {data.value}', 1)

            elif type(data) == list:
                for item in data:
                    lineInterperet(['write', attributes[0], [item, Boolean(False)]])

            else:
                if cFunction in data.__class__.__bases__:
                    to.write(str(data))
                else:
                    error(f'Attempted to write to {type(to)} named {attributes[0]} with type {type(data)}.', 3)

            if flush == True:
                to.flush()

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
            ['write', 'console', [String("Hello, World!")]],
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