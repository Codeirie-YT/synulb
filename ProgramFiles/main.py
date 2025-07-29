# Runs the compiler and bytecode interperter

import sys, fileio, os, inspect
argv = sys.argv[1:]

if argv:
    _path = argv[0]

# restarts the program

def get_script_dir(follow_symlinks=True):
    if getattr(sys, 'frozen', False): # py2exe, PyInstaller, cx_Freeze
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
    elif os.name == 'posix':  # vs code wont stop screaming my ears hurt make it fucking stop
        os.system(f'python3 \"{path}\" {args}')
    elif os.name == 'java':
        print("Sorry, but JPython is not a supported interperter for Synulb. Try using the CPython interperter instead.")

def main():
    fileio.boot()
    if not argv:
        _path = input('Please enter the path to your program (.syn)\n>>> ')

    file = fileio.readSyn(_path)
    if file == 0:
        print('Something went wrong. Your program could not be loaded but returned no error. Please try again.')
        runFile(os.path.join(get_script_dir(), 'main.py'), '')
    elif file == 1:
        print('That file does not exist. Please try again.')
        runFile(os.path.join(get_script_dir(), 'main.py'), '')
    else:
        print('>> File sucessfully read. Compiling...')
        #print(file.read())

        #compiler = os.path.join(get_script_dir(), 'compiler.py')
        #interperter = os.path.join(get_script_dir(), 'interperter.py')

        #runFile(compiler, f'"{file.read()}"')
        from compiler import parser, lexer
        p = parser
        compileSYN = lambda x: p.parse(lexer(x))

        print(compileSYN(file.read()))

if __name__ == '__main__':
    main()