import parser

"""
this file will contain a single function pr_str which does the opposite of read_str: take a data structure and return a string representation of it.
"""


def pr_str(expr):
    """pr_str is much simpler (than read_str) and is basically just a switch statement on the type of the input object:
    - symbol: return the string name of the symbol
    - number: return the number (as a string)
    - list: iterate through each element of the list, calling pr_str on it, join the results together with a space separator, and surround the final result with parens.
    """

    if isinstance(expr, list):
        vals = [pr_str(val) for val in expr]
        return '(' + ' '.join(vals) + ')'
    elif isinstance(expr, parser.IntSymbol):
        return str(expr.val)
    elif isinstance(expr, parser.StrSymbol):
        return expr.val

    else:
        print ("can't print", expr)
        return -1
