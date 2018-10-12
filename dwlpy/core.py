import parser
import printer

class Namespace:
    """ Namespace maps symbols to functions"""
    def __init__(self):
        self.funcs = {}

        self.set('+', lambda a, b: parser.IntSymbol(a.val + b.val)) 
        self.set('-', lambda a, b: parser.IntSymbol(a.val - b.val))
        self.set('*', lambda a, b: parser.IntSymbol(a.val * b.val))
        self.set('/', lambda a, b: parser.IntSymbol(int(a.val/b.val)))
        self.set('prn', func_prn)
        self.set('list', func_list)
        self.set('list?', func_list_p)
        self.set('empty?', func_empty_p)
        self.set('count', func_count)
        self.set('=', func_eq)
        self.set('<', func_lt)
        self.set('<=', func_le)
        self.set('>', func_gt)
        self.set('>=', func_ge)
        self.set('pr-str', func_pr_str)
        self.set('str', func_str)
        self.set('prn', func_prn)
        self.set('println', func_println)

    def set(self, key, func):
        self.funcs[key] = func

def func_prn(*args):
    outs = ""
    for a in args:
        s = printer.pr_str(a, True)
        outs += s
    print(outs)
    return parser.NilSymbol()

def func_list(*args):
    return parser.LispList(args)

def func_list_p(arg):
    if isinstance(arg, parser.LispList):
        return parser.TrueSymbol()
    else:
        return parser.FalseSymbol()

def func_empty_p(arg):
    if len(arg.values)> 0:
        return parser.FalseSymbol()
    else:
        return parser.TrueSymbol()

def func_count(arg):
    if (isinstance(arg, parser.LispList) or
        isinstance(arg, parser.LispVector)):
        return parser.IntSymbol(len(arg.values))
    return parser.IntSymbol(0)
        
def func_eq(a, b):
    # allow vectors and lists to compare equal?
    aIsList = (isinstance(a, parser.LispList) or
               isinstance(a, parser.LispVector))
    bIsList = (isinstance(b, parser.LispList) or
               isinstance(b, parser.LispVector))
    if (aIsList and bIsList):
        if len(a.values) != len(b.values):
            return parser.FalseSymbol()
        for i in range(len(a.values)):
            aval = a.values[i]
            bval = b.values[i]
            if not func_eq(aval, bval):
                return parser.FalseSymbol()
        return parser.TrueSymbol()
    if (type(a) != type(b)):
        return parser.FalseSymbol()
    if isinstance(a, parser.LispString):
        if ((len(a.str) != len(b.str)) or
            (a.str != b.str)):
            return parser.FalseSymbol()
        else:
            return parser.TrueSymbol()
    if (isinstance(a, parser.IntSymbol) or
        isinstance(a, parser.StrSymbol) or
        isinstance(a, parser.LispKeyword)):
        if a.val == b.val:
            return parser.TrueSymbol()
        else:
            return parser.FalseSymbol()

    # other (singleton?) types
    return parser.TrueSymbol()

def func_lt(a, b):
    if a.val < b.val:
        return parser.TrueSymbol()
    return parser.FalseSymbol()

def func_le(a, b):
    if a.val <= b.val:
        return parser.TrueSymbol()
    return parser.FalseSymbol()

def func_gt(a, b):
    if a.val > b.val:
        return parser.TrueSymbol()
    return parser.FalseSymbol()

def func_ge(a, b):
    if a.val >= b.val:
        return parser.TrueSymbol()
    return parser.FalseSymbol()

def func_pr_str(*args):
    strings = [printer.pr_str(a, True) for a in args]
    joined = " ".join(strings)
    return parser.LispString(joined)

def func_str(*args):
    strings = [printer.pr_str(a, False) for a in args]
    joined = "".join(strings)
    return parser.LispString(joined)

def func_prn(*args):
    strings = [printer.pr_str(a, True) for a in args]
    joined = " ".join(strings)
    print(joined)
    return parser.NilSymbol()
    
def func_println(*args):
    strings = [printer.pr_str(a, False) for a in args]
    joined = " ".join(strings)
    print(joined)
    return parser.NilSymbol()
    
        

