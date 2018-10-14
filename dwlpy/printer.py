import parser

"""
this file will contain a single function pr_str which does the opposite of read_str: take a data structure and return a string representation of it.
"""


def escape(s):
    outs = ""
    for c in s:
        if c == '"':
            outs += r'\"'
        elif c == '\n':
            outs += r'\n'
        elif c == '\\':
            outs += '\\\\'
        else:
            outs += c
    return outs

def unescape(s):
    outs = ""
    while s:
        c = s[0]
        if c == '\\':
            n = s[1]
            if n == 'n':
                outs += '\n'
            elif n == '\\':
                outs += '\\'
            elif n == '"':
                outs += '"'
            elif n == 't':
                outs += "\t"
            else:
                outs += '<???>'
            s = s[2:]
        else:
            outs += c
            s = s[1:]
    return outs

def pr_str(expr, print_readably):
    """pr_str is much simpler (than read_str) and is basically just a switch statement on the type of the input object:
    - symbol: return the string name of the symbol
    - number: return the number (as a string)
    - list: iterate through each element of the list, calling pr_str on it, join the results together with a space separator, and surround the final result with parens.
    """

    if expr == []:
        return "blank line"

    if isinstance(expr, parser.LispList):
        vals = [pr_str(val, print_readably) for val in expr.values]
        return '(' + ' '.join(vals) + ')'
    if isinstance(expr, parser.LispVector):
        vals = [pr_str(val, print_readably) for val in expr.values]
        return '[' + ' '.join(vals) + ']'
    elif isinstance(expr, parser.IntSymbol):
        return str(expr.val)
    elif isinstance(expr, parser.NilSymbol):
        return 'nil'
    elif isinstance(expr, parser.TrueSymbol):
        return 'true'
    elif isinstance(expr, parser.FalseSymbol):
        return 'false'
    elif isinstance(expr, parser.StrSymbol):
        return expr.val
    elif isinstance(expr, parser.LispString):
        if print_readably:
            s = escape(expr.str)
            return '"' + s + '"'
        else:
            s = expr.str
            return s
    elif isinstance(expr, parser.FuncClosure):
        return '#<function>'
    elif isinstance(expr, parser.LispKeyword):
        return str(expr)
    elif isinstance(expr, parser.LispAtom):
        contents = pr_str(expr.ptr, print_readably)
        return "(atom {0})".format(contents)
    elif isinstance(expr, parser.LispHashMap):
        vals = []
        for k in expr.keys():
            vals.append(pr_str(k, print_readably))
            vals.append(pr_str(expr.lookup(k), print_readably))
        s = " ".join(vals)
        return '{'+s+'}'
    else:
        return '<unknown of of type {0}:{1}>'.format(type(expr), expr)
