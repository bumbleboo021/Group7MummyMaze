import pygame
import sys
import random
import json
import os
from collections import deque
import copy 
from linklist import Queue
from dsu import *
from mecung import *
pygame.init()
screen_rong = 1200
screen_dai = 600
screen = pygame.display.set_mode((screen_rong,screen_dai))
clock = pygame.time.Clock()
FPS = 60

#color
DEN = (0, 0, 0)                  
TRANG = (255, 255, 255)            
DO = (255, 0, 0)                 
XANH_LA = (0, 255, 0)              
XANH_LAM = (0, 0, 255)            
VANG = (255, 255, 0)               
TIM = (255, 0, 255)                
XANH_NGOC = (0, 255, 255)          
CAM = (255, 165, 0)                
XAM_TRUNG_BINH = (128, 128, 128)
NAU_DAM = (139, 69, 19)   

run = 1
huy = 1
turn_step = 0 


#nguyen chi bao
def tao_me_cung_6():
    with open('maps.json', 'r') as f:
        data = json.load(f)
    map_data = data["1"]
    sz = 6
    mc = Mecung(sz)
    mc.matrix = map_data['matrix']
    mc.tim_cua_ra()
    return mc

def tao_me_cung_8():
    with open('maps.json', 'r') as f:
        data = json.load(f)
    map_data = data["6"]
    sz = 8
    mc = Mecung(sz)
    mc.matrix = map_data['matrix']
    mc.tim_cua_ra()
    return mc

def tao_me_cung_10():
    with open('maps.json', 'r') as f:
        data = json.load(f)
    map_data = data["11"]
    sz = 10
    mc = Mecung(sz)
    mc.matrix = map_data['matrix']
    mc.tim_cua_ra()
    return mc

def getbit(n, k):
    return (n >> k) & 1

def tao_me_cung_random(n):
    mecung = Mecung(n)
    dem_so_canh = 0
    dsu = DSU(n)
    
    #Bao mê cung
    for x in range(n):
        mecung.matrix[0][x] += 1
        dsu.union(dsu.tra_ve_int(0,x,0),dsu.tra_ve_int(0,x,1))
        mecung.matrix[n - 1][x] += 4
        dsu.union(dsu.tra_ve_int(n - 1,x,2),dsu.tra_ve_int(n - 1,x,3))
        mecung.matrix[x][0] += 8
        dsu.union(dsu.tra_ve_int(x,0,3),dsu.tra_ve_int(x,0,0))
        mecung.matrix[x][n - 1] += 2
        dsu.union(dsu.tra_ve_int(x,n - 1,1),dsu.tra_ve_int(x,n - 1,2))
        
    #Xử lí chu trình 
    for x in range(n):
        dem = 0
        ok = 0
        for y in range(n):
            if y == n//2 and ok == 0:
                ok = 1
                dem = 0
            val = random.randint(0,15)
            val = val ^ mecung.matrix[x][y]
            for id in range(4):
                if getbit(val,id) :
                    if dsu.union( dsu.tra_ve_int(x,y,id) , dsu.tra_ve_int(x,y,id + 1) ) == 0 or dem >= n//4:
                        val -= (1 << id)
                    else:
                        dem += 1
            mecung.matrix[x][y] |= val

    for x in range(n):
        for y in range(n):
            val = mecung.matrix[x][y]
            if (val >> 0) & 1 and x > 0: 
                mecung.matrix[x-1][y] |= (1 << 2)
            if (val >> 1) & 1 and y < n - 1: 
                mecung.matrix[x][y+1] |= (1 << 3)
            if (val >> 2) & 1 and x < n - 1: 
                mecung.matrix[x+1][y] |= (1 << 0)
            if (val >> 3) & 1 and y > 0: 
                mecung.matrix[x][y-1] |= (1 << 1)

    #Tạo cửa ra
    huong = random.randint(0,3)
    hang_or_cot = random.randint(0,n - 1)
    if huong == 0:
        mecung.door = (0,hang_or_cot,0)
    if huong == 1:
        mecung.door = (hang_or_cot,n - 1,1)
    if huong == 2:
        mecung.door = (n-1,hang_or_cot,2)
    if huong == 3:
        mecung.door = (hang_or_cot,0,3)

    player_pos = [0, 0]
    mummy_pos = [[0, 0]]

    dp = [[[[[0] * 3 for _ in range(n)] 
                       for _ in range(n)] 
                       for _ in range(n)] 
                       for _ in range(n)]
    q = Queue()
    for x in range(n):
        for y in range(n):
            if x != mecung.door[0] and y != mecung.door[1]:
                dp[mecung.door[0]][mecung.door[1]][x][y][0] = 1
                q.push((mecung.door[0],mecung.door[1],x,y,0))
            for buoc in range(3):
                dp[x][y][x][y][buoc] = 2
                q.push((x,y,x,y,buoc))
    hx = [-1,0,1,0]
    hy = [0,1,0,-1]
    while q.len >  0:
        trang_thai = q.pop()
        buoc = trang_thai[4]
        buoc += 2
        buoc %= 3
        xuser = trang_thai[0]
        yuser = trang_thai[1]
        xmm = trang_thai[2]
        ymm = trang_thai[3]
        if buoc == 0:
            for huong in range(4):
                xuser_new = xuser + hx[huong]
                yuser_new = yuser + hy[huong]
                if mecung.trang_thai(xuser,yuser,huong) == 0 and mecung.trang_thai(xuser_new,yuser_new,(huong+2)%4) == 0:
                    if dp[xuser_new][yuser_new][xmm][ymm][buoc] == 0:
                        dp[xuser_new][yuser_new][xmm][ymm][buoc] = dp[xuser][yuser][xmm][ymm][(buoc+1)%3]
                        q.push((xuser_new,yuser_new,xmm,ymm,buoc))
                    elif dp[xuser_new][yuser_new][xmm][ymm][buoc] == 2:
                        dp[xuser_new][yuser_new][xmm][ymm][buoc] = dp[xuser][yuser][xmm][ymm][(buoc+1)%3]
                        if dp[xuser_new][yuser_new][xmm][ymm][buoc] == 1:
                            q.push((xuser_new,yuser_new,xmm,ymm,buoc))
        else:
            for huong in range(4):
                xmm_new = xmm + hx[huong]
                ymm_new = ymm + hy[huong]
                if mecung.trang_thai(xmm,ymm,huong) == 0 and mecung.trang_thai(xmm_new,ymm_new,(huong+2)%4) == 0:
                    if dp[xuser][yuser][xmm_new][ymm_new][buoc] == 0:
                        dp[xuser][yuser][xmm_new][ymm_new][buoc] = dp[xuser][yuser][xmm][ymm][(buoc+1)%3]
                        q.push((xuser,yuser,xmm_new,ymm_new,buoc))
                    elif dp[xuser][yuser][xmm_new][ymm_new][buoc] == 1:
                        dp[xuser][yuser][xmm_new][ymm_new][buoc] = dp[xuser][yuser][xmm][ymm][(buoc+1)%3]
                        if dp[xuser][yuser][xmm_new][ymm_new][buoc] == 2:
                            q.push((xuser,yuser,xmm_new,ymm_new,buoc))
                    
    while True:
        px, py = random.randint(0, n - 1), random.randint(0, n - 1)
        mx, my = random.randint(0, n - 1), random.randint(0, n - 1)
        
        if (px, py) != (mx, my) and dp[px][py][mx][my][0] == 1:
            player_pos = [px, py]
            mummy_pos = [[mx, my]]
            break

    key_pos = None
    bom_pos = None

    return mecung, player_pos, mummy_pos, key_pos, bom_pos

