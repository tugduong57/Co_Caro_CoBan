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

def Update_Score(banco, Map, turn, x, y,dx, dy, ScorePlayer, ScoreAI, ScoreTong, T_player, T_Ai,  T_Tong):
    if turn == player:
        matrix = ScorePlayer; T_matrix = T_player
    else: # turn == AI
        matrix = ScoreAI; T_matrix = T_Ai

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
    if m[0] == m[1] == "C":
        m[0] = "B"
    elif m[0] == m[1] == "D":
        m[0] = "C"

    # else:
    #     m = m[0]
    Map[x][y][0] = "".join(m)
    newScore = Map[x][y][0];
    RemoveT(T_matrix, matrix[x][y], x, y); matrix[x][y] = newScore; AddT(T_matrix, matrix[x][y], x, y)
    RemoveT(T_Tong, ScoreTong[x][y], x, y);
    # ScoreTong[x][y] = min(ScorePlayer[x][y], ScoreAI[x][y])
    tong = ScorePlayer[x][y] + ScoreAI[x][y]; tong = list(tong); tong.sort()
    ScoreTong[x][y] = "".join(tong[:4])
    AddT(T_Tong, ScoreTong[x][y], x, y);

def Update_Map(banco, Map, turn, x, y, dx, dy, ScorePlayer, ScoreAI, ScoreTong, T_player, T_Ai,  T_Tong):
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

    if (dx, dy) in [ (1, 0), (1, -1), (0, -1), (-1, -1) ]:
        Map[x][y][Direc[(dx, dy)]] = "".join(canhke[::-1])   
    elif (dx, dy) in [ (-1, 0),(-1, 1),  (0, 1), ( 1, 1 ) ]:
        Map[x][y][Direc[(dx, dy)]] = "".join(canhke)      
    Update_Score(banco, Map, turn,x,y,dx,dy, ScorePlayer, ScoreAI, ScoreTong, T_player, T_Ai,  T_Tong)

def SCAN(banco, Map, turn, x, y, ScorePlayer, ScoreAI, ScoreTong, T_player, T_Ai,  T_Tong):
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
                    Update_Map(banco, Map, turn, new_x, new_y, -dx, -dy, ScorePlayer, ScoreAI, ScoreTong, T_player, T_Ai,  T_Tong)
                    if trang == -1:
                        break
                if giatri != turn and giatri != ".":
                    break
            else:
                break
            i += 1

def UuTien_move(T_Ai, T_player):
    c = ""; d = ""
    for a in T_Ai:
        if a[0] == "A":        # Thắng "ngay" được THÌ thắng luôn
            return T_Ai[a][0] 
        if a[0] == "B":
            c = a     
    # Nếu không thắng được luôn:        
    for b in T_player:                 
        if b[0] == "A":        # Chặn nước thắng "ngay" của player             
            return T_player[b][0]
    # Nếu đối thủ không thắng ngay được: 
    if c != "":                # Tạo nước thắng "ở lượt sau" được thì tạo luôn
        return T_Ai[c][0]
    # # Nếu không tạo được:                     
    # if d != "":                # Chặn nước thắng "ở lượt sau" của player 
    #     return T_player[d][0]
    return (-1, -1)

def minimax(Board, isAI, depth, Score_Player, Score_AI, Score_Tong, Tplayer, TAi, TTong, Map_Player, Map_AI, x, y):
    if depth == 0:
        return 0

    if isAI:
        N_o = 5
        list_Best = []
        T = list(TTong.keys())
        T.sort()
        for i in T:
            if i[0] == "A" or i[0] == "B":
                list_Best = TTong[i]
                break
            list_Best += TTong[i]
            if len(list_Best) > N_o:
                break
        list_Best = list_Best[:N_o]

        maxVal = float('-inf');
        for (x, y) in list_Best:
            Board[x][y] = AI;
            if checkWin.checkWin(Board, AI, x+1, y+1, nxn, NumberToWin) == "Win":
                Val = 1000000
                Board[x][y] = "."
                maxVal = max(Val, maxVal)
                continue

            Board1 = Board.copy();  
            Score_Player1 = copy.deepcopy(Score_Player); Score_AI1 = copy.deepcopy(Score_AI); Score_Tong1 = copy.deepcopy(Score_Tong)
            Tplayer1 = copy.deepcopy(Tplayer); TAi1 = copy.deepcopy(TAi); TTong1 = copy.deepcopy(TTong); 
            Map_Player1 = copy.deepcopy(Map_Player); Map_AI1 = copy.deepcopy(Map_AI);
            
            RemoveT(Tplayer1, Score_Player1[x][y], x, y); RemoveT(TAi1, Score_AI1[x][y], x, y)
            RemoveT(TTong1, Score_Tong1[x][y], x, y)

            SCAN(Board1, Map_Player1, player, x, y, Score_Player1, Score_AI1, Score_Tong1, Tplayer1, TAi1,  TTong1);
            SCAN(Board1, Map_AI1, AI, x, y, Score_Player1, Score_AI1, Score_Tong1, Tplayer1, TAi1,  TTong1);
            
            Val = minimax(Board1, False, depth-1, Score_Player1, Score_AI1, Score_Tong1, Tplayer1, TAi1, TTong1, Map_Player1, Map_AI1, x, y)

            Board[x][y] = "."

            maxVal = max(Val, maxVal)

        return maxVal

    else:
        N_o = 5
        list_Best = []
        T = list(TTong.keys())
        T.sort()
        for i in T:
            if i[0] == "A" or i[0] == "B":
                list_Best = TTong[i]
                break
            list_Best += TTong[i]
            if len(list_Best) > N_o:
                break
        list_Best = list_Best[:N_o]
        minVal = float('inf');
        for (x, y) in list_Best:
            Board[x][y] = player;
            if checkWin.checkWin(Board, player, x+1, y+1, nxn, NumberToWin) == "Win":
                Val = -1000000
                Board[x][y] = "."
                minVal = min(Val, minVal)
                continue
                    
            Board1 = Board.copy();  
            Score_Player1 = copy.deepcopy(Score_Player); Score_AI1 = copy.deepcopy(Score_AI); Score_Tong1 = copy.deepcopy(Score_Tong)
            Tplayer1 = copy.deepcopy(Tplayer); TAi1 = copy.deepcopy(TAi); TTong1 = copy.deepcopy(TTong); 
            Map_Player1 = copy.deepcopy(Map_Player); Map_AI1 = copy.deepcopy(Map_AI);
            
            RemoveT(Tplayer1, Score_Player1[x][y], x, y); RemoveT(TAi1, Score_AI1[x][y], x, y)
            RemoveT(TTong1, Score_Tong1[x][y], x, y)

            SCAN(Board1, Map_Player1, player, x, y, Score_Player1, Score_AI1, Score_Tong1, Tplayer1, TAi1,  TTong1);
            SCAN(Board1, Map_AI1, AI, x, y, Score_Player1, Score_AI1, Score_Tong1, Tplayer1, TAi1,  TTong1);
            
            Val = minimax(Board1, True, depth-1, Score_Player1, Score_AI1, Score_Tong1, Tplayer1, TAi1, TTong1, Map_Player1, Map_AI1, x, y)

            Board[x][y] = "."

            minVal = min(Val, minVal)

        return minVal


