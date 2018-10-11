import reader
import printer

def READ(s):
    malData = reader.read_str(s)
    return malData

def EVAL(s):
    return s

def PRINT(s):
    return printer.pr_str(s)

def rep(s):
    readval = READ(s)
    evalval = EVAL(readval)
    return PRINT(evalval)
    

def mainloop():
    while True:
        s = input("user> ")
        print (rep(s))
        
if __name__ == "__main__":
    mainloop()
