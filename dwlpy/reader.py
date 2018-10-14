import re

import parser
import printer

def read_str(s):
    """ call tokenizer and create a new Reader object instance with the tokens. Then it will call read_form with the Reader instance."""

    tokens = tokenizer(s)
    if len(tokens) == 0:
        return []
    #print("tokens:", tokens)
    r = parser.Reader(tokens)
    malData = read_form(r)
    return malData


def tokenizer(s):
    """ this function will take a single string and return a list of all the tokens (strings) in it."""

    pattern = r"""[\s,]*(~@|[\[\]{}()'`~^@]|"(?:\\.|[^\\"])*"|;.*|[^\s\[\]{}('"`,;)]*)"""
    
    tokens = [x for x in re.findall(pattern, s) if ((len(x)> 0) and(x[0] != ';'))]

    #print ("tokens:", tokens)
    return tokens


def read_form(readerInst):
    """this function will peek at the first token in the Reader object
    and switch on the first character of that token.  If the character
    is a left paren then read_list is called with the Reader object.
    Otherwise, read_atom is called with the Reader Ojbect.  The return
    value from read_form is a MAL data type. You can likely just
    return a plain list of MAL types.
    """

    tok = readerInst.peek()

    if tok is '(':
        return parser.LispList(read_list(readerInst, ')'))
    elif tok is '[':
        return parser.LispVector(read_list(readerInst, ']'))
    elif tok is '{':
        return parser.LispHashMap(read_list(readerInst, '}'))
    elif tok is '@':
        atSign = readerInst.next()
        nextForm = read_form(readerInst)
        return parser.LispList([parser.StrSymbol('deref'), nextForm])
    elif tok is "'":
        readerInst.next()
        nextForm = read_form(readerInst)
        return parser.LispList([parser.StrSymbol('quote'), nextForm])
    elif tok is "`":
        readerInst.next()
        nextForm = read_form(readerInst)
        return parser.LispList([parser.StrSymbol('quasiquote'), nextForm])
    elif tok is "~":
        readerInst.next()
        nextForm = read_form(readerInst)
        return parser.LispList([parser.StrSymbol('unquote'), nextForm])
    elif tok == "~@":
        readerInst.next()
        nextForm = read_form(readerInst)
        return parser.LispList([parser.StrSymbol('splice-unquote'), nextForm])
    else:
        return read_atom(readerInst)
    

def read_list(readerInst, termVal):
    """this function will repeatedly call read_form with the Reader object
    until it encounters a ')' token (if it reaches EOF before reading
    a ')' then that is an error). It accumulates the results into a
    List type. Note that read_list repeatedly calls read_form rather
    than read_atom. This mutually recursive definition between
    read_list and read_form is what allows lists to contain lists.
    """

    outList = []

    firstParen = readerInst.next()

    while True:
        if not readerInst.has_token():
            raise SyntaxError('missing ' + termVal)
        
        malItem = read_form(readerInst)

        if isinstance(malItem, parser.StrSymbol) and malItem.val == termVal:
            return outList
        outList.append(malItem)

def read_atom(readerInst):
    """ this function will look at the contents of the token and return the appropriate scalar (simple/single) data type value. Initially, you can just implement numbers(integers) and symbols. This will allow you to proceed through the next couple of steps before you will need to implement the other fundamental MAL types: nil, true, false, and string. The remaining MAL types: keyword, vector, hash-map, and atom do not need to be implemented until step 9 (but can be implemented at any point between this step and that). BTW, symbol types are just objects that contain a single string name value."""

    if not readerInst.has_token():
        raise SyntaxError('reached EOF')

    malItem = readerInst.next()

    try:
        intNum = int(malItem)
        return parser.IntSymbol(intNum)
    except ValueError:
        #print ("malItem:", malItem)
        #print ("len:", len(malItem))
        if ((len(malItem)>1) and (malItem[0] == '"') and (malItem[-1] == '"')):
            s = printer.unescape(malItem[1:-1])
            #print ("making lisp string:", s)
            #for i,c in enumerate(s):
            #    print (i, c)
            return parser.LispString(s)

        if ((len(malItem) > 1) and (malItem[0] == ':')):
            s = malItem[1:]
            return parser.LispKeyword(s)
        if malItem == 'nil':
            return parser.NilSymbol()
        elif malItem == 'true':
            return parser.TrueSymbol()
        elif malItem == 'false':
            return parser.FalseSymbol()
        else:
            return parser.StrSymbol(malItem)
    
    

