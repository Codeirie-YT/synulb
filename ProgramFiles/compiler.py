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
            pass
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
