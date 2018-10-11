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
