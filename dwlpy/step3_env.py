import reader
import printer
import parser
import environment

repl_env = environment.Environment(None)

repl_env.set('+', lambda a, b: parser.IntSymbol(a.val + b.val)) 
repl_env.set('-', lambda a, b: parser.IntSymbol(a.val - b.val))
repl_env.set('*', lambda a, b: parser.IntSymbol(a.val * b.val))
repl_env.set('/', lambda a, b: parser.IntSymbol(int(a.val/b.val)))

def READ(s):
    malData = reader.read_str(s)
    return malData

def EVAL(ast, env):
    #print ("evaluating", ast)
    if not isinstance(ast, list):
        return eval_ast(ast, env)
    if len(ast) == 0:
        return ast

    op = ast[0]
    if isinstance(op, parser.StrSymbol) and op.val == 'def!':
        """call the set method of the current environment (second parameter of
        EVAL called env) using the unevaluated first parameter (second
        list element) as the symbol key and the evaluated second
        parameter as the value."""
        val = EVAL(ast[2], env)
        env.set(ast[1].val, val)
        return val
    elif isinstance(op, parser.StrSymbol) and op.val == 'let*':
        newenv = environment.Environment(env)
        for i in range(0, len(ast[1]), 2):
            name = ast[1][i].val
            val = EVAL(ast[1][i+1], newenv)
            newenv.set(name, val)
        val = EVAL(ast[2], newenv)
        return val
    else:
        ast_list = eval_ast(ast, env)
        return ast_list[0](*ast_list[1:])
    

def PRINT(s):
    return printer.pr_str(s)

def rep(s):
    readval = READ(s)
    evalval = EVAL(readval, repl_env)
    return PRINT(evalval)

def eval_ast(ast, env):
    if isinstance(ast, parser.StrSymbol):
        v = ast.val
        return env.get(v)
        
    elif isinstance(ast, list):
        return [EVAL(x, env) for x in ast]
    else:
        return ast


def mainloop():
    while True:
        s = input("user> ")
        try:
            print (rep(s))
        except ValueError as e:
            print(e)
        
if __name__ == "__main__":
    mainloop()
