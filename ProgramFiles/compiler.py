# Compiles the program into bytecode
# this is such bad code

import pickle
from sys import argv, maxsize, setrecursionlimit
from helper import *
from dataclasses import dataclass
argv = argv[1:]

# This allows for loops. The recursion limit is the number of times an 'infinite' loop can run before crashing.
if maxsize > 2**32: # If your python is running in 64-bits
    setrecursionlimit((2*64)-1)
elif maxsize == 2**32: # If you python is running in 32-bits
    setrecursionlimit((2*32)-1)
elif maxsize < (2**32)-1: # if your computer is from 1999
    setrecursionlimit(1000000)


class token:
    def __init__(self, _type, value):
        self.type = _type
        self.value = value

    def __str__(self):
        return f"{self.type} {self.value}"
    
    def __repr__(self):
        return self.__str__()

_match = {
    '@': '{decl}', 
    '$': '{defcFunc}', 
    '!': '{builtin}', 
    '>': '{wrt}', 
    '<': '{read}', 
    '%': '{method}', 
    '#': '{def}', 
    '^': '{flag}', 
    '&': '{clss}', 
    '-{': '{pramopen}', 
    '{': '{arryopen}', 
    '}': '{arryclse}', 
    '(': '{lparen}', 
    ')': '{rparen}', 
    ':;': '{void}', 
    ':': '{colon}', 
    ';': '{semi}', 
    ',': '{comma}', 
    '==': '{boolop}', 
    '=': '{assignop}', 
    '.': '{dot}', 
    '-&': '{and}', 
    '~&': '{nand}', 
    '|': '{or}', 
    '~|': '{nor}', 
    '~': '{not}', 
    '+': '{add}', 
    '-': '{sub}', 
    '*': '{mul}', 
    '/': '{div}'
}


def tokenNames(_token): # I could use a dict but its too late now (also i dont like writing dict syntax)
    global _match
    try:
        return _match[_token]
    except ValueError:
        print()

def lexer(program: str) -> list:
    ctoken = ''
    tokens = []
    inString = False
    #print(str(program))
    program = program.replace('\r\n', '\n').replace('\r', '\n')
    program = '\n'.join(x[:idx(x, '//')] for x in program.splitlines())
    #print(program)

    # Tells you the type of a token
    typeof = lambda x: '<int>' if ctoken.isdigit() else '<bool>' if ctoken in ['true', 'false'] else '<word>'

    for char in program:
        if char in ['@', '$', '!', '>', '<', '%', '#', '^', '&'] and not inString:
            if ctoken != '':
                tokens.append(token(typeof(ctoken), ctoken))
                ctoken = ''

            tokens.append(token('<startsym>', tokenNames(char)))

        elif char == '"':
            if ctoken != '' and not inString:
                tokens.append(token(typeof(ctoken), ctoken))
            elif ctoken != '':
                tokens.append(token('<str>', ctoken))
            ctoken = ''

            inString = not inString

        elif ctoken in ['-{', ':;', '==', '-&', '~&', '~|'] and not inString:
            if ctoken != '':
                tokens.append(token(typeof(ctoken), ctoken))
                ctoken = ''

            tokens.append(token('<syntax>', tokenNames(ctoken)))
            ctoken = ''

        elif char in ['{', '}', ':', ';', '(', ')', ',', '=', '.', '-', '+', '*', '/', '~', '|'] and not inString:
            if ctoken != '':
                tokens.append(token(typeof(ctoken), ctoken))
                ctoken = ''

            tokens.append(token('<syntax>', tokenNames(char)))
            ctoken = ''

        elif ctoken in ['true', 'false'] and not inString:
            if ctoken != '':
                tokens.append(token(typeof(ctoken), ctoken))
                ctoken = ''
            tokens.append(token('<bool>', '{' + ctoken + '}'))
            ctoken = ''

        elif inString:
            ctoken += char

        elif char in [' ', '  ', '  ', '\n']:
            pass

        else:
            ctoken += char

    return tokens

#@dataclass
#class group:
#    name : str = '<placeholder>'
#    contents : list = []

# A group is ['type', ['name'], ['contents']]

