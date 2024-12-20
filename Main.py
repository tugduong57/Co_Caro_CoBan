import pygame, sys, checkWin
from pygame import QUIT, K_SPACE, K_RETURN, K_UP, K_DOWN, K_LEFT, K_RIGHT, KEYDOWN, K_a, K_s, K_d, K_w, K_r, K_p

import os
os.chdir("E:/ThisPC/Desktop/Code/Caro")

pygame.init()
GRID_SIZE = 15; nxn = 10;
banco = []; NumberToWin = 5; player = ""; AI = ""; turn = ""; pre = (); game_over = False; turn = ""; LuotAI = False
ScorePlayer = []; ScoreAI = []; ScoreTong = []; T_Tong = {}
TH = {}; T_player = {}; T_Ai = {} # Bảng tra cứu điểm; Dir lưu tọa độ các điểm có cùng Value
directions = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
Direc = {(-1, 0): 1, (-1, 1): 2, (0, 1): 3, (1, 1): 4, (1, 0): 5, (1, -1):6, (0, -1):7, (-1, -1):8}
MapPlayer = []; MapAI = [] 

def AddT(T, value, x, y):
    if value not in T:
        T[value] = []
    T[value].append((x,y))

def RemoveT(T, value, x, y):
    if value in T:
        if (x,y) in T[value]:
            T[value].remove((x, y))
    if T[value] == []:
        T.pop(value)

def Update_Pre(x, y, turn):
    global pre;
    pre = (x, y, turn)

def taoBangDanhGia(N):
    matrix = [["F"] * N for _ in range(N)]
    return matrix

def print_matrix(matrix):
    for row in matrix:
        print(" ".join(f"{value:5}" for value in row))
    print()

def Init():
    global nxn, banco, player, AI, pre, game_over, turn, LuotAI;
    global ScorePlayer, ScoreAI, ScoreTong, MapPlayer, MapAI, TH, T_player, T_Ai, T_Tong;
    game_over = False
    turn = player; LuotAI = False
    pre = (0,0,"")
    nxn = GRID_SIZE;
    banco = [ ['.']*nxn for _ in range(nxn)]
    ScorePlayer = taoBangDanhGia(nxn); ScoreAI = taoBangDanhGia(nxn); ScoreTong = taoBangDanhGia(nxn);
    player = "X"; AI = "O"
    # Ma trận Map : lưu 8 hướng của 1 ô, và điểm đánh giá của 4 đường
    MapPlayer.clear(); MapAI.clear()
    for i in range(nxn):
        MapPlayer.append( [] ); MapAI.append( [] )
        for j in range(nxn):
            MapPlayer[i].append( [0] + ["00"]*8 + ["F","F","F","F"]) # white
            MapAI[i].append( [0] + ["00"]*8 + ["F","F","F","F"]) # white
            if i == 0:
                MapPlayer[i][j][1] = "-1"; MapAI[i][j][1] = "-1"
            if j == nxn-1: 
                MapPlayer[i][j][3] = "-1"; MapAI[i][j][3] = "-1"
            if i == nxn-1:
                MapPlayer[i][j][5] = "-1"; MapAI[i][j][5] = "-1"
            if j == 0:
                MapPlayer[i][j][7] = "-1"; MapAI[i][j][7] = "-1"
    TH.clear()
    with open("H.txt", encoding="utf-8") as inp:
        for i in range(361):
            line = inp.readline().split(";"); xau = line[0]; diem = line[1]
            TH[xau] = diem
    T_player = {}; T_Ai = {}; T_Tong = {}
    for i in range(nxn):
        for j in range(nxn):
            value = ScorePlayer[i][j];
            AddT(T_player, value, i, j); AddT(T_Ai, value, i, j); AddT(T_Tong, value, i, j)  


# Set up
WINDOW_WIDTH = 800; WINDOW_HEIGHT = 800; SQUARE_SIZE = min(WINDOW_WIDTH, WINDOW_HEIGHT) // GRID_SIZE
WHITE = (255, 255, 255); BACKGROUND_COLOR = (255, 255, 255); LINE_COLOR = (0, 0, 0); X_COLOR = (0, 0, 0); O_COLOR = (0, 0, 0); Pre_COLOR = (0,0,255)

