# Compiles the program into bytecode
# this is such bad code

class token:
    def __init__(self, _type, value):
        self.type = _type
        self.value = value

def tokenNames(_token): # I could use a dict but its too late now (also i dont like writing dict syntax)
    match _token:
        case '@':
            return '{decl}'
        case '$':
            return '{defcFunc}'
        case '!':
            return '{builtin}'
        case '>':
            return '{wrt}'
        case '<':
            return '{read}'
        case '%':
            return '{method}'
        case '#':
            return '{def}'
        case '^':
            return '{flag}'
        case '&':
            return '{clss}'
        case '-{':
            return '{pramopen}'
        case '{':
            return '{arryopen}'
        case '}':
            return '{arryclse}'
        case '(':
            return '{lparen}'
        case ')':
            return '{rparen}'
        case ':;':
            return '{void}'
        case ':':
            return '{colon}'
        case ';':
            return '{semi}'
        case ',':
            return '{comma}'
        case '==':
            return '{boolop}'
        case '=':
            return '{assigop}'
        case '.':
            return '{dot}'
        case '-&':
            return '{and}'
        case '~&':
            return '{nand}'
        case '|':
            return '{or}'
        case '~|':
            return '{nor}'
        case '~':
            return '{not}'
        case '+':
            return '{add}'
        case '-':
            return '{sub}'
        case '*':
            return '{mul}'
        case '/':
            return '{div}'

def lexer(program):
    ctoken = ''
    tokens = []
    inString = False

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
    def __init__():
        pass



def idx(value, sub):
    try:
        return value.index(sub)
    except ValueError:
        return None

def main():
    program = '''
$setup:
    @choord1:cFunc;
    @dot1:choord1;
    @choord2:cFunc;
    @dot2:choord2;
;

$choord1: // This creates a choordinate type.
    -{x: int, y: int}
    @me.value:{x,y}; // This also forces me.value to be an array of size 2. Only arrays values can be declared and defined on the same line.
    @me.fName:"choordinate"; // The formal name of the datatype.
;

$choord2: // This creates a choordinate type.
    -{x: int, y: int}
    @me.location:{x,y};
;

$main:
    #dot1:{12, 13}; // This works, as it sets the value
    #dot2:{56, 12}; // This doesn't work, as .value hasn't been declared yet.
;
'''

    program = '\n'.join(x[:idx(x, '//')] for x in program.splitlines())

    # lexer testing
    #z = (f'{x.type}, {x.value}' for x in lexer(program))
    #for y in list(z):
    #    print(y)

    print(parser.parse(lexer(program)))

if __name__ == '__main__':
    main()
