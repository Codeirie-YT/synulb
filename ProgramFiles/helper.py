'''Helper file for Synulb.'''

def error(text: str, exitcode: int):
    ''' EXIT CODES 
    0: No errors
    1: InternalError
    2: SyntaxError
    3: TypeError
    4: IndexError'''
    print(text)
    print(f'Program exited with code {exitcode}')
    exit()