import copy

def AI_move():
    (x, y) = UuTien_move(T_Ai, T_player)
    if (x, y) != (-1, -1):
        return (x, y)

    # Score_Player, Score_AI, Score_Tong, Tplayer, TAi, T_Tong, Map_Player, Map_AI

    N_o = 5
    list_Best = []
    T = list(T_Tong.keys())
    T.sort()
    for i in T:
        if i[0] == "B":
            list_Best = T_Tong[i]
            break
        list_Best += T_Tong[i]
        if len(list_Best) > N_o:
            break
    list_Best = list_Best[:N_o]
    bestVal = float('-inf'); 
    bestRow = -1; bestCol = -1
    for (x, y) in list_Best:
        banco[x][y] = AI;

        Board = banco.copy(); 
        Score_Player = copy.deepcopy(ScorePlayer); Score_AI = copy.deepcopy(ScoreAI); Score_Tong = copy.deepcopy(ScoreTong)
        # Score_Player = ScorePlayer.copy(); Score_AI = ScoreAI.copy(); Score_Tong = ScoreTong.copy()
        Tplayer = copy.deepcopy(T_player); TAi = copy.deepcopy(T_Ai); TTong = copy.deepcopy(T_Tong); 
        Map_Player = copy.deepcopy(MapPlayer); Map_AI = copy.deepcopy(MapAI);
        
        RemoveT(Tplayer, Score_Player[x][y], x, y); RemoveT(TAi, Score_AI[x][y], x, y)
        RemoveT(TTong, Score_Tong[x][y], x, y)

        SCAN(Board, Map_Player, player, x, y, Score_Player, Score_AI, Score_Tong, Tplayer, TAi,  TTong);
        SCAN(Board, Map_AI, AI, x, y, Score_Player, Score_AI, Score_Tong, Tplayer, TAi,  TTong);
        
        moveVal = minimax(Board, False, 2, Score_Player, Score_AI, Score_Tong, Tplayer, TAi, TTong, Map_Player, Map_AI, x, y)
        print(x, y, moveVal, "####################################")
        banco[x][y] = "."

        if moveVal > bestVal:
            bestRow = x; bestCol = y 
            bestVal = moveVal

    return (bestRow, bestCol)


def game_loop():
    global AI, player;
    global ScorePlayer, ScoreAI, ScoreTong, T_Ai, T_player, T_Tong, banco, game_over, turn, LuotAI;
    global MapPlayer, MapAI;
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
                        SCAN(banco, MapPlayer, player, row, col, ScorePlayer, ScoreAI, ScoreTong, T_player, T_Ai,  T_Tong);
                        SCAN(banco, MapAI, AI, row, col, ScorePlayer, ScoreAI, ScoreTong, T_player, T_Ai,  T_Tong);
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
            if LuotAI:
                draw_board(); draw_XO(banco); draw_numbers()
                # if (event.key == K_SPACE):
                (x, y) = AI_move()
                banco[x][y] = AI; Update_Pre(x, y, AI)
                # draw_board();
                RemoveT(T_player, ScorePlayer[x][y], x, y); RemoveT(T_Ai, ScoreAI[x][y], x, y)
                RemoveT(T_Tong, ScoreTong[x][y], x, y)
                ScorePlayer[x][y] = "-1"; ScoreAI[x][y] = "-1"; ScoreTong[x][y] = "-1"
                if checkWin.checkWin(banco, AI, x+1, y+1, nxn, NumberToWin) == "Win":
                    game_over = True; turn = AI;
                    break
                SCAN(banco, MapPlayer, player, x, y, ScorePlayer, ScoreAI, ScoreTong, T_player, T_Ai,  T_Tong);
                SCAN(banco, MapAI, AI, x, y, ScorePlayer, ScoreAI, ScoreTong, T_player, T_Ai,  T_Tong);
                
                LuotAI = False;

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