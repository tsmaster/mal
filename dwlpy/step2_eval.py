import reader
import printer
import parser


repl_env = {'+': lambda a, b: parser.IntSymbol(a.val + b.val),
            '-': lambda a, b: parser.IntSymbol(a.val - b.val),
            '*': lambda a, b: parser.IntSymbol(a.val * b.val),
            '/': lambda a, b: parser.IntSymbol(int(a.val/b.val))
            }

def READ(s):
    malData = reader.read_str(s)
    return malData

def EVAL(ast, env):
    #print ("evaluating", ast)
    if not isinstance(ast, list):
        return eval_ast(ast, env)
    if len(ast) == 0:
        return ast
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
        if v in env:
            return env[v]
        else:
            #raise ValueError('unknown value ' + v)
            raise ValueError("'" + v + "' not found.")
        
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
