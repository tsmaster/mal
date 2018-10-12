class Symbol:
    pass

class IntSymbol(Symbol):
    def __init__(self, val):
        self.val = val

    def __str__(self):
        return "Int<{0}>".format(self.val)

    def __repr__(self):
        return str(self)

class StrSymbol(Symbol):
    def __init__(self, s):
        self.val = s

    def __str__(self):
        return "Str<{0}>".format(self.val)

    def __repr__(self):
        return str(self)

class NilSymbol(Symbol):
    def __str__(self):
        return "<Nil>"

    def __repr__(self):
        return str(self)

class TrueSymbol(Symbol):
    def __str__(self):
        return "#T"

    def __repr__(self):
        return str(self)

class FalseSymbol(Symbol):
    def __str__(self):
        return "#F"

    def __repr__(self):
        return str(self)

class FuncClosure:
    def __init__(self, env, params, body):
        self.env = env
        self.params = params
        self.body = body
        
    def __str__(self):
        return "FuncClosure"

    def __repr__(self):
        return str(self)

class LispList:
    def __init__(self, values):
        self.values = values

class LispString:
    def __init__(self, s):
        self.str = s
        
class LispVector:
    def __init__(self, values):
        self.values = values

class LispKeyword:
    def __init__(self, val):
        self.val = '0x29E' + val
        self.rawVal = val

    def __str__(self):
        return ':' + self.rawVal

class LispHashMap:
    def __init__(self, val):
        self.data = {}


class Reader:
    """ a simple stateful Reader object in reader.py. This object will store the tokens and a position. """

    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def next(self):
        """ returns the token at the current position and increments the position"""
        val = self.tokens[self.position]
        self.position += 1
        return val

    def peek(self):
        """ just returns the token at the current position"""
        return self.tokens[self.position]

    def has_token(self):
        return self.position < len(self.tokens)


class ExpressionOfSymbols:
    pass
