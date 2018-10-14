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
        self.set('nth', func_nth)
        self.set('first', func_first)
        self.set('rest', func_rest)
        self.set('throw', func_throw)
        self.set('apply', func_apply)
        self.set('map', func_map)
        self.set('nil?', func_nil_p)
        self.set('true?', func_true_p)
        self.set('false?', func_false_p)
        self.set('symbol', func_symbol)
        self.set('symbol?', func_symbol_p)
        self.set('keyword', func_keyword)
        self.set('keyword?', func_keyword_p)
        self.set('vector', func_vector)
        self.set('vector?', func_vector_p)
        self.set('hash-map', func_hash_map)
        self.set('map?', func_map_p)
        self.set('assoc', func_assoc)
        self.set('dissoc', func_dissoc)
        self.set('get', func_get)
        self.set('contains?', func_contains_p)
        self.set('keys', func_keys)
        self.set('vals', func_vals)
        self.set('sequential?', func_sequential_p)


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
    if (parser.compare_eq(a, b)):
        return parser.TrueSymbol()
    else:
        return parser.FalseSymbol()

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

def func_nth(arg, pos):
    pval = pos.val
    if ((pval < 0) or
        (pval >= len(arg.values))):
        raise IndexError("out of range")
    return arg.values[pos.val]

def func_first(arg):
    if isinstance(arg, parser.NilSymbol):
        return arg
    if (isinstance(arg, parser.LispList) or
        isinstance(arg, parser.LispVector)):
        if len(arg.values) == 0:
            return parser.NilSymbol()
        return arg.values[0]
    raise ArgumentError("should be list or vector")

def func_rest(arg):
    if isinstance(arg, parser.NilSymbol):
        return parser.LispList([])
    if (isinstance(arg, parser.LispList) or
        isinstance(arg, parser.LispVector)):
        return parser.LispList(arg.values[1:])
    raise ArgumentError("should be list or vector")

def func_apply(*args):
    """takes at least two arguments. The first argument is a function and
    the last argument is list (or vector). The arguments between the
    function and the last argument (if there are any) are concatenated
    with the final argument to create the arguments that are used to
    call the function. The apply function allows a function to be
    called with arguments that are contained in a list (or vector). In
    other words, (apply F A B [C D]) is equivalent to (F A B C D).
    """

    fn = args[0]
    lastArg = args[-1]
    restArgs = list(args[1:-1])
    fullArgs = restArgs + list(lastArg.values)
    if (isinstance(fn, parser.FuncClosure)):
        return fn.call(fullArgs)
    else:
        return fn(*fullArgs)

def func_map(fn, argList):
    """takes a function and a list (or vector) and evaluates the function
    against every element of the list (or vector) one at a time and
    returns the results as a list."""

    retvals = []

    for arg in argList.values:
        if isinstance(fn, parser.FuncClosure):
            r = fn.call([arg])
        else:
            r = fn(arg)
        retvals.append(r)
    return parser.LispList(retvals)

def func_nil_p(arg):
    if isinstance(arg, parser.NilSymbol):
        return parser.TrueSymbol()
    else:
        return parser.FalseSymbol()
    
def func_true_p(arg):
    if isinstance(arg, parser.TrueSymbol):
        return parser.TrueSymbol()
    else:
        return parser.FalseSymbol()
    
def func_false_p(arg):
    if isinstance(arg, parser.FalseSymbol):
        return parser.TrueSymbol()
    else:
        return parser.FalseSymbol()

def func_symbol(arg):
    return parser.StrSymbol(arg.str)
    
def func_symbol_p(arg):
    if isinstance(arg, parser.StrSymbol):
        return parser.TrueSymbol()
    else:
        return parser.FalseSymbol()
    
def func_throw(arg):
    raise parser.MalException("foo", arg)

def func_keyword(arg):
    if isinstance(arg, parser.LispKeyword):
        return arg
    if isinstance(arg, parser.LispString):
        return parser.LispKeyword(arg.str)

def func_keyword_p(arg):
    if isinstance(arg, parser.LispKeyword):
        return parser.TrueSymbol()
    else:
        return parser.FalseSymbol()

def func_vector(*args):
    return parser.LispVector(args)

def func_vector_p(arg):
    if (isinstance(arg, parser.LispVector)):
        return parser.TrueSymbol()
    else:
        return parser.FalseSymbol()

def func_hash_map(*args):
    return parser.LispHashMap(args)

def func_map_p(arg):
    if (isinstance(arg, parser.LispHashMap)):
        return parser.TrueSymbol()
    else:
        return parser.FalseSymbol()

def func_assoc(*args):
    oldHM = args[0]
    kvs = args[1:]
    newDict = {}
    newDict.update(oldHM.data)
    newHM = parser.LispHashMap([])
    newHM.data = newDict

    for i in range(0, len(kvs), 2):
        key = kvs[i]
        val = kvs[i+1]
        newHM.assign(key, val)
    
    return newHM

def func_dissoc(hm, *keys):
    newDict = {}
    newDict.update(hm.data)
    newHM = parser.LispHashMap([])
    newHM.data = newDict

    for k in keys:
        newHM.unassign(k)
    
    return newHM


def func_get(hm, key):
    if not isinstance(hm, parser.LispHashMap):
        return parser.NilSymbol()
    v = hm.lookup(key)
    if v is None:
        return parser.NilSymbol()
    else:
        return v

def func_contains_p(hm, key):
    if not isinstance(hm, parser.LispHashMap):
        return parser.FalseSymbol()
    v = hm.lookup(key)
    if v is None:
        return parser.FalseSymbol()
    else:
        return parser.TrueSymbol()

def func_keys(arg):
    return parser.LispList(list(arg.keys()))

def func_vals(arg):
    vals = []
    for k in arg.keys():
        vals.append(arg.lookup(k))
    return parser.LispList(vals)

def func_sequential_p(arg):
    if ((isinstance(arg, parser.LispList)) or
        (isinstance(arg, parser.LispVector))):
        return parser.TrueSymbol()
    else:
        return parser.FalseSymbol()



