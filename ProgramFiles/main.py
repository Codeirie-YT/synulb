# Runs the compiler and bytecode interperter

import sys, fileio, os
argv = sys.argv[1:]

if argv:
    _path = argv[0]

# restarts the program
def restart():
    os.system(f'py {os.path.join(os.getcwd(), 'main.py')}')

def main():
    fileio.boot()
    if not argv:
        _path = input('Please enter the path to your program (.syn)\n>>> ')

    file = fileio.readSyn(_path)
    if file == 0:
        print('Something went wrong. Your program could not be loaded but returned no error. Please try again.')
        restart()
    elif file == 1:
        print('That file does not exist. Please try again.')
        restart()
    else:
        print('>> File sucessfully read. Compiling...')
        print(file)

if __name__ == '__main__':
    main()