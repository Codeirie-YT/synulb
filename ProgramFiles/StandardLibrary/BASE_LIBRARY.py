# This file exists as a base library for SYNULB.

class cFunction:  # classFunctions
    def __init__(self, name: str, code: list, value: any, methods: dict):
        self.name = name
        self.code = code   # Bytecode values for the cFunc
        self.value = value  # Value attribute for classes
        self.methods = methods  # Methods for classes

class externalFunction:  # create a builtin function that runs python code
    def __init__(self, name: str, code: str):
        self.name = name
        self.code = code # python code


def _import(): # The actual library
    return [
        cFunction('sayPiFromCF', ['write', 'console', '3.14'], None, None),
        externalFunction('sayPiFromEF', 'print(3.14)')
    ]