class parser:
    # Token types: <int>, <bool>, <word>, <startsym>, <syntax>
    def __init__(self):
        self.p = 0 # A pointer 
        self.pgm: list
        
    @property
    def _p(self) -> token: # The value that the pointer points to
        return self.pgm[self.p]
    
    def groupParse(self, tokens: list, findend: bool) -> list: # Parses one group
        # findend tells you if it needs to find the end of the group
        # top-level groups don't need this

        group = [tokens[0].value,[],[]]
        # group[0] is type
        # group[1] is name
        #    it is a list for functions in libs like math.add
        # group[2] is contents

        i = 1

        # Make sure the <name> is correct
        while tokens[i].value != '{colon}':
            if tokens[i].value != '{colon}':
                if tokens[i].type != '<word>' and tokens[i].value != '{dot}':
                    error("SyntaxErrror: Invalid name on a group.", 2)
                else:
                    group[1].append(tokens[i])

                i += 1

        colonidx = i

        # Find the end of the group, now that we are on the colon.
        # This also collects contents
        if findend:
            depth = 1
            while depth > 0:
                if depth > 0:
                    i += 1

                    if tokens[i].type == '<startsym>':
                        depth += 1

                    elif tokens[i].value == '{semi}':
                        depth -= 1

                    else:
                        group[2].append(tokens[i])

        else:
            group[2] = tokens[colonidx+1:-1] # From the colon to the end without the semicolon

        # Parse the sub groups
        # not yet, we need to know if theres sub groups

        types = {t.type for t in group[2]}
        values = {t.value for t in group[2]}
        if '<startsym>' in types:
            # ok yeah there is
            # now for sub groups

            i = 0
            # All groups found?
            agf = False
            while not agf:
                if not agf:
                    try:
                        # Find the start of a group
                        while group[2][i].type != '<startsym>':
                            if group[2][i].type != '<startsym>':
                                i += 1

                        start = i

                        # Find the end of a group
                        depth = 1
                        while depth > 0:
                            if depth > 0:
                                i += 1

                                if group[2][i].type == '<startsym>':
                                    depth += 1

                                elif group[2][i].value == '{semi}':
                                    depth -= 1

                        end = i

                        group[2][start] = self.groupParse(group[2][start:end+1], False)
                        del group[2][start+1:end+1]

                        i = start + 1

                    except IndexError:
                        error("SyntaxError: The start or end of a group is missing.", 2)

                    if i == len(group) - 2:
                        agf = True

        elif '{comma}' in values: # oh :( is it there a function?
            # yay!
            # we need to make a list of all the arguments

            # Current Argument
            carg = []
            # Index
            i = -1
            # Start of the current argument
            start = 0
            # Current token
            ctoken = None
            while '{comma}' in values:
                if '{comma}' in values:
                    i += 1
                    ctoken = group[2]

                    if ctoken.value == '{comma}':
                        group[2][start] = carg
                        del group[2][start + 1: i + 1] # This also deletes the comma
                        i = start # Adjust idx now that the list is shifted back
                        start += 1 # The argument is collaped into a singular list
                        values = {t.value for t in group[2]} # Recalibrate

                        if start == len(group[2]):
                            break
                    else:
                        if type(ctoken) == token: # Ignores a prevous argument
                            if ctoken.type == '<str>':
                                carg.append(ctoken.value)
                            else:
                                carg.append(ctoken)
        else:
            if group[2] != []:
                if group[2][0].type == '<str>':
                    group[2] = [group[2][0].value]
                else:
                    group[2] = [group[2]] 
                    # The {comma} parser groups arguments in a list regardless of length, so this is neesesdsdd need edsed yeah
            else:
                group[2] = [group[2]] 
        return group

    
    def parse(self, program: list) -> list:
        self.pgm = program
        self.pgm.append(token('<EOF>', 'End of file'))

        # All groups found?
        agf = False
        while not agf:
            if not agf:
                try:
                    # Find the start of a group
                    while self._p.type != '<startsym>':
                        if self._p.type != '<startsym>':
                            self.p += 1

                    start = self.p

                    # Find the end of a group
                    depth = 1
                    while depth > 0:
                        if depth > 0:
                            self.p += 1

                            if self._p.type == '<startsym>':
                                depth += 1

                            elif self._p.value == '{semi}':
                                depth -= 1

                    end = self.p

                    self.pgm[start] = self.groupParse(self.pgm[start:end+1], False)
                    del self.pgm[start+1:end+1]

                    self.p = start + 1

                except IndexError:
                    error("SyntaxError: The start or end of a group is missing.", 2)

                if self.p == len(self.pgm) - 1:
                    agf = True

        return self.pgm

def compileTOPLEVEL(parsed) -> list:
    bytecode = [
        ['declare', 'setup', 'cFunction'],
        ['declare', 'main', 'cFunction']
    ]
    
    # These tell if the call setup and call main are in the bytecode
    setupRan = False
    mainRan = False
    for group in parsed:
        if type(group) == token:
            if group.type == '<EOF>':
                break
            else:
                error("InernalError: Stray token in AST.", 1)
        else:
            bytecode.append(compileSUBLEVELS(group))

            if [bytecode[-1][0], bytecode[-1][1]] == ['define', 'setup']:
                bytecode.append(['call', 'setup', [None]])
                setupRan = True
            elif [bytecode[-1][0], bytecode[-1][1]] == ['define', 'main']:
                bytecode.append(['call', 'main', [None]])
                mainRan = True

    if not setupRan:
        bytecode.append(['call', 'setup', [None]])
        warn("NotFoundWarning: The 'setup' cFunc is missing.")
    
    if not mainRan:
        bytecode.append(['call', 'main', [None]])
        warn("NotFoundWarning: The 'main' cFunc is missing.")

    return bytecode

        
def compileSUBLEVELS(group) -> list:
    bytecode = []

    if group[0] == '{defcFunc}': # cFunction definitons
        name = group[1][0].value
        args = None
        if group[2] != [[]]:
            contents = list(compileSUBLEVELS(x) for x in group[2])
        else:
            contents = []

        group = ['define', name, args, contents]

    elif group[0] == '{wrt}': # write
        to = group[1][0].value
        data = group[2]

        group = ['write', to, data]

    return group

def idx(value, sub):
    try:
        return value.index(sub)
    except ValueError:
        return None

def main(pgm):

    #pgm = '\n'.join(x[:idx(x, '//')] for x in pgm.splitlines())
    #print(pgm)

    # lexer testing
    #z = (f'{x.type}, {x.value}' for x in lexer(program))
    #for y in list(z):
    #    print(y)

    p = parser()

    #print(p.parse(lexer(pgm)))

if __name__ == '__main__':
    main(argv[0])
