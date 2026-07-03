from helper import *
import os
class cFunction:  # Class function
    '''A singular object that acts as both a class and a function'''
    def __init__(self, name: str, code: list, value: any, methods: dict):
        self.name = name
        self.code = code # Bytecode 
        self.value = value # Value for datatypes
        self.fName = None # Formal name for datatypes
        self.methods = methods # Methods for classes




# ~~~~~~~~~~ TYPES ~~~~~~~~~~

class null(cFunction):
    '''No data.'''
    def __init__(self):
        super().__init__('null', None, None, None)
        self.fName = 'Null'

    def __str__(self):
        return 'null'

class undefined(cFunction):
    '''No data *yet*. Placeholder for the .value of declared variables but not defined variables.'''
    def __init__(self):
        super().__init__('undef', None, None, None)
        self.fName = 'Undefined'

    def __str__(self):
        return 'undefined'

class Integer(cFunction):
    '''Signed 32bit integer'''
    def __init__(self, value: str = '0x0'):
        super().__init__('int', None, value, None)
        self.fName = 'Integer'

        self._max = (2 * 32) - 1
        self._min = -(2 * 32)

        # Python Functions that can be run in Synulb:

    # Python Functions that can't be run in Synulb:

    def check(self):
        if type(self.value) is undefined:
            return 0
        

        if self.__int__() > self._max:
            self.value = hex(self._min)
            warn("OverflowWarning: Overflow")
            return 1
            
        elif self.__int__() < self._min:
            self.value = hex(self._max)
            warn("UnderflowWarning: Underflow")
            return 2

        else:
            return 0

    def __int__(self):
        '''Returns a python integer for the value.'''
        if type(self.value) in [undefined, null]:
            return self.value
        
        return int(self.value, base=16)
    
    def __str__(self):
        return str(self.__int__())

class String(cFunction):
    '''A string'''
    def __init__(self, value: str = ''):
        super().__init__('str', None, value, None)
        self.fName = 'String'

    def __str__(self):
        return self.value
    
class Boolean(cFunction):
    '''A boolean. Values are in lowercase: true/false'''
    def __init__(self, value: bool = False):
        super().__init__('bool', None, value, None)
        self.fName = 'Boolean'

    def __str__(self):
        return str(self.value)
    
    def __bool__(self):
        return self.value

class Character(cFunction):
    '''Unsigned 8 bit integer'''
    def __init__(self, value: str = '0x0'):
        super().__init__('char', None, value, None)
        self.fName = 'Character'

        self._max = 255
        self._min = 0

        # Python Functions that can be run in Synulb:

    # Python Functions that can't be run in Synulb:

    def check(self):
        if type(self.value) is undefined:
            return 0
        

        if self.__int__() > self._max:
            self.value = hex(self._min)
            warn("OverflowWarning: Overflow")
            return 1
            
        elif self.__int__() < self._min:
            self.value = hex(self._max)
            warn("UnderflowWarning: Underflow")
            return 2

        else:
            return 0

    def __int__(self):
        '''Returns a python integer for the value.'''
        if type(self.value) in [undefined, null]:
            return self.value
        
        return int(self.value, 16)
    
    def __char__(self):
        '''Returns a character'''
        if type(self.value) in [undefined, null]:
            return self.value
        
        return chr(int(self.value, 16))
    
    def __str__(self):
        return self.__char__()
    
class iostream():
    '''fileio stream for >< commands'''
    def __init__(self, location):
        self.location = location
    
    def write(data, flush):
        if flush:
            pass
        else:
            pass

class mergeio:
    '''Alternative to fileio that merges an in and out stream into one.'''
    def __init__(self, _in, out):
        self._in = _in
        self.out = out

        self.write = out.write
        self.flush = out.flush
        self.writable = out.writable
        self.seekable = lambda: _in.seekable() and out.seekable()
        self.tell = lambda: out.tell() if _in.tell == out._tell else ValueError("Multiple 'tell' lengths returned.")
        self.read = _in.read
        self.readable = _in.readable
        self.readline = _in.readline
        self.readlines = _in.readlines
    
    def close(self):
        self._in.close()
        self.out.close()

    def seek(self, offset, whence=os.SEEK_SET):
        if self.seekable():
            self._in.seek(offset, whence)
            self.out.seek(offset, whence)

    def trunicate(self, size=None):
        self.out.trunicate = size

    def __str__(self):
        return self.read()