# This file exists as a base library for SYNULB.

from interperter import cFunction, externalFunction

def _import(): # The actual library
    return [
        cFunction('sayPiFromCF', ['write', 'console', '3.14'], None, None),
        externalFunction('sayPiFromEF', 'print(3.14)')
    ]