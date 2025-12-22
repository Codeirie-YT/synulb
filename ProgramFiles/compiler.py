# Compiles the program into bytecode
# this is such bad code

import pickle
from sys import argv
from helper import *
argv = argv[1:]

class token:
    def __init__(self, _type, value):
        self.type = _type
        self.value = value

    def __str__(self):
        return f"{self.type} {self.value}"

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

def lexer(program) -> list:
    ctoken = ''
    tokens = []
    inString = False
    print(str(program))
    program = program.replace('\r\n', '\n').replace('\r', '\n')
    program = '\n'.join(x[:idx(x, '//')] for x in program.splitlines())
    #print(program)

    for char in program:
        if char in ['@', '$', '!', '>', '<', '%', '#', '^', '&'] and not inString:
            if ctoken != '':
                tokens.append(token((lambda x: '<int>' if ctoken.isdigit() else '<bool>' if ctoken in ['true', 'false'] else '<word>')(ctoken), ctoken))
                ctoken = ''

            tokens.append(token('<startsym>', tokenNames(char)))

        elif char == '"':
            if ctoken != '' and not inString:
                tokens.append(token((lambda x: '<int>' if ctoken.isdigit() else '<bool>' if ctoken in ['true', 'false'] else '<word>')(ctoken), ctoken))
            elif ctoken != '':
                tokens.append(token('<str>', ctoken))
            ctoken = ''

            inString = not inString

        elif inString:
            ctoken += char

        elif ctoken in ['-{', ':;', '==', '-&', '~&', '~|']:
            if ctoken != '':
                tokens.append(token((lambda x: '<int>' if ctoken.isdigit() else '<bool>' if ctoken in ['true', 'false'] else '<word>')(ctoken), ctoken))
                ctoken = ''

            tokens.append(token('<syntax>', tokenNames(ctoken)))
            ctoken = ''

        elif char in ['{', '}', ':', ';', '(', ')', ',', '=', '.', '-', '+', '*', '/', '~', '|']:
            if ctoken != '':
                tokens.append(token((lambda x: '<int>' if ctoken.isdigit() else '<bool>' if ctoken in ['true', 'false'] else '<word>')(ctoken), ctoken))
                ctoken = ''

            tokens.append(token('<syntax>', tokenNames(char)))
            ctoken = ''

        elif ctoken in ['true', 'false']:
            if ctoken != '':
                tokens.append(token((lambda x: '<int>' if ctoken.isdigit() else '<bool>' if ctoken in ['true', 'false'] else '<word>')(ctoken), ctoken))
                ctoken = ''
            tokens.append(token('<bool>', '{' + ctoken + '}'))
            ctoken = ''

        elif char in [' ', '  ', '  ', '\n']:
            pass

        else:
            ctoken += char

    return tokens

class parser:
    # Token types: <int>, <bool>, <word>, <startsym>, <syntax>
    def __init__(self):
        self.p = 0 # A pointer 
        self.pgm: list
        
    @property
    def _p(self) -> token: # The value that the pointer points to
        return self.pgm[self.p]
    
    def parse(self, program) -> list:
        self.pgm = program
        self.pgm.append(token('<EOF>', 'End of file'))

        # Phase 1: Creating groups (syntax of ( symbol name ':' stuff ';' ))
        # Linear Search for the start symbol
        while self._p.type != '<startsym>': # Find group start (1a)
            if self._p.type != '<startsym>':
                self.p += 1

                if self._p.type == '<EOF>':
                    error('SyntaxError: Couldn\'t find a startsymbol. (ex: $, !, #, etc.) Line: all of them', 2)
                
        if self._p.type == '<startsym>':
            try: # Find the first colon
                h = self.p
                self.p = self.pgm.index('{colon}', self.p)
            except ValueError:
                error(f'SyntaxError: \':\' missing, expected following the first startsymbol.', 2)

            
            return self._p
        
        else: # if the search for <startsym> didnt find <startsym>...
            error('InternalError: Search for <startsym> found a <startsym> and didn\'t return <startsym>. It\'s as crazy as it sounds. Please report this.', 1)




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
