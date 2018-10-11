def READ(s):
    return s

def EVAL(s):
    return s

def PRINT(s):
    return s

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
