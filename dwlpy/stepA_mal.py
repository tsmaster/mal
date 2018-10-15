import sys
import traceback

import reader
import printer
import parser
import environment
import core
import mal_readline


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

        ast = macro_expand(ast, env)
        if not isinstance(ast, parser.LispList):
            return eval_ast(ast, env)
        
        op = ast.values[0]
        #print ("op", op)
        if isinstance(op, parser.StrSymbol) and op.val == 'def!':
            """call the set method of the current environment (second parameter of
            EVAL called env) using the unevaluated first parameter (second
            list element) as the symbol key and the evaluated second
            parameter as the value."""
            val = EVAL(ast.values[2], env)
            #print ("defining", ast.values[1].val)
            env.set(ast.values[1].val, val)
            return val
        if isinstance(op, parser.StrSymbol) and op.val == 'defmacro!':
            val = EVAL(ast.values[2], env)
            val.setMacro(True)
            env.set(ast.values[1].val, val)
            return val
        elif isinstance(op, parser.StrSymbol) and op.val == 'let*':
            newenv = environment.Environment(env, [], [])
            for i in range(0, len(ast.values[1].values), 2):
                name = ast.values[1].values[i].val
                val = EVAL(ast.values[1].values[i+1], newenv)
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
        elif isinstance(op, parser.StrSymbol) and op.val == 'quote':
            return ast.values[1]
        elif isinstance(op, parser.StrSymbol) and op.val == 'quasiquote':
            ast = quasiquote(ast.values[1])
            continue
        elif isinstance(op, parser.StrSymbol) and op.val == 'macroexpand':
            return macro_expand(ast.values[1], env)
        elif isinstance(op, parser.StrSymbol) and op.val == 'try*':
            catchop = ast.values[2].values[0]
            if isinstance(catchop, parser.StrSymbol) and catchop.val == 'catch*':
                try:
                    return EVAL(ast.values[1], env)
                except parser.MalException as me:
                    ex_label = ast.values[2].values[1].val
                    newenv = environment.Environment(env, [ex_label], [me.mal_obj])
                    return EVAL(ast.values[2].values[2], newenv)
                    
                except Exception as e:
                    ex_label = ast.values[2].values[1].val
                    ex_type, ex_val, ex_tb = sys.exc_info()
                    traceback.print_exc()
                    ex_str = parser.LispString(str(e) + str(ex_tb))
                    newenv = environment.Environment(env, [ex_label], [ex_str])
                    return EVAL(ast.values[2].values[2], newenv)
            else:
                return EVAL(ast.values[1], env)
        else:
            ast_list = eval_ast(ast, env)
            
            if isinstance(ast_list.values[0], parser.FuncClosure):
                func = ast_list.values[0]

                ast = func.body
                env = func.prepareEnv(ast_list.values[1:])
                continue
    
            #print ("about to call", ast_list.values[0])
            
            return ast_list.values[0](*ast_list.values[1:])


def is_macro_call(ast, env):
    if (isinstance(ast, parser.LispList) and
        isinstance(ast.values[0], parser.StrSymbol)):
        try:
            v = env.get(ast.values[0].val)
        except ValueError:
            return False
        return (isinstance(v, parser.FuncClosure) and
                v.isMacro)
    return False

def macro_expand(ast, env):
    while is_macro_call(ast, env):
        macro_func = env.get(ast.values[0].val)
        ast = macro_func.call(ast.values[1:])
    return ast

def is_pair(p):
    if (isinstance(p, parser.LispList) or
        isinstance(p, parser.LispVector)):
        return len(p.values) > 0
    return False

def quasiquote(ast):
    #print ("quasiquote with", printer.pr_str(ast, True))
    if not is_pair(ast):
        #print("step i: ast is not pair", ast)
        return parser.LispList([parser.StrSymbol('quote'), ast])
    if (isinstance(ast.values[0], parser.StrSymbol) and
        ast.values[0].val == 'unquote'):
        #print("step ii : found 'unquote'")
        return ast.values[1]
    if is_pair(ast.values[0]):
        zz = ast.values[0].values[0]
        #print ("zz", zz)
        #print ("t(zz)", type(zz))
        if isinstance(zz, parser.StrSymbol) and zz.val == 'splice-unquote':
            #print("step iii : found 'splice-unquote'")
            return parser.LispList([parser.StrSymbol('concat'),
                                    ast.values[0].values[1],
                                    quasiquote(parser.LispList(ast.values[1:]))])
    #print("step iv : else")
    return parser.LispList([parser.StrSymbol('cons'),
                            quasiquote(ast.values[0]),
                            quasiquote(parser.LispList(ast.values[1:]))])
                      

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
    elif isinstance(ast, parser.LispVector):
        return parser.LispVector([EVAL(x, env) for x in ast.values])
    elif isinstance(ast, parser.LispHashMap):
        keyvals = []
        for k in ast.keys():
            keyvals.append(EVAL(k, env))
            keyvals.append(EVAL(ast.lookup(k), env))
        return parser.LispHashMap(keyvals)
    else:
        return ast

# initial self-hosted functions
rep("(def! not (fn* (a) (if a false true)))")
rep('(def! load-file (fn* (f) (eval (read-string (str "(do " (slurp f) ")")))))')
rep('(def! *ARGV* (list))')
rep("(defmacro! cond (fn* (& xs) (if (> (count xs) 0) (list 'if (first xs) (if (> (count xs) 1) (nth xs 1) (throw \"odd number of forms to cond\")) (cons 'cond (rest (rest xs)))))))")
if sys.version_info[0] == 3:
    rep('(def! *host-language* "python3")')
else:
    rep('(def! *host-language* "python2.7")')
rep('(def! *gensym-counter* (atom 0))')
rep('(def! gensym (fn* [] (symbol (str \"G__\" (swap! *gensym-counter* (fn* [x] (+ 1 x)))))))')
rep('(defmacro! or (fn* (& xs) (if (empty? xs) nil (if (= 1 (count xs)) (first xs) (let* (condvar (gensym)) `(let* (~condvar ~(first xs)) (if ~condvar ~condvar (or ~@(rest xs)))))))))')

def mainloop():
    rep('(println (str "Mal [" *host-language* "]"))')
    while True:
        try:
            s = mal_readline.readline("user> ")
            print (rep(s))
        except ValueError as e:
            print(e)
        except IndexError as e:
            print(e)
        except parser.MalException as me:
            print(me)
            print(printer.pr_str(me.mal_obj, True))
        except SyntaxError as e:
            print(e)
        except EOFError:
            print("\nBye!")
            return
        except AttributeError as e:
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

        try:
            rep('(load-file "{0}")'.format(fn))
        except SyntaxError as e:
            print(e)
        #print("Done")
        
