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
    print('\x1b[0m')

def boot():
    import datetime, sys
    print(f'\x1b[32mSYNULB VERSION ALPHA 0.1.7_d -- {sys.platform} -- {datetime.datetime.now()}')

'''
Versions as per this update (12):

Alpha 0.1.0             FIX-UNTRAKED
Alpha 0.1.1             Compiler interface working! Added Swearing.
Alpha 0.1.2             This was done 4 months ago, IDK the changes
Alpha 0.1.3             Fixed Untracked Files
Alpha 0.1.4             desperatly tried to fix a non-existant bug. sad.
Alpha 0.1.5             MADE A PARSER! IT KINDA WORKS YIPPEE!
Alpha 0.1.6             Working compiler: "Hello, World!"
Alpha 0.1.6_b           Fixed Installer
Alpha 0.1.7             I ADDED VARIABLES!
Workflow Alpha 0.1.7_b  Make Workflow for pipline
Workflow Alpha 0.1.7_c  Disable flake8 and the .txt install
Alpha 0.1.7_b           Made version numbers make sence.
'''