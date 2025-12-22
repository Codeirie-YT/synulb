'''File Read/Write library for Synulb.'''
# Libraries
import sys, os, pickle

# Eliminates the .pyc file.
# Or at least it *should*
# It doesnt. Waaaa.
sys.dont_write_bytecode = True
# Full path is needed to access files. Otherwise, a FileNotFoundError will be raised.
_path = os.getcwd()

def readBC(filename: str):
    '''Reads from a bytecode file.'''
    try:
        # Join is used to support cross-platform IO.
        return pickle.load(os.path.join(_path, filename))
    except Exception as e:
        print(e)
        return None, 1

def writeBC(filename: str, bytecode: list):
    '''Writes to a bytecode file.'''
    try:
        with open(os.path.join(_path, filename), 'wb') as f:
            pickle.dump(bytecode, f)
    except:
        return 1 # Error occured
    else:
        return 0 # Exit code 0.
    
def readSyn(filepath: str):
    '''Reads a .syn file.'''
    try:
        if filepath[filepath.index('.'):] != '.syn':
            print(f'That is not a synulb file!')
            exit()
    except ValueError as e:
        print(f'That is not a synulb file!')
        print(e)
        exit()
    
    try:
        ispath = os.path.exists(os.path.abspath(filepath))

        if ispath:
            print("Path Exists.")
            print(os.path.abspath(filepath))
            return open(os.path.abspath(filepath))
        else:
            if 'win' in sys.platform:
                #print(os.path.abspath(os.path.join(os.environ.get('PATH'), filepath)))
                return open(os.path.abspath(os.path.join(os.environ.get('PATH'), filepath)))
            else:
                raise FileNotFoundError

    except FileNotFoundError:
        return 1
    
    except Exception as e:
        print(f'^[1;31m{e}')
    else:
        return 0
    

def boot():
    import datetime
    print(f'SYNULB VERSION 1.0.0 -- {sys.platform} -- {datetime.datetime.now()}')