# Tạo cửa sổ
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Bàn cờ XO')
font = pygame.font.Font(None, 20)

def draw_numbers():
    # Vẽ số vào từng ô vuông
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            value1 = str(ScorePlayer[row][col])
            value2 = str(ScoreAI[row][col])
            value3 = str(ScoreTong[row][col])
            if value1 == "-1":
                continue
            text_surface1 = font.render(value1, True, (0,0,0)); text_surface2 = font.render(value2, True, (0,0,0))
            text_surface3 = font.render(value3, True, (0,0,0))
            text_x = col * SQUARE_SIZE; text_y = row * SQUARE_SIZE
            screen.blit(text_surface1, (text_x+2, text_y+2)); screen.blit(text_surface2, (text_x+2, text_y+17))
            screen.blit(text_surface3, (text_x+2, text_y+32))

# Hàm vẽ bàn cờ
def draw_board():
    screen.fill(BACKGROUND_COLOR)
    for row in range(1, GRID_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (0, row * SQUARE_SIZE) , (WINDOW_WIDTH, row * SQUARE_SIZE)  , 3); pygame.draw.line(screen, LINE_COLOR, (row * SQUARE_SIZE, 0) , (row * SQUARE_SIZE, WINDOW_HEIGHT) , 3)
    pygame.draw.line(screen, LINE_COLOR, (0, 0 * SQUARE_SIZE), (WINDOW_WIDTH, 0* SQUARE_SIZE), 5); pygame.draw.line(screen, LINE_COLOR, (0 * SQUARE_SIZE, 0), (0 * SQUARE_SIZE, WINDOW_HEIGHT), 5); pygame.draw.line(screen, LINE_COLOR, (0, GRID_SIZE * SQUARE_SIZE-2), (WINDOW_WIDTH, GRID_SIZE* SQUARE_SIZE-2), 5); pygame.draw.line(screen, LINE_COLOR, (GRID_SIZE * SQUARE_SIZE-1, 0), (GRID_SIZE * SQUARE_SIZE-1, WINDOW_HEIGHT), 5)

# Hàm vẽ X và O
def draw_XO(banco):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if banco[row][col] == 'X':
                pygame.draw.line(screen, X_COLOR, (col * SQUARE_SIZE + 20, row * SQUARE_SIZE + 20), (col * SQUARE_SIZE + SQUARE_SIZE - 20, row * SQUARE_SIZE + SQUARE_SIZE - 20), 5); pygame.draw.line(screen, X_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE - 20, row * SQUARE_SIZE + 20), (col * SQUARE_SIZE + 20, row * SQUARE_SIZE + SQUARE_SIZE - 20), 5)
            elif banco[row][col] == 'O':
                pygame.draw.circle(screen, O_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 7, 2) 
    row = pre[0]; col = pre[1]
    if pre[2] == "X":
        pygame.draw.line(screen, Pre_COLOR, (col * SQUARE_SIZE + 20, row * SQUARE_SIZE + 20), (col * SQUARE_SIZE + SQUARE_SIZE - 20, row * SQUARE_SIZE + SQUARE_SIZE - 20), 5); pygame.draw.line(screen, Pre_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE - 20, row * SQUARE_SIZE + 20), (col * SQUARE_SIZE + 20, row * SQUARE_SIZE + SQUARE_SIZE - 20), 5)
    elif pre[2] == "O":
        pygame.draw.circle(screen, Pre_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 7, 2) 