try:
    from nhanvat import Char
    def char_fast_copy(self, memo):
        return Char(self.x, self.y, self.mecung, self.have_key, self.song)
    Char.__deepcopy__ = char_fast_copy
except ImportError: pass

# --- VE ITEMS  ---
def ve_items(screen, cell_size, offset_x, offset_y):
    # 1. VẼ KEY
    if 'key_pos' in globals() and globals()['key_pos'] is not None:
        kr, kc = globals()['key_pos']
        # Load anh neu chua co
        if 'key_img_scaled' not in globals() or globals().get('last_cell_size') != cell_size:
            if 'key_img_raw' in globals() and globals()['key_img_raw']:
                globals()['key_img_scaled'] = pygame.transform.scale(globals()['key_img_raw'], (int(cell_size*0.6), int(cell_size*0.6)))
            else: globals()['key_img_scaled'] = None
        
        # Ve key
        kx = offset_x + kc * cell_size + (cell_size * 0.2)
        ky = offset_y + kr * cell_size + (cell_size * 0.2)
        
        if globals().get('key_img_scaled'):
            screen.blit(globals()['key_img_scaled'], (kx, ky))
        else:
            pygame.draw.circle(screen, VANG, (int(kx + cell_size*0.3), int(ky + cell_size*0.3)), 10)

    # 2. VẼ BOM
    if 'bom_pos' in globals() and globals()['bom_pos'] is not None:
        br, bc = globals()['bom_pos']
        if 'bom_img_scaled' not in globals() or globals().get('last_cell_size') != cell_size:
            if 'bom_img_raw' in globals() and globals()['bom_img_raw']:
                globals()['bom_img_scaled'] = pygame.transform.scale(globals()['bom_img_raw'], (int(cell_size*0.8), int(cell_size*0.8)))
            else: globals()['bom_img_scaled'] = None
            
        bx = offset_x + bc * cell_size + (cell_size * 0.1)
        by = offset_y + br * cell_size + (cell_size * 0.1)
        
        if globals().get('bom_img_scaled'):
            screen.blit(globals()['bom_img_scaled'], (bx, by))
        else:
            pygame.draw.circle(screen, (50, 50, 50), (int(bx + cell_size*0.4), int(by + cell_size*0.4)), 15)

    globals()['last_cell_size'] = cell_size

