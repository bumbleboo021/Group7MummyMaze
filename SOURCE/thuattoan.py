from mecung import *
from nhanvat import *
from collections import deque
import random
import copy
class Thuat_toan:
    def __init__(self,mecung : Mecung,user_char : Char,xacuop : Char,xacuop_2 : Char = None,bom = None ,key = None):
        self.mecung = mecung
        self.user_char = user_char
        self.xacuop = xacuop
        self.xacuop_2 = xacuop_2
        self.bom = bom
        self.key = key
        pass
    def update_song(self):
        if self.key is not None:
            if self.user_char.pos() == self.key.pos():
                self.user_char.update_key(1)
                self.key.song = 0
        if self.user_char.pos() == self.xacuop.pos() and self.xacuop.song == 1:
            self.user_char.song = 0
            pass
        if self.xacuop_2 is not None:
            if self.user_char.pos() == self.xacuop_2.pos() and self.xacuop_2.song == 1:
                self.user_char.song = 0
            if self.xacuop.pos() == self.xacuop_2.pos() and self.xacuop.song == 1 and self.xacuop_2.song == 1:
                self.xacuop.song = 0
                self.xacuop_2.song = 0
        if self.bom is not None:
            if self.user_char.pos() == self.bom.pos():
                self.user_char.song = 0
            if self.xacuop.pos() == self.bom.pos():
                self.xacuop.song = 0
            if self.xacuop_2 is not None and self.xacuop_2.pos() == self.bom.pos():
                self.xacuop_2.song = 0
class Thuat_toan_easy(Thuat_toan):
    def apply(self, so_xac_uop : int):
        if so_xac_uop == 1:
            while 1 :
                i = random.randint(0,3)
                if self.xacuop.di_chuyen(i) :
                    return i
        else:
            while 1 :
                i = random.randint(0,3)
                j = random.randint(0,3)
                if self.xacuop.di_chuyen(i) and self.xacuop_2.di_chuyen(j):
                    return (i,j)
                    
class Thuat_toan_medium(Thuat_toan):
    def dis(self, huong, character):
        x_ = self.user_char.x 
        y_ = self.user_char.y
        x = character.x
        y = character.y
        if huong == 0:
            x -= 1
        if huong == 1:
            y += 1
        if huong == 2:
            x += 1
        if huong == 3:
            y -= 1
        return abs(x - x_) + abs(y - y_) 
    def apply(self, so_xac_uop : int):
        if so_xac_uop == 1:
            huong = -1
            ans = 1000000
            for i in range(4):
                if self.xacuop.di_chuyen(i) and self.dis(i) < ans:
                    ans = self.dis(i)
                    huong = i

            return huong
        else:
            huong1 = -1
            ans = 1000000
            for i in range(4):
                if self.xacuop.di_chuyen(i) and self.dis(i) < ans:
                    ans = self.dis(i)
                    huong1 = i
            ans = 1000000
            huong2 = -1
            for i in range(4):
                if self.xacuop_2.di_chuyen(i) and self.dis(i) < ans:
                    ans = self.dis(i)
                    huong2 = i
            return (huong1,huong2)
class Thuat_toan_hard(Thuat_toan):
    def apply(self, so_xac_uop : int):
        queue = deque()
        key = self.user_char.have_key
        self.user_char.update_key(0)
        queue.append(self.user_char)
        set_dinh = set()
        huong1 = -1
        huong2 = -1
        while len(queue) > 0:
            dinh_bfs = queue.popleft() 
            
            for huong in range(4):
                if self.xacuop.di_chuyen(huong) and dinh_bfs.pos(-1) == self.xacuop.pos(huong):
                    if huong1 == -1:
                        huong1 = huong
                if so_xac_uop == 2:
                    if self.xacuop_2.di_chuyen(huong) and dinh_bfs.pos(-1) == self.xacuop_2.pos(huong):
                        if huong2 == -1:
                            huong2 = huong
                if dinh_bfs.di_chuyen(huong)  and (dinh_bfs.pos(huong) not in set_dinh):
                    dinh_copy = copy.deepcopy(dinh_bfs)
                    dinh_copy.move_nhan_vat(huong)
                    queue.append(dinh_copy)
                    set_dinh.add(dinh_bfs.pos(huong))
        self.user_char.update_key(key)
        if so_xac_uop == 1:
            return huong1
        else:
            return huong1,huong2

            
        
        