def Update_Score(turn, x, y,dx, dy):
    global player, AI, ScorePlayer, ScoreAI, ScoreTong, T_Tong, T_player, T_Ai, MapPlayer, MapAI;
    if turn == player:
        matrix = ScorePlayer; T_matrix = T_player; Map = MapPlayer
    else: # turn == AI
        matrix = ScoreAI; T_matrix = T_Ai; Map = MapAI

    if (dx, dy) in [ (1, 0), (1, -1), (0, -1), (-1, -1) ]:
        xau = Map[x][y][Direc[(dx, dy)]] + "X" + Map[x][y][Direc[(-dx, -dy)]]   
    elif (dx, dy) in [ (-1, 0),(-1, 1),  (0, 1), ( 1, 1 ) ]:
        xau = Map[x][y][Direc[(-dx, -dy)]] +  "X" + Map[x][y][Direc[(dx, dy)]]

    k = Direc[(dx, dy)]
    if k > 4:
        k -= 4
    Map[x][y][8 + k] = TH[xau]

    if turn == player:
        matrix = ScorePlayer; T_matrix = T_player;
    else: # turn == AI
        matrix = ScoreAI; T_matrix = T_Ai;

    oldScore = matrix[x][y]
    m = [Map[x][y][9],Map[x][y][10],Map[x][y][11],Map[x][y][12]]; m.sort();
    if m[0] == "A":
        e = "A"
    elif m[0] == "B" or (m[0] == "C" and m[1] == "C"):
        e = "B"
    else:
        e = m[0]

    # else:
    #     m = m[0]
    Map[x][y][0] = e
    newScore = Map[x][y][0];
    RemoveT(T_matrix, matrix[x][y], x, y); matrix[x][y] = newScore; AddT(T_matrix, matrix[x][y], x, y)
    RemoveT(T_Tong, ScoreTong[x][y], x, y);
    ScoreTong[x][y] = min(ScorePlayer[x][y], ScoreAI[x][y])
    AddT(T_Tong, ScoreTong[x][y], x, y);

def Update_Map(turn, x, y, dx, dy):
    canhke = []; global Direc;
    trang = 1; i = 1
    while True:
        new_x = x + dx*i; new_y = y + dy*i
        if 0 <= new_x < nxn and 0 <= new_y < nxn:
            giatri = banco[new_x][new_y]
            if giatri == turn:
                canhke.append('1') 
                if trang != 0:
                    trang = 0
            elif giatri == ".":
                if trang == 1: 
                    canhke.append("0")
                    trang -= 1
                elif trang == 0:
                    canhke.append("0")
                    trang -= 1
                if trang == -1:
                    break
            else:
                canhke.append('-1'); 
                break
        else:
            canhke.append("-1"); 
            break
        i += 1
    if turn == player:
        Map = MapPlayer
    else: # turn == AI
        Map = MapAI

    if (dx, dy) in [ (1, 0), (1, -1), (0, -1), (-1, -1) ]:
        Map[x][y][Direc[(dx, dy)]] = "".join(canhke[::-1])   
    elif (dx, dy) in [ (-1, 0),(-1, 1),  (0, 1), ( 1, 1 ) ]:
        Map[x][y][Direc[(dx, dy)]] = "".join(canhke)      
    Update_Score(turn,x,y,dx,dy)

def SCAN(turn, x, y):
    global directions;
    for dx, dy in directions:
        h = []; trang = 1; i = 1
        while True:
            new_x = x + dx * i; new_y = y + dy * i
            if 0 <= new_x < nxn and 0 <= new_y < nxn:
                giatri = banco[new_x][new_y]
                if giatri == turn:
                    if trang == 1:
                        trang = 0
                if giatri == ".":
                    trang -= 1;
                    Update_Map(turn, new_x, new_y, -dx, -dy)
                    if trang == -1:
                        break
                if giatri != turn and giatri != ".":
                    break
            else:
                break
            i += 1

