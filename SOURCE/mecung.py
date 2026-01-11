class Mecung:
    def __init__(self, sz : int,door = None):
        self.sz = sz
        self.matrix = []
        self.door = door
        for i in range(sz):
            self.matrix.append([])
            self.matrix[i] = [0]  * sz
    
    def trang_thai(self, x : int , y : int ,id : int):
        if x < 0 or y < 0 or x >= self.sz or y >= self.sz:
            return 1
        val = self.matrix[x][y]
        return ((val >> id ) & 1)
    def tim_cua_ra(self):
        for i in range(self.sz):
            if (self.matrix[0][i] >> 0) & 1 == 0: self.door = (0, i, 0); return
            if (self.matrix[self.sz-1][i] >> 2) & 1 == 0: self.door = (self.sz-1, i, 2); return
            if (self.matrix[i][0] >> 3) & 1 == 0: self.door = (i, 0, 3); return
            if (self.matrix[i][self.sz-1] >> 1) & 1 == 0: self.door = (i, self.sz-1, 1); return
    def __deepcopy__(self, memo): return self
if __name__ == "__main__":
    a = Mecung(6)
    