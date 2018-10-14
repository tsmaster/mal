import parser
import printer
import reader


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
        self.set('read-string', func_read_string)
        self.set('slurp', func_slurp)
        self.set('atom', func_atom)
        self.set('atom?', func_atom_p)
        self.set('deref', func_deref)
        self.set('reset!', func_reset_bang)
        self.set('swap!', func_swap_bang)
        self.set('cons', func_cons)
        self.set('concat', func_concat)

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
    
def func_read_string(arg):
    if not isinstance(arg, parser.LispString):
        raise ArgumentError("should be a string")
    return reader.read_str(arg.str)

def func_slurp(arg):
    if not isinstance(arg, parser.LispString):
        raise ArgumentError("should be a string")
    fn = arg.str
    with open(fn) as fileObj:
        return parser.LispString(fileObj.read())
    
def func_atom(arg):
    return parser.LispAtom(arg)

def func_atom_p(arg):
    if isinstance(arg, parser.LispAtom):
        return parser.TrueSymbol()
    else:
        return parser.FalseSymbol()

def func_deref(arg):
    if not isinstance(arg, parser.LispAtom):
        raise ArgumentError("should be an atom")

    return arg.ptr

def func_reset_bang(arg, newval):
    if not isinstance(arg, parser.LispAtom):
        raise ArgumentError("should be an atom")
    
    arg.ptr = newval
    return newval

def func_swap_bang(arg, fn, *args):
    """The atom's value is modified to the result of applying the function
    with the atom's value as the first argument and the optionally
    given function arguments as the rest of the arguments. The new
    atom's value is returned."""

    if not isinstance(arg, parser.LispAtom):
        raise ArgumentError("should be an atom")

    arg_list = [arg.ptr] + list(args)

    if isinstance(fn, parser.FuncClosure):
        val = fn.call(arg_list)
    else:
        val = fn(*arg_list)

    arg.ptr = val

    return val

def func_cons(a, b_list):
    return b_list.prepend(a)

def func_concat(*args):
    outvals = []
    for a in args:
        outvals += a.values
    return parser.LispList(outvals)