def AI_move():
    # (x, y) = AI_move()
    global ScorePlayer, ScoreAI, T_Ai, T_player, T_Tong, banco
    print(T_Ai)
    if "A" in T_Ai:                     # Thắng "ngay" được thắng luôn
        return T_Ai["A"][0]             
    else:                               # Nếu không thắng được luôn:
        if "A" in T_player:                 # Chặn nước thắng "ngay" của player
            return T_player["A"][0]
        else:                               # Nếu đối thủ không thắng ngay được:
            if "B" in T_Ai:                     # Tạo nước thắng "ở lượt sau" được thì tạo luôn
                return T_Ai["B"][0]
            else:                               # Nếu không tạo được:
                if "B" in T_player:                 # Chặn nước thắng "ở lượt sau" của player 
                    return T_player["B"][0]
    # Trường hợp không còn "A" và "B" ở cả 2 
    # -> T_Ai và T_player còn "C" "D" "E" "F" 
    # Nước "C" "D" "E" nào là tốt nhất?? nước tạo ra A và B ??
    return T_Tong[min(T_Tong.keys())][0]

def game_loop():
    global AI, player;
    global ScorePlayer, ScoreAI, T_Ai, T_player, banco, game_over, turn, LuotAI;
    
    while True:
        draw_board(); draw_XO(banco); draw_numbers()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over and not LuotAI:
                x_mouse, y_mouse = pygame.mouse.get_pos(); row, col = y_mouse // SQUARE_SIZE, x_mouse // SQUARE_SIZE
                if event.button == 1:
                    if banco[row][col] == '.':
                        banco[row][col] = player; Update_Pre(row, col, player)
                        RemoveT(T_player, ScorePlayer[row][col], row, col); RemoveT(T_Ai, ScoreAI[row][col], row, col)
                        RemoveT(T_Tong, ScoreTong[row][col], row, col);
                        ScorePlayer[row][col] = "-1"; ScoreAI[row][col] = "-1"; ScoreTong[row][col] = "-1"
                        if checkWin.checkWin(banco, player, row+1, col+1, nxn, NumberToWin) == "Win":
                            game_over = True; 
                            break
                        SCAN(player, row, col);
                        SCAN(AI, row, col);
                        LuotAI = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    x_mouse, y_mouse = pygame.mouse.get_pos(); x, y = y_mouse // SQUARE_SIZE, x_mouse // SQUARE_SIZE
                    print(MapPlayer[x][y], flush=True)
                    for (dx, dy) in directions: 
                    #(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)
                        if (dx, dy) in [ (1, 0), (1, -1), (0, -1), (-1, -1) ]:
                            xau = MapPlayer[x][y][Direc[(dx, dy)]] + "X" + MapPlayer[x][y][Direc[(-dx, -dy)]]   
                        elif (dx, dy) in [ (-1, 0),(-1, 1),  (0, 1), ( 1, 1 ) ]:
                            xau = MapPlayer[x][y][Direc[(-dx, -dy)]] +  "X" + MapPlayer[x][y][Direc[(dx, dy)]]
                        print(xau, flush=True)
                    print()
            if event.type == KEYDOWN and LuotAI:
                LuotAI = False;
                if (event.key == K_SPACE):
                    #(x, y) = T_Tong[min(T_Tong.keys())][0] 
                    (x, y) = AI_move()
                    banco[x][y] = AI; Update_Pre(x, y, AI)
                    draw_board();
                    RemoveT(T_player, ScorePlayer[x][y], x, y); RemoveT(T_Ai, ScoreAI[x][y], x, y)
                    RemoveT(T_Tong, ScoreTong[x][y], x, y)
                    ScorePlayer[x][y] = "-1"; ScoreAI[x][y] = "-1"; ScoreTong[x][y] = "-1"
                    if checkWin.checkWin(banco, AI, x+1, y+1, nxn, NumberToWin) == "Win":
                        game_over = True; turn = AI;
                        break
                    SCAN(player, x, y);
                    SCAN(AI, x, y);
            if event.type == KEYDOWN:
                if (event.key == K_r):
                    Init()

        if game_over:
            font = pygame.font.Font(None, 74)
            winner_text = font.render(f'{turn} wins!', True, (0, 0, 0))
            screen.blit(winner_text, (WINDOW_WIDTH // 2 - winner_text.get_width() // 2, WINDOW_HEIGHT // 2 - winner_text.get_height() // 2))
        pygame.display.flip()

Init();
game_loop()