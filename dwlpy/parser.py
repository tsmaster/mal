import environment

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
    def __init__(self, env, params, body, evalFunc):
        self.env = env
        self.params = params
        self.body = body
        self.evalFunc = evalFunc
        self.isMacro = False

    def setMacro(self, isMacro):
        self.isMacro = isMacro
        
    def __str__(self):
        return "FuncClosure"

    def __repr__(self):
        return str(self)

    def prepareEnv(self, args):
        newenv = environment.Environment(self.env, [], [])
                
        for i,p in enumerate(self.params):
            if p == '&':
                nextP = self.params[i+1]
                val = LispList(args[i:])
                newenv.set(nextP, val)
                break
            val = args[i]
            newenv.set(p, val)
        return newenv

    def call(self, argList):
        return self.evalFunc(self.body, self.prepareEnv(argList))

class LispList:
    def __init__(self, values):
        self.values = values

    def prepend(self, new_head):
        return LispList([new_head] + list(self.values))

class LispString:
    def __init__(self, s):
        self.str = s
        
class LispVector:
    def __init__(self, values):
        self.values = values
        
    def prepend(self, new_head):
        return LispList([new_head] + list(self.values))

class LispKeyword:
    def __init__(self, val):
        self.val = '0x29E' + val
        self.rawVal = val

    def __str__(self):
        return ':' + self.rawVal

class LispHashMap:
    def __init__(self, vals):
        self.data = {}
        for i in range(0, len(vals), 2):
            key = vals[i]
            val = vals[i+1]
            self.data[key] = val
            
    def keys(self):
        keyList = list(self.data.keys())
        #keyList.sort()
        return keyList

    def lookup(self, key):
        for k in self.data.keys():
            if compare_eq(k,key):
                return self.data[k]
        return None

    def assign(self, key, value):
        for k in self.data.keys():
            if compare_eq(k,key):
                self.data[k] = value
                return
        self.data[key] = value
    
class LispAtom:
    def __init__(self, val):
        self.ptr = val


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

class MalException(Exception):
    def __init__(self, ex_str, ex_obj):
        super().__init__(ex_str)
        self.mal_obj = ex_obj
        

def compare_eq(a, b):
    # allow vectors and lists to compare equal?
    aIsList = (isinstance(a, LispList) or
               isinstance(a, LispVector))
    bIsList = (isinstance(b, LispList) or
               isinstance(b, LispVector))
    if (aIsList and bIsList):
        if len(a.values) != len(b.values):
            return False
        for i in range(len(a.values)):
            aval = a.values[i]
            bval = b.values[i]
            if not func_eq(aval, bval):
                return False
        return TrueSymbol()
    if (type(a) != type(b)):
        return FalseSymbol()
    if isinstance(a, LispString):
        if ((len(a.str) != len(b.str)) or
            (a.str != b.str)):
            return False
        else:
            return TrueSymbol()
    if (isinstance(a, IntSymbol) or
        isinstance(a, StrSymbol) or
        isinstance(a, LispKeyword)):
        if a.val == b.val:
            return True
        else:
            return False

    # other (singleton?) types
    return True
    
