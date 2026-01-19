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

class undefined:
    '''No data *yet*. Placeholder for the .value of declared variables but not defined variables.'''
    pass

class Integer(cFunction):
    def __init__(self, value: str = '0x0'):
        super().__init__('int', None, value, None)
        self.fName = 'Integer'

        # Python Functions that can be run in Synulb:

    # Python Functions that can't be run in Synulb:

    def check(self):
        if type(self.value) is undefined:
            return 0
        
        _max = 2147483647
        _min = -2147483648

        if self.__int__() > _max:
            self.value = hex(_min)
            warn("OverflowWarning: Overflow")
            return 1
            
        elif self.__int__() < _min:
            self.value = hex(_max)
            warn("UnderflowWarning: Underflow")
            return 2

        else:
            return 0

    def __int__(self):
        '''Returns a python integer for the value.'''
        return int(self.value, 16)
    
    