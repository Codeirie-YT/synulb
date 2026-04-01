from helper import *

class cFunction:  # Class function
    '''A singular object that acts as both a class and a function'''
    def __init__(self, name: str, code: list, value: any, methods: dict):
        self.name = name
        self.code = code # Bytecode 
        self.value = value # Value for datatypes
        self.fName = None # Formal name for datatypes
        self.methods = methods # Methods for classes


class externalFunction:  # create a builtin function that runs python code
    '''Python code that can be run in synulb'''
    def __init__(self, name: str, code: str):
        self.name = name
        self.code = code # python code


# ~~~~~~~~~~ TYPES ~~~~~~~~~~

class null(cFunction):
    '''No data.'''
    def __init__(self):
        super().__init__('null', None, None, None)

    def __str__(self):
        return 'null'

class undefined(cFunction):
    '''No data *yet*. Placeholder for the .value of declared variables but not defined variables.'''
    def __init__(self):
        super().__init__('undefined', None, None, None)

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
        
        return int(self.value, 16)
    
class Character:
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