def ve_player(screen, cell_size, offset_x, offset_y, player_pos=None):
    if 'p_state' not in globals():
        globals()['p_state'] = {
            'pixel_x': None, 'pixel_y': None, 'target_x': None, 'target_y': None, 
            'grid_r': 0, 'grid_c': 0, 'direction': 2, 'is_moving': False,                 
            'frame_index': 0, 'last_update': 0, 'imgs': {}                          
        }
    st = globals()['p_state']
    
    if player_pos is None:
        if 'player_pos' in globals(): player_pos = globals()['player_pos']
        else: player_pos = [0, 0]

    grid_x = offset_x + player_pos[1] * cell_size
    grid_y = offset_y + player_pos[0] * cell_size
    
    if st['pixel_x'] is None or abs(st['pixel_x'] - grid_x) > cell_size * 2:
        st['pixel_x'], st['pixel_y'] = grid_x, grid_y
        st['target_x'], st['target_y'] = grid_x, grid_y
        st['grid_r'], st['grid_c'] = player_pos[0], player_pos[1]

    if not st['imgs']:
        idle_files = ["assets/up.png", "assets/right.png", "assets/down.png", "assets/left.png"]
        st['imgs']['idle'] = []
        for f in idle_files:
            img = pygame.image.load(f)
            st['imgs']['idle'].append(pygame.transform.scale(img, (cell_size, cell_size)))

        move_files = ["assets/move_up.png", "assets/move_right.png", "assets/move_down.png", "assets/move_left.png"]
        st['imgs']['move'] = []
        for f in move_files:
            sheet = pygame.image.load(f)
            sheet_w, sheet_h = sheet.get_size()
            num_frames = max(1, sheet_w // sheet_h)
            frames = []
            for i in range(num_frames):
                frame = sheet.subsurface((i * sheet_h, 0, sheet_h, sheet_h))
                frames.append(pygame.transform.scale(frame, (cell_size, cell_size)))
            st['imgs']['move'].append(frames)

    SPEED = cell_size / 16.0 
    if st['is_moving']:
        if st['pixel_x'] < st['target_x']: st['pixel_x'] = min(st['pixel_x'] + SPEED, st['target_x'])
        elif st['pixel_x'] > st['target_x']: st['pixel_x'] = max(st['pixel_x'] - SPEED, st['target_x'])
        if st['pixel_y'] < st['target_y']: st['pixel_y'] = min(st['pixel_y'] + SPEED, st['target_y'])
        elif st['pixel_y'] > st['target_y']: st['pixel_y'] = max(st['pixel_y'] - SPEED, st['target_y'])

        if abs(st['pixel_x'] - st['target_x']) < 1 and abs(st['pixel_y'] - st['target_y']) < 1:
            st['pixel_x'] = st['target_x']
            st['pixel_y'] = st['target_y']
            st['is_moving'] = False
            player_pos[0] = st['grid_r']
            player_pos[1] = st['grid_c']

    current_time = pygame.time.get_ticks()
    image_to_draw = None
    if st['imgs']:
        if st['is_moving']:
            anim_frames = st['imgs']['move'][st['direction']]
            if current_time - st['last_update'] > 60:
                st['frame_index'] = (st['frame_index'] + 1) % len(anim_frames)
                st['last_update'] = current_time
            image_to_draw = anim_frames[st['frame_index']]
        else:
            image_to_draw = st['imgs']['idle'][st['direction']]
            st['frame_index'] = 0 
    
    if image_to_draw: screen.blit(image_to_draw, (int(st['pixel_x']), int(st['pixel_y'])))
    else: pygame.draw.rect(screen, (0, 0, 255), (int(st['pixel_x'] + cell_size/2), int(st['pixel_y'] + cell_size/2)), cell_size//3)

def ve_mummy(screen, cell_size, offset_x, offset_y, mummy_pos_list=None):
    if 'm_states' not in globals(): globals()['m_states'] = {}
    if 'MUMMY_IMGS' not in globals(): globals()['MUMMY_IMGS'] = {}
    m_states = globals()['m_states']
    m_imgs = globals()['MUMMY_IMGS']

    if mummy_pos_list is None:
        if 'mummy_pos' in globals(): mummy_pos_list = globals()['mummy_pos']
        elif 'a' in globals(): sz = globals()['a'].sz; mummy_pos_list = [[sz - 1, sz - 1]]
        else: mummy_pos_list = []

    if not m_imgs:
        idle_files = ["assets/mumUp.png", "assets/mumRight.png", "assets/mumDown.png", "assets/mumLeft.png"]
        m_imgs['idle'] = []
        for f in idle_files:
            img = pygame.image.load(f)
            m_imgs['idle'].append(pygame.transform.scale(img, (cell_size, cell_size)))
        
        move_files = ["assets/mummy_up.png", "assets/mummy_right.png", "assets/mummy_down.png", "assets/mummy_left.png"]
        m_imgs['move'] = []
        for f in move_files:
            sheet = pygame.image.load(f)
            sheet_w, sheet_h = sheet.get_size()
            num_frames = max(1, sheet_w // sheet_h)
            frames = []
            for i in range(num_frames):
                frame = sheet.subsurface((i * sheet_h, 0, sheet_h, sheet_h))
                frames.append(pygame.transform.scale(frame, (cell_size, cell_size)))
            m_imgs['move'].append(frames)

    current_time = pygame.time.get_ticks()
    SPEED = cell_size / 16.0

    for i, pos in enumerate(mummy_pos_list):
        if i not in m_states:
            m_states[i] = {
                'pixel_x': None, 'pixel_y': None, 'target_x': None, 'target_y': None,
                'grid_r': pos[0], 'grid_c': pos[1], 'direction': 2, 'is_moving': False,
                'frame_index': 0, 'last_update': 0
            }
        st = m_states[i]
        
        target_grid_r, target_grid_c = pos[0], pos[1]
        target_pixel_x = offset_x + target_grid_c * cell_size
        target_pixel_y = offset_y + target_grid_r * cell_size

        if st['pixel_x'] is None or abs(st['pixel_x'] - target_pixel_x) > cell_size * 5:
            st['pixel_x'], st['pixel_y'] = target_pixel_x, target_pixel_y
            st['grid_r'], st['grid_c'] = target_grid_r, target_grid_c
        if (st['grid_r'] != target_grid_r or st['grid_c'] != target_grid_c) and not st['is_moving']:
            if target_grid_r < st['grid_r']: st['direction'] = 0
            elif target_grid_c > st['grid_c']: st['direction'] = 1
            elif target_grid_r > st['grid_r']: st['direction'] = 2
            elif target_grid_c < st['grid_c']: st['direction'] = 3
            st['is_moving'] = True
            st['grid_r'], st['grid_c'] = target_grid_r, target_grid_c

        st['target_x'], st['target_y'] = target_pixel_x, target_pixel_y

        if st['is_moving']:
            if st['pixel_x'] < st['target_x']: st['pixel_x'] = min(st['pixel_x'] + SPEED, st['target_x'])
            elif st['pixel_x'] > st['target_x']: st['pixel_x'] = max(st['pixel_x'] - SPEED, st['target_x'])
            if st['pixel_y'] < st['target_y']: st['pixel_y'] = min(st['pixel_y'] + SPEED, st['target_y'])
            elif st['pixel_y'] > st['target_y']: st['pixel_y'] = max(st['pixel_y'] - SPEED, st['target_y'])
            
            if abs(st['pixel_x'] - st['target_x']) < 1 and abs(st['pixel_y'] - st['target_y']) < 1:
                st['pixel_x'], st['pixel_y'] = st['target_x'], st['target_y']
                st['is_moving'] = False

        image_to_draw = None
        if m_imgs and 'move' in m_imgs:
            if st['is_moving']:
                anim_frames = m_imgs['move'][st['direction']]
                if current_time - st['last_update'] > 50: 
                    st['frame_index'] = (st['frame_index'] + 1) % len(anim_frames)
                    st['last_update'] = current_time
                image_to_draw = anim_frames[st['frame_index']]
            else:
                image_to_draw = m_imgs['idle'][st['direction']]
                st['frame_index'] = 0

        if image_to_draw: screen.blit(image_to_draw, (int(st['pixel_x']), int(st['pixel_y'])))
        else: pygame.draw.rect(screen, DO, (int(st['pixel_x'])+10, int(st['pixel_y'])+10, cell_size-20, cell_size-20))

def xu_ly_am_thanh(screen, dang_nhap, menu):
    if 'AM_THANH_BAT' not in globals(): globals()['AM_THANH_BAT'] = True
    if 'PREV_MOUSE_PRESSED' not in globals(): globals()['PREV_MOUSE_PRESSED'] = False
    if 'DA_PHAT_SFX' not in globals(): globals()['DA_PHAT_SFX'] = False

    if 'SND_VIC' not in globals():
        globals()['SND_VIC'] = pygame.mixer.Sound("assets/snd_win.mp3")
    if 'SND_DEF' not in globals():
        globals()['SND_DEF'] = pygame.mixer.Sound("assets/snd_lose.mp3")
    if 'SND_PROX' not in globals():
        globals()['SND_PROX'] = pygame.mixer.Sound("assets/snd_prox.mp3")
    if 'LAST_PROX_TIME' not in globals(): globals()['LAST_PROX_TIME'] = 0

    # --- BUTTON CONFIG ---
    btn_x, btn_y = 1130, 60 
    radius = 50 
    
    mouse_x, mouse_y = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()[0]
    dist = ((mouse_x - btn_x)**2 + (mouse_y - btn_y)**2)**0.5
    
    if dist <= radius:
        if click and not globals()['PREV_MOUSE_PRESSED']:
            globals()['AM_THANH_BAT'] = not globals()['AM_THANH_BAT']
    globals()['PREV_MOUSE_PRESSED'] = click
    bat_nhac = globals()['AM_THANH_BAT']

    if menu == 2 or menu == 3:
        if pygame.mixer.music.get_busy(): pygame.mixer.music.stop()
        if bat_nhac and not globals()['DA_PHAT_SFX']:
            if menu == 3 and globals()['SND_VIC']: globals()['SND_VIC'].play()
            if menu == 2 and globals()['SND_DEF']: globals()['SND_DEF'].play()
            globals()['DA_PHAT_SFX'] = True
            
    else:
        globals()['DA_PHAT_SFX'] = False
        # --- NHAC NEN  ---
        can_phat = (dang_nhap or (menu == 1)) and bat_nhac
        dang_phat = pygame.mixer.music.get_busy()
        if can_phat and not dang_phat:
            pygame.mixer.music.load("assets/snd_bg.mp3")
            pygame.mixer.music.play(-1)
        elif not can_phat and dang_phat:
            pygame.mixer.music.stop()

        if menu == 0 and bat_nhac:
            if 'player_pos' in globals() and 'mummy_pos' in globals():
                p = globals()['player_pos']
                gan_mummy = False
                for m in globals()['mummy_pos']:
                    kc = abs(p[0] - m[0]) + abs(p[1] - m[1])
                    if kc < 3:
                        gan_mummy = True
                        break
                if gan_mummy:
                    curr_time = pygame.time.get_ticks()
                    if curr_time - globals()['LAST_PROX_TIME'] > 2000:
                        if globals()['SND_PROX']: globals()['SND_PROX'].play()
                        globals()['LAST_PROX_TIME'] = curr_time

def player_move(event, player_pos, maze): 
    try: from nhanvat import Char
    except ImportError: return

    if globals()['turn_step'] != 0: return
    if 'p_state' not in globals(): return
    st = globals()['p_state']
    if st['is_moving']: return

    if event.type == pygame.KEYDOWN:
        huong = -1
        if event.key == pygame.K_UP: huong = 0
        elif event.key == pygame.K_RIGHT: huong = 1
        elif event.key == pygame.K_DOWN: huong = 2
        elif event.key == pygame.K_LEFT: huong = 3
        
        if huong != -1:
            st['direction'] = huong
            
            # --- CHECK VICTORY (EXIT) ---
            if maze.door == (player_pos[0], player_pos[1], huong):
                # LOGIC KEY: Check xem co key tren ban do khong
                if 'key_pos' in globals() and globals()['key_pos'] is not None:
                    # Chua an key -> Khong duoc qua
                    return 
                else:
                    globals()['menu_start'] = 3
                    return

            nv = Char(player_pos[0], player_pos[1], maze)
            if nv.di_chuyen(huong):
                # --- SAVE STATE FOR UNDO ---
                if 'undo_stack' not in globals(): globals()['undo_stack'] = []
                mummy_copy = [m[:] for m in globals()['mummy_pos']]
                state = {'p': player_pos[:], 'm': mummy_copy}
                globals()['undo_stack'].append(state)

                if 'AM_THANH_BAT' in globals() and globals()['AM_THANH_BAT']:
                    # --- LOAD AM THANH DI CHUYEN ---
                    if 'SND_MOVE' not in globals():
                        globals()['SND_MOVE'] = pygame.mixer.Sound("assets/snd_move.mp3")
                    globals()['SND_MOVE'].play()
                
                next_r, next_c = player_pos[0], player_pos[1]
                if huong == 0: next_r -= 1
                elif huong == 1: next_c += 1
                elif huong == 2: next_r += 1
                elif huong == 3: next_c -= 1
                
                # --- CHECK BOM (PLAYER CHAM BOM -> DEFEAT) ---
                if 'bom_pos' in globals() and globals()['bom_pos'] == [next_r, next_c]:
                    globals()['menu_start'] = 2
                    return

                # --- CHECK KEY (PLAYER AN KEY) ---
                if 'key_pos' in globals() and globals()['key_pos'] == [next_r, next_c]:
                    globals()['key_pos'] = None # Key bien mat

                # --- TINH TOAN LAI OFFSET (CO MARGIN 1 CELL) ---
                SIDEBAR_W = 260
                HEADER_H = 120 
                screen_rong, screen_dai = 1200, 600
                
                available_h = screen_dai - HEADER_H
                
                cell_size = available_h // (maze.sz + 2)
                
                maze_pixel_w = maze.sz * cell_size
                maze_pixel_h = a.sz * cell_size
                
                total_content_h = HEADER_H + maze_pixel_h
                offset_y_header = (screen_dai - total_content_h) // 2
                offset_y = offset_y_header + HEADER_H
                
                available_w = screen_rong - SIDEBAR_W
                offset_x = SIDEBAR_W + (available_w - maze_pixel_w) // 2
                
                st['target_x'] = offset_x + next_c * cell_size
                st['target_y'] = offset_y + next_r * cell_size
                st['grid_r'] = next_r
                st['grid_c'] = next_c
                st['is_moving'] = True
                
                globals()['turn_step'] = 1
                
def mummy_move(mummy_list, player_target_pos, maze, difficulty): 
    try:
        from nhanvat import Char
        from thuattoan import Thuat_toan_easy, Thuat_toan_medium, Thuat_toan_hard
    except ImportError: return

    if not mummy_list: return

    p_char = Char(player_target_pos[0], player_target_pos[1], maze)
    m1_sim = Char(mummy_list[0][0], mummy_list[0][1], maze)
    m2_sim = None
    if len(mummy_list) > 1: m2_sim = Char(mummy_list[1][0], mummy_list[1][1], maze)
    
    algo = None
    if difficulty == "DE": algo = Thuat_toan_easy(maze, p_char, m1_sim, m2_sim)
    elif difficulty == "TRUNG BINH": algo = Thuat_toan_medium(maze, p_char, m1_sim, m2_sim)
    elif difficulty == "KHO": algo = Thuat_toan_hard(maze, p_char, m1_sim, m2_sim)
    
    d1, d2 = -1, -1
    if algo:
        result = algo.apply(len(mummy_list))
        if len(mummy_list) == 1: d1 = result
        elif len(mummy_list) == 2: d1, d2 = result

    if d1 != -1 and len(mummy_list) > 0:
        m1 = Char(mummy_list[0][0], mummy_list[0][1], maze)
        m1.move_nhan_vat(d1)
        mummy_list[0][0], mummy_list[0][1] = m1.x, m1.y
        
        if 'bom_pos' in globals() and globals()['bom_pos'] == [m1.x, m1.y]:
             globals()['bom_pos'] = None
             mummy_list.pop(0)
             
             if len(mummy_list) > 0 and d2 != -1:
                  m2 = Char(mummy_list[0][0], mummy_list[0][1], maze)
                  m2.move_nhan_vat(d2)
                  mummy_list[0][0], mummy_list[0][1] = m2.x, m2.y
                  if 'bom_pos' in globals() and globals()['bom_pos'] == [m2.x, m2.y]:
                       globals()['bom_pos'] = None
                       mummy_list.pop(0)
             return 

        if len(mummy_list) > 1:
             if mummy_list[0] == mummy_list[1]:
                  mummy_list.pop(1)
                  return 

    if d2 != -1 and len(mummy_list) > 1:
        m2 = Char(mummy_list[1][0], mummy_list[1][1], maze)
        m2.move_nhan_vat(d2)
        mummy_list[1][0], mummy_list[1][1] = m2.x, m2.y

        if 'bom_pos' in globals() and globals()['bom_pos'] == [m2.x, m2.y]:
             globals()['bom_pos'] = None
             mummy_list.pop(1)
             return

        if mummy_list[0] == mummy_list[1]:
             mummy_list.pop(1)
                
def khoi_tao_game():
    global a, player_pos, mummy_pos, level_chon, size_chon
    
    if 'undo_stack' in globals(): globals()['undo_stack'] = []
    
    if level_chon == "RANDOM":
        a, p_pos, m_pos, k_pos, b_pos = tao_me_cung_random(size_chon)
        player_pos = list(p_pos)
        
        mummy_pos = list(m_pos) 
        
        globals()['key_pos'] = list(k_pos) if k_pos else None
        globals()['bom_pos'] = list(b_pos) if b_pos else None
    else:
        with open('maps.json', 'r') as f:
            data = json.load(f)
        map_data = data[str(level_chon)]
        matrix_data = map_data['matrix']
        a = Mecung(len(matrix_data))
        a.matrix = matrix_data
        a.tim_cua_ra()
        player_pos = map_data.get("player") or [0, 0]
        mummy_pos = map_data.get("mummy") or []
        # LOAD KEY VA BOM TU FILE JSON
        globals()['key_pos'] = map_data.get("key") 
        globals()['bom_pos'] = map_data.get("bom")
    
    if 'p_state' in globals(): del globals()['p_state']
    if 'm_states' in globals(): del globals()['m_states']
    globals()['turn_step'] = 0

#nguyen mai khoi

def chuyen_man_ke():
    global level_chon
    if level_chon != "RANDOM":
        level_chon += 1
        if level_chon > 20: level_chon = 1
    khoi_tao_game()

#nguyen anh huy

# VẼ GIAO DIỆN
font = pygame.font.SysFont(None, 60)
font_nho = pygame.font.SysFont(None, 30)
font_to = pygame.font.SysFont(None, 100)

choi_btn = pygame.Rect(340, 140, 520, 155)
hd_btn   = pygame.Rect(340, 335, 520, 155)

def ve_nut(rect, text, color):
    pygame.draw.rect(screen, color, rect, border_radius=12)
    label = font_nho.render(text, True, TRANG) 
    screen.blit(label, label.get_rect(center=rect.center))

# VẼ 20 Ô MÀN CHƠI
level_chon = -1
level_rects = []
cols, rows = 5, 4

w = 85      
h = 55

gap_x = 36
gap_y = 19

start_x = 310
start_y = 163

for i in range(20):
    row, col = i // cols, i % cols
    rect = pygame.Rect(start_x + col * (w + gap_x), start_y + row * (h + gap_y), w, h)
    level_rects.append(rect)

# NÚT RAMDOM MAZE
random_btn = pygame.Rect(350, 515, 480, 60)

# CÁC NÚT ĐỘ KHÓ
de_btn  = pygame.Rect(365, 120, 470, 140)
tb_btn  = pygame.Rect(365, 280, 470, 140)
kho_btn = pygame.Rect(365, 440, 470, 140)

menu_start=1

# CÀI ĐẶT LƯU DỮ LIỆU VÀO TÀI KHOẢN
acc_file="account.json"
def load_acc():
    if not os.path.exists(acc_file): return {}
    with open(acc_file,"r") as fin: return json.load(fin)

def save_acc(data):
    with open(acc_file,"w") as fin: json.dump(data,fin)

def create_acc(tai_khoan, mat_khau):
    accs = load_acc()
    if tai_khoan in accs: return False, "TAI KHOAN DA TON TAI!"
    if tai_khoan == "" or mat_khau == "": return False, "KHONG DUOC DE TRONG!"
    
    # Thêm trường "VI TRI" (mặc định là [0, 0])
    accs[tai_khoan] = {
        "MAT KHAU": mat_khau,
        "MAN CHOI HIEN TAI": 1, 
        "DO KHO": "DE",
        "VI TRI": [0, 0] 
    }
    save_acc(accs)
    return True, "DANG KY THANH CONG"

def update_progress(tai_khoan, level_vua_thang, vi_tri_moi):
    accs = load_acc()
    if tai_khoan in accs:
        # Nếu thắng màn hiện tại, mở khóa màn tiếp theo
        if level_vua_thang == accs[tai_khoan]["MAN CHOI HIEN TAI"]:
            accs[tai_khoan]["MAN CHOI HIEN TAI"] += 1
        
        # Luôn cập nhật vị trí mới
        accs[tai_khoan]["VI TRI"] = vi_tri_moi
        save_acc(accs)

class ONhap:
    def __init__(self, x, y, w, h, text_goi_y=""):
        self.hinh = pygame.Rect(x, y, w, h)
        self.noi_dung = ""
        self.duoc_chon = False
        self.text_goi_y = text_goi_y 

    def xu_ly(self, event): # NHẬP NỘI DUNG (XÓA NẾU BẤM BACKSPACE)
        if event.type == pygame.MOUSEBUTTONDOWN: 
            self.duoc_chon = self.hinh.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.duoc_chon:
            if event.key == pygame.K_BACKSPACE: 
                self.noi_dung = self.noi_dung[:-1]
            else:
                if len(self.noi_dung) < 20: 
                    self.noi_dung += event.unicode

    def ve(self, man_hinh): # VIẾT CHỮ VÀ VẼ Ô NHỎ
        hien_thi = ""
        mau_sac = DEN
        
        if self.duoc_chon:
            pygame.draw.rect(man_hinh, TRANG, self.hinh, 2)

        if self.noi_dung == "" and not self.duoc_chon:
            hien_thi = self.text_goi_y
            mau_sac = (80, 80, 80) 
        else:
            hien_thi = self.noi_dung
            mau_sac = DEN 

        chu = font_nho.render(hien_thi, True, mau_sac)
        text_rect = chu.get_rect(center=self.hinh.center)
        man_hinh.blit(chu, text_rect)
    
    def veto(self, man_hinh): # VIẾT CHỮ VÀ VẼ Ô LỚN
        pygame.draw.rect(man_hinh, (212, 175, 118), self.hinh)
        hien_thi = self.noi_dung if self.noi_dung != "" else self.text_goi_y
        mau_sac = DEN if self.noi_dung != "" else (120, 120, 120)
        chu = font_to.render(hien_thi, True, mau_sac)
        text_rect = chu.get_rect(center=self.hinh.center)
        man_hinh.blit(chu, text_rect)

#TỌA ĐỘ Ô NHẬP SIZE
o_nhap_size = ONhap(390, 260, 420, 80,"SIZE")
nut_xac_nhan_size = pygame.Rect(400, 400, 400, 80)
# TỌA ĐỘ SIZE BAR
SIDEBAR_W = 260
HEADER_H = 120 
screen_dai = 600 
screen_rong = 1200
MAU_NEN_GAME = (70, 50, 35)

# LOAD ASSETS MỚI (NẰM TRONG THƯ MỤC ASSETS)
v_raw = pygame.image.load("assets/victory.jpg")
vic_img = pygame.transform.scale(v_raw, (screen_rong, screen_dai))
d_raw = pygame.image.load("assets/defeat.jpg")
def_img = pygame.transform.scale(d_raw, (screen_rong, screen_dai))
img_raw = pygame.image.load("assets/sidebar.jpg")
sidebar_img = pygame.transform.scale(img_raw, (SIDEBAR_W, screen_dai))
h_raw = pygame.image.load("assets/header.jpg")
header_w = screen_rong - SIDEBAR_W
header_img = pygame.transform.scale(h_raw, (header_w, HEADER_H))

# ẢNH NỀN 
login_img = None; level_img = None; dokho_img = None; menu_img = None

# LOAD MENU IMAGE
if os.path.exists("assets/man_hinh_bat_dau.png"):
    menu_img = pygame.transform.scale(pygame.image.load("assets/man_hinh_bat_dau.png"), (screen_rong, screen_dai))

# LOAD GUIDE IMAGE 
guide_img = None
if os.path.exists("assets/guide.jpg"):
    guide_img = pygame.transform.scale(pygame.image.load("assets/guide.jpg"), (screen_rong, screen_dai))
elif os.path.exists("assets/guide.png"):
    guide_img = pygame.transform.scale(pygame.image.load("assets/guide.png"), (screen_rong, screen_dai))

# LOAD RANDOM IMAGE
random_img = None
if os.path.exists("assets/random.jpg"):
    random_img = pygame.transform.scale(pygame.image.load("assets/random.jpg"), (screen_rong, screen_dai))
elif os.path.exists("assets/random.png"):
    random_img = pygame.transform.scale(pygame.image.load("assets/random.png"), (screen_rong, screen_dai))

# LOAD LOGIN
if os.path.exists("assets/login.png"):
    login_img = pygame.transform.scale(pygame.image.load("assets/login.png"), (screen_rong, screen_dai))
elif os.path.exists("assets/login.jpg"):
    login_img = pygame.transform.scale(pygame.image.load("assets/login.jpg"), (screen_rong, screen_dai))

# LOAD LEVEL
if os.path.exists("assets/level.png"):
    level_img = pygame.transform.scale(pygame.image.load("assets/level.png"), (screen_rong, screen_dai))
elif os.path.exists("assets/level.jpg"):
    level_img = pygame.transform.scale(pygame.image.load("assets/level.jpg"), (screen_rong, screen_dai))

# LOAD ĐỘ KHÓ
if os.path.exists("assets/dokho.png"):
    dokho_img = pygame.transform.scale(pygame.image.load("assets/dokho.png"), (screen_rong, screen_dai))
elif os.path.exists("assets/dokho.jpg"):
    dokho_img = pygame.transform.scale(pygame.image.load("assets/dokho.jpg"), (screen_rong, screen_dai))

# LOAD ẢNH KEY VÀ BOM - LOAD TRỰC TIẾP
key_img_raw = pygame.image.load("assets/key.png")
bom_img_raw = pygame.image.load("assets/bom.png")

# LOAD ẢNH KHÓA
lock_img = pygame.transform.scale(pygame.image.load("assets/lock.png"), (80, 65))


stair_imgs = {}
stair_imgs[0] = pygame.image.load("assets/stairs_up.png")
stair_imgs[1] = pygame.image.load("assets/stairs_right.png")
stair_imgs[2] = pygame.image.load("assets/stairs_down.png")
stair_imgs[3] = pygame.image.load("assets/stairs_left.png")

btn_undo_rect  = pygame.Rect(35, 165, 190, 52)
btn_reset_rect = pygame.Rect(35, 220, 190, 52) 
btn_opt_rect   = pygame.Rect(35, 285, 190, 52) 
btn_quit_rect  = pygame.Rect(35, 340, 190, 52)
btn_vd_menu_rect = pygame.Rect(300, 400, 250, 150)
btn_vd_action_rect = pygame.Rect(650, 400, 250, 150)
size_chon = 6 

o_tai_khoan = ONhap(400, 345, 400, 50, "USERNAME") 
o_mat_khau = ONhap(400, 420, 400, 50, "PASSWORD")
nut_dang_nhap = pygame.Rect(350, 510, 200, 70)
nut_dang_ky = pygame.Rect(650, 510, 200, 70)

run = 1
huy = 1
menu_start = 1
dang_dang_nhap = True
thong_bao_loi = ""
do_kho = ""

#=====CODE KHI GAME CHẠY====#
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = 0

        if dang_dang_nhap: # CODE DÙNG ĐỂ ĐĂNG NHẬP ĐĂNG KÍ
            o_tai_khoan.xu_ly(event); o_mat_khau.xu_ly(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if nut_dang_nhap.collidepoint(event.pos):
                    accs = load_acc()
                    tk, mk = o_tai_khoan.noi_dung, o_mat_khau.noi_dung
                    if tk in accs and accs[tk]["MAT KHAU"] == mk:
                        dang_dang_nhap = False; thong_bao_loi = ""
                    else: thong_bao_loi = "SAI TAI KHOAN HOAC MAT KHAU"
                elif nut_dang_ky.collidepoint(event.pos):
                    tk, mk = o_tai_khoan.noi_dung, o_mat_khau.noi_dung
                    thanh_cong, thong_bao = create_acc(tk, mk)
                    thong_bao_loi = thong_bao

        elif menu_start == 1: 
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: # NÚT ESC DÙNG ĐỂ LÙI 1 THAO TÁC
                if huy == 3: 
                    huy = 0  
                elif huy == 4:
                    huy = 0  
                elif huy == 0:
                    huy = 1  
                elif huy == 2:
                    huy = 1  
                else:        
                    run = 0  
            if huy == 4: o_nhap_size.xu_ly(event) # Ô NHẬP SIZE
            if event.type == pygame.MOUSEBUTTONDOWN:
                if huy == 1: # THAO TÁC NẾU BẤM VÀO CHƠI HOẶC HƯỚNG DẪN
                    if choi_btn.collidepoint(event.pos): huy = 0
                    elif hd_btn.collidepoint(event.pos): huy = 2
                elif huy == 0: # Ô CHỌN LEVEL
                    accs = load_acc()
                    user_data = accs.get(o_tai_khoan.noi_dung, {"MAN CHOI HIEN TAI": 1, "VI TRI": [0,0]})
                    man_hien_tai = user_data["MAN CHOI HIEN TAI"]
                    for i, rect in enumerate(level_rects):
                        if rect.collidepoint(event.pos):
                            level_bam = i + 1
                            
                            if level_bam <= man_hien_tai:
                                level_chon = level_bam
                                
                                if level_bam == man_hien_tai:
                                    player_pos = user_data.get("VI TRI", [0, 0])
                                else:
                                    player_pos = [0, 0]
                                huy = 3
                            else:
                                thong_bao_loi = "BAN CHUA MO KHOA MAN NAY!"
                    if random_btn.collidepoint(event.pos): level_chon = "RANDOM"; thong_bao_loi = ""; huy = 4 
                elif huy == 3: # Ô ĐỘ KHÓ
                    if de_btn.collidepoint(event.pos): globals()['do_kho'] = "DE"
                    if tb_btn.collidepoint(event.pos): globals()['do_kho'] = "TRUNG BINH"
                    if kho_btn.collidepoint(event.pos): globals()['do_kho'] = "KHO"
                    if de_btn.collidepoint(event.pos) or tb_btn.collidepoint(event.pos) or kho_btn.collidepoint(event.pos):
                        khoi_tao_game(); menu_start = 0
                elif huy == 4: # Ô NHẬP SIZE
                    if nut_xac_nhan_size.collidepoint(event.pos):
                        if o_nhap_size.noi_dung.isdigit():
                            val = int(o_nhap_size.noi_dung)
                            if 4 <= val <= 50: size_chon = val; huy = 3; thong_bao_loi = ""
                            else: thong_bao_loi = "SIZE TU 4 DEN 50"
                        else: thong_bao_loi = "VUI LONG NHAP SO"
        
        elif menu_start == 2: # THUA
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_vd_menu_rect.collidepoint(event.pos): khoi_tao_game(); menu_start = 0
                if btn_vd_action_rect.collidepoint(event.pos): menu_start = 1; huy = 1
                mx, my = pygame.mouse.get_pos()
                if not def_img:
                     if ((mx - 400)**2 + (my - 400)**2)**0.5 <= 60: khoi_tao_game(); menu_start = 0
                     if ((mx - 800)**2 + (my - 400)**2)**0.5 <= 60: menu_start = 1; huy = 1
        
        elif menu_start == 3: # THẮNG 
            if event.type == pygame.MOUSEBUTTONDOWN:
                update_progress(o_tai_khoan.noi_dung, level_chon, [0, 0])
                if btn_vd_menu_rect.collidepoint(event.pos): menu_start = 1; huy = 1
                if btn_vd_action_rect.collidepoint(event.pos): chuyen_man_ke(); menu_start = 0
                mx, my = pygame.mouse.get_pos()
                if not vic_img:
                     if ((mx - 400)**2 + (my - 400)**2)**0.5 <= 60: menu_start = 1; huy = 1
                     if ((mx - 800)**2 + (my - 400)**2)**0.5 <= 60: chuyen_man_ke(); menu_start = 0

        # XỬ LÍ GAME PLAY
        elif menu_start == 0:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                menu_start = 1
                huy = 3
            if 'a' in globals() and 'player_pos' in globals():
                player_move(event, player_pos, a)
                accs = load_acc()
                if o_tai_khoan.noi_dung in accs:
                    accs[o_tai_khoan.noi_dung]["VI TRI"] = player_pos
                    save_acc(accs)
                if 'menu_start' in globals(): menu_start = globals()['menu_start']

            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_undo_rect.collidepoint(event.pos):
                    if 'undo_stack' in globals() and len(globals()['undo_stack']) > 0:
                        prev_state = globals()['undo_stack'].pop()
                        player_pos[:] = prev_state['p']
                        globals()['mummy_pos'] = [m[:] for m in prev_state['m']]
                        globals()['turn_step'] = 0 
                        if 'p_state' in globals(): 
                            globals()['p_state']['pixel_x'] = None 
                            globals()['p_state']['is_moving'] = False
                        if 'm_states' in globals(): globals()['m_states'] = {}
                elif btn_reset_rect.collidepoint(event.pos): khoi_tao_game()
                elif btn_opt_rect.collidepoint(event.pos):
                    if 'AM_THANH_BAT' in globals(): globals()['AM_THANH_BAT'] = not globals()['AM_THANH_BAT']
                elif btn_quit_rect.collidepoint(event.pos): menu_start = 1; huy = 1
    
    # 2. XỬ LÝ LOGIC GAME
    if menu_start == 0:
        if turn_step == 1:
            if 'p_state' in globals() and not globals()['p_state']['is_moving']:
                turn_step = 2
        elif turn_step == 2:
            if 'mummy_pos' in globals() and 'do_kho' in globals():
                dk = globals()['do_kho']; 
                if dk == "": dk = "DE"
                mummy_move(globals()['mummy_pos'], player_pos, a, dk)
            turn_step = 3
        elif turn_step == 3:
            any_moving = False
            if 'm_states' in globals():
                for s in globals()['m_states'].values():
                        if s['is_moving']: any_moving = True
            if not any_moving: turn_step = 4
        elif turn_step == 4:
            if 'mummy_pos' in globals() and 'do_kho' in globals():
                dk = globals()['do_kho']; 
                if dk == "": dk = "DE"
                mummy_move(globals()['mummy_pos'], player_pos, a, dk)
            turn_step = 5
        elif turn_step == 5:
            any_moving = False
            if 'm_states' in globals():
                for s in globals()['m_states'].values():
                        if s['is_moving']: any_moving = True
            if not any_moving: turn_step = 0

        # --- XỬ LÝ LOGIC GAME ---
        if 'mummy_pos' in globals() and 'player_pos' in globals():
            
            tap_hop_mummy = set(tuple(m) for m in globals()['mummy_pos'])
            
            so_luong_state = len(globals()['m_states']) if 'm_states' in globals() else 0
            
            if len(tap_hop_mummy) != so_luong_state:
                 globals()['m_states'] = {}

            # KIỂM TRA THUA
            for m in globals()['mummy_pos']:
                if m[0] == player_pos[0] and m[1] == player_pos[1]:
                    menu_start = 2 
                    globals()['menu_start'] = 2
                    break

    # 3. VẼ GIAO DIỆN
    screen.fill(DEN)
     
    if dang_dang_nhap: # ĐĂNG NHẬP
        if login_img: screen.blit(login_img, (0, 0))
        o_tai_khoan.ve(screen); o_mat_khau.ve(screen)
        
        if thong_bao_loi:
            mau_chu = XANH_LA if "THANH CONG" in thong_bao_loi else DO
            loi = font_nho.render(thong_bao_loi, True, mau_chu)
            screen.blit(loi, (450, 560))

    elif menu_start == 1:
        if huy == 1: # PHẦN MENU
            if menu_img: screen.blit(menu_img, (0,0))
        elif huy == 2: # PHẦN HƯỚNG DẪN
            if guide_img: screen.blit(guide_img, (0, 0))
        elif huy == 0: # CHỌN LEVEL
            if level_img: screen.blit(level_img, (0, 0))
            user_data = load_acc().get(o_tai_khoan.noi_dung, {})
            man_hien_tai = user_data.get("MAN CHOI HIEN TAI", 1)
            for i, rect in enumerate(level_rects):
                level_so = i + 1
                if level_so > man_hien_tai:
                    if lock_img:
                        lock_rect = lock_img.get_rect(center=rect.center)
                        screen.blit(lock_img, lock_rect)
            if thong_bao_loi:
                loi = font_nho.render(thong_bao_loi, True, DO)
                screen.blit(loi, (450, 450))
        elif huy == 3: # CHỌN ĐỘ KHÓ
            if dokho_img: screen.blit(dokho_img, (0, 0))
        elif huy == 4: # CHỌN MÊ CUNG RAMDOM
            if random_img: screen.blit(random_img, (0, 0))
            o_nhap_size.veto(screen)
            center_x, center_y = 600, 295
            if thong_bao_loi: # KHI NHẬP SAI
                loi = font_nho.render(thong_bao_loi, True, DO)
                screen.blit(loi, (450, 500))
    
    elif menu_start == 2: # THUA
        if def_img: screen.blit(def_img, (0, 0))

    elif menu_start == 3: # THẮNG
        if vic_img: screen.blit(vic_img, (0, 0))

    else:
        # VẼ TRÒ CHƠI
        if 'a' not in globals():
            if size_chon == 8: a = tao_me_cung_8()
            elif size_chon == 10: a = tao_me_cung_10()
            else: a = tao_me_cung_6()
            player_pos = [0, 0]
            mummy_pos = [[a.sz - 1, a.sz - 1]]

        if 'a' in locals() or 'a' in globals():
            screen.fill(MAU_NEN_GAME) 
            if sidebar_img: screen.blit(sidebar_img, (0, 0))
            
            HEADER_H = 120
            available_h = screen_dai - HEADER_H
            cell_size = available_h // (a.sz + 2)
            maze_pixel_w = a.sz * cell_size
            maze_pixel_h = a.sz * cell_size
            total_content_h = HEADER_H + maze_pixel_h
            offset_y_header = (screen_dai - total_content_h) // 2
            available_w = screen_rong - SIDEBAR_W
            offset_x = SIDEBAR_W + (available_w - maze_pixel_w) // 2
            offset_y_maze = offset_y_header + HEADER_H

            if 'header_img_raw' not in globals() and header_img: globals()['header_img_raw'] = pygame.image.load("assets/header.jpg")
            if 'header_img_raw' in globals():
                h_scaled = pygame.transform.scale(globals()['header_img_raw'], (maze_pixel_w, HEADER_H))
                screen.blit(h_scaled, (offset_x, offset_y_header))
            elif header_img:
                h_scaled = pygame.transform.scale(header_img, (maze_pixel_w, HEADER_H))
                screen.blit(h_scaled, (offset_x, offset_y_header))

            # VẼ CẦU THANG
            if 'stair_imgs' in globals() and a.door and 0 <= a.door[2] <= 3:
                dr, dc, d_dir = a.door
                s_img = globals()['stair_imgs'].get(d_dir)
                if s_img:
                    s_scaled = pygame.transform.scale(s_img, (cell_size, cell_size))
                    sx = offset_x + dc * cell_size
                    sy = offset_y_maze + dr * cell_size
                    if d_dir == 0: sy -= cell_size 
                    elif d_dir == 1: sx += cell_size 
                    elif d_dir == 2: sy += cell_size 
                    elif d_dir == 3: sx -= cell_size 
                    screen.blit(s_scaled, (sx, sy))

            # VẼ BÀN CỜ
            SAN_SANG = (210, 190, 140) 
            SAN_TOI = (185, 165, 120)  
            for r in range(a.sz):
                for c in range(a.sz):
                    x = offset_x + c * cell_size
                    y = offset_y_maze + r * cell_size
                    mau_nen = SAN_SANG if (r + c) % 2 == 0 else SAN_TOI
                    pygame.draw.rect(screen, mau_nen, (x, y, cell_size, cell_size))
                    val = a.matrix[r][c]
                    wall_color = NAU_DAM
                    thick = 4
                    if (val >> 0) & 1: pygame.draw.line(screen, wall_color, (x, y), (x + cell_size, y), thick)
                    if (val >> 1) & 1: pygame.draw.line(screen, wall_color, (x + cell_size, y), (x + cell_size, y + cell_size), thick)
                    if (val >> 2) & 1: pygame.draw.line(screen, wall_color, (x, y + cell_size), (x + cell_size, y + cell_size), thick)
                    if (val >> 3) & 1: pygame.draw.line(screen, wall_color, (x, y), (x, y + cell_size), thick)
            
            # VẼ ITEM (KEY/BOM)
            ve_items(screen, cell_size, offset_x, offset_y_maze)
            ve_player(screen, cell_size, offset_x, offset_y_maze, player_pos)
            ve_mummy(screen, cell_size, offset_x, offset_y_maze, mummy_pos)

    xu_ly_am_thanh(screen, dang_dang_nhap, menu_start)
    pygame.display.flip()
    clock.tick(FPS)# your code goes here