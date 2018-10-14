import sys

import reader
import printer
import parser
import environment
import core

repl_env = environment.Environment(None, [], [])
repl_ns = core.Namespace()

for k,v in repl_ns.funcs.items():
    repl_env.set(k, v)

def func_eval(arg):
    return EVAL(arg, repl_env)

#eval (not in core, because it needs the toplevel env?)
repl_env.set('eval', func_eval)

def READ(s):
    malData = reader.read_str(s)
    return malData

def EVAL(ast, env):
    while True:
        #print ("evaluating", ast)
        if not isinstance(ast, parser.LispList):
            return eval_ast(ast, env)
        if len(ast.values) == 0:
            return ast
    
        op = ast.values[0]
        #print ("op", op)
        if isinstance(op, parser.StrSymbol) and op.val == 'def!':
            """call the set method of the current environment (second parameter of
            EVAL called env) using the unevaluated first parameter (second
            list element) as the symbol key and the evaluated second
            parameter as the value."""
            val = EVAL(ast.values[2], env)
            env.set(ast.values[1].val, val)
            return val
        elif isinstance(op, parser.StrSymbol) and op.val == 'let*':
            newenv = environment.Environment(env)
            for i in range(0, len(ast.values[1]), 2):
                name = ast.values[1][i].val
                val = EVAL(ast.values[1][i+1], newenv)
                newenv.set(name, val)
            env = newenv
            ast = ast.values[2]
            continue
        elif isinstance(op, parser.StrSymbol) and op.val == 'do':
            ret = None
            for t in ast.values[1:-1]:
                #print ("evaluating",t)
                ret = EVAL(t, env)
                #print ("got ret")
                #print ("env:", env)
            ast = ast.values[-1]
            continue
        elif isinstance(op, parser.StrSymbol) and op.val == 'if':
            #print ("evaluating if")
            test = EVAL(ast.values[1], env)
            #print ("test:", test)
            if not (isinstance(test, parser.NilSymbol) or isinstance(test, parser.FalseSymbol)):
                # true eval
                #print ("test was true, evaluating", ast.values[2])
                ast = ast.values[2]
                continue
            elif len(ast.values) > 3:
                #print ("test was false, evaluating else", ast.values[3])
                #else
                ast = ast.values[3]
                continue
            else:
                #print ("test was false, returning Nil")
                return parser.NilSymbol()
        elif isinstance(op, parser.StrSymbol) and op.val == 'fn*':
            newenv = environment.Environment(env, [], [])
            params = [x.val for x in ast.values[1].values]
            body = ast.values[2]
            #print ("making func", params, body)
            funcClosure = parser.FuncClosure(newenv, params, body, EVAL)
            return funcClosure
    
        else:
            ast_list = eval_ast(ast, env)
            
            if isinstance(ast_list.values[0], parser.FuncClosure):
                func = ast_list.values[0]

                ast = func.body
                env = func.prepareEnv(ast_list.values[1:])
                continue
    
            #print ("about to call", ast_list.values[0])
            
            return ast_list.values[0](*ast_list.values[1:])
    

def PRINT(s):
    return printer.pr_str(s, True)

def rep(s):
    readval = READ(s)
    evalval = EVAL(readval, repl_env)
    return PRINT(evalval)

def eval_ast(ast, env):
    if isinstance(ast, parser.StrSymbol):
        v = ast.val
        return env.get(v)
        
    elif isinstance(ast, parser.LispList):
        return parser.LispList([EVAL(x, env) for x in ast.values])
    else:
        return ast

# initial self-hosted functions
rep("(def! not (fn* (a) (if a false true)))")
rep('(def! load-file (fn* (f) (eval (read-string (str "(do " (slurp f) ")")))))')
rep('(def! *ARGV* (list))')

def mainloop():
    while True:
        s = input("user> ")
        try:
            print (rep(s))
        except ValueError as e:
            print(e)
        
if __name__ == "__main__":
    if len(sys.argv) == 1:
        mainloop()
    else:
        #print ("processing command line:", sys.argv)
        fn = sys.argv[1]
        #print ("processing file:", fn)        
        #print ("extra args:", sys.argv[2:])
        argStrings = [parser.LispString(x) for x in sys.argv[2:]]
        listObj = parser.LispList(argStrings)
        repl_env.set('*ARGV*', listObj)
        
        rep('(load-file "{0}")'.format(fn))
        #print("Done")
        
