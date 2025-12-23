# Runs the compiler and bytecode interperter

import sys, fileio, os, inspect
from time import perf_counter_ns as timer

argv = sys.argv[1:]

if argv:
    _path = argv[0]

# restarts the program

def get_script_dir(follow_symlinks=True):
    if getattr(sys, 'frozen', False):
        path = os.path.abspath(sys.executable)
    else:
        path = inspect.getabsfile(get_script_dir)
    if follow_symlinks:
        path = os.path.realpath(path)
    return os.path.dirname(path)



def runFile(path: str, args):
    global isPosix
    if os.name == 'nt':
        os.system(f'py \"{path}\" {args}')
    elif os.name == 'posix':  # vs code wont stop screaming my ears hurt make it stop
        os.system(f'python3 \"{path}\" {args}')
    elif os.name == 'java':
        print("Sorry, but JPython is not a supported interperter for Synulb. Try using the CPython interperter instead.")

def main():
    fileio.boot()
    if argv == []:
        _path = input('Please enter the path to your program (.syn)\n>>> ')
    else:
        _path = argv[0]

    file = fileio.readSyn(_path)

    if file == 0:
        print('Something went wrong. Your program could not be loaded but returned no error. Please try again.')
        runFile(os.path.join(get_script_dir(), 'main.py'), '')
    elif file == 1:
        print('That file does not exist. Please try again.')
        runFile(os.path.join(get_script_dir(), 'main.py'), '')
    else:
        print('>> File sucessfully read. Compiling...\n')
        # Originally tried to run the compiler from terminal and pass arguments to it
        #print(file.read())

        #compiler = os.path.join(get_script_dir(), 'compiler.py')
        #interperter = os.path.join(get_script_dir(), 'interperter.py')

        #runFile(compiler, f'"{file.read()}"')

        from compiler import parser, lexer
        p = parser()
        s = timer()
        #print(lexer(file.read()))

        #compileSYN = lambda x: lexer(x)
        #for x in compileSYN(file.read()):
        #    print(x)

        compileSYN = lambda x: p.parse(lexer(x))
        print(compileSYN(file.read()))

        print(f'Compiling finished in {(timer() - s) / 1000000} ms')

if __name__ == '__main__':
    main()