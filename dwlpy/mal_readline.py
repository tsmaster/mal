import os
import sys
import readline as pyreadline

history_loaded = False
histfile = os.path.expanduser("~/.mal-history")
if sys.version_info[0] >= 3:
    rl = input
else:
    rl = raw_input

def readline(promptStr):
    try:
        #print(promptStr)
        #line = rl()
        line = rl(promptStr)
    except IOError:
        pass
    except EOFError:
        return None
    return line
