'''Helper file for Synulb.'''

def error(text: str, exitcode: int):
    ''' EXIT CODES 
    0: No errors
    1: InternalError
    2: SyntaxError
    3: TypeError
    4: IndexError
    5: ContextError'''
    print(f'\x1b[31m{text}')
    print(f'\x1b[31mProgram exited with code {exitcode}\x1b[37m')
    exit()

def warn(text: str):
    print(f'\x1b[38;5;166m{text}')

def boot():
    import datetime, sys
    print(f'\x1b[32mSYNULB VERSION 0.1.0 -- {sys.platform} -- {datetime.datetime.now()}')