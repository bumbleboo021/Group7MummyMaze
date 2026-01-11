from mecung import *
class Char:
    def __init__(self,x : int, y : int, mecung : Mecung,have_key = 1, song = 1):
        self.x = x
        self.y = y
        self.mecung = mecung
        self.have_key = have_key
        self.song = song
    def update_key(self, x : int):
        self.have_key = x
    def pos(self,huong = -1):
        x = self.x
        y = self.y
        if huong == 0:
            x -= 1
        if huong == 1:
            y += 1
        if huong == 2:
            x += 1
        if huong == 3:
            y -=1 
        return (x,y)   
    def di_chuyen(self,huong : int):
        if self.mecung.door == (self.x,self.y,huong) and self.have_key:
            return 1
        if self.mecung.trang_thai(self.x,self.y,huong) == 0:
            if huong == 0:
                if self.mecung.trang_thai(self.x - 1,self.y,2) == 0:
                    
                    return 1
            if huong == 1:
                if self.mecung.trang_thai(self.x ,self.y + 1,3) == 0:
                    
                    return 1
            if huong == 2:
                if self.mecung.trang_thai(self.x + 1,self.y,0) == 0:
                    
                    return 1
            if huong == 3:
                if self.mecung.trang_thai(self.x ,self.y - 1,1) == 0:
                    
                    return 1
        return 0
    def move_nhan_vat(self,huong : int):
        if huong == 0:
            self.x -= 1
        elif huong == 1:
            self.y += 1
        elif huong == 2:
            self.x += 1
        elif huong == 3:
            self.y -= 1
    def out(self):
        if self.x < 0 or self.y < 0 or self.x >= self.mecung.sz or self.y >= self.mecung.sz:
            return 1
        return 0
