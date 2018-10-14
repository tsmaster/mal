class Environment:
    def __init__(self, outer, binds, exprs):
        self.data = {}
        self.outer = outer
        for i, b in enumerate(binds):
            self.set(b, exprs[i])

    def set(self, key, val):
        self.data[key] = val
        #print ("self.data:", self.data.keys())

    def find(self, key):
        if key in self.data:
            return self

        if not self.outer:
            raise ValueError("'{0}' not found".format(key))

        return self.outer.find(key)

    def get(self, key):
        env = self.find(key)
        return env.data[key]

        
        
    
