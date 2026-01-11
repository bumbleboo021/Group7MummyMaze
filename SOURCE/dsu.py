class DSU:
    def __init__(self, sz : int):
        self.sz = sz
        self.cha = [0] * ((sz + 1)**2)
        for i in range((sz + 1)**2) : 
            self.cha[i] = i
        pass
    def find(self, u : int):
        if u == self.cha[u]:
            return u
        self.cha[u] = self.find(self.cha[u])
        return self.cha[u]
        pass
    def union(self, u : int , v : int ):
        if self.find(u) == self.find(v):
            return False
        u = self.find(u)
        v = self.find(v)
        self.cha[u] = v
        return True
        pass
    def tra_ve_int(self,x : int, y : int,z : int):
        if z == 0 or z == 4:
            return x * (self.sz + 1) + y 
        if z == 1:
            return self.tra_ve_int(x , y + 1, 0)
        if z == 2:
            return self.tra_ve_int(x + 1, y + 1, 0)
        if z == 3:
            return self.tra_ve_int(x + 1, y , 0)
if __name__ == "__main__":
    a = DSU(2)
    a.union(1,2)
