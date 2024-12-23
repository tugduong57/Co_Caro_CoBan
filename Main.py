import pygame, sys
from pygame import QUIT, K_SPACE, K_RETURN, K_UP, K_DOWN, K_LEFT, K_RIGHT, KEYDOWN, K_a, K_s, K_d, K_w, K_r, K_p
import copy
import random
pygame.init()

# --------------------------------------------------------------------------
#               Phần khởi tạo 
GRID_SIZE = 15; nxn = 15; max_depth = 3
banco = []; NumberToWin = 5; 
player = ""; AI = ""; turn = ""; pre = (); game_over = False; LuotAI = False
# Bảng tra cứu điểm
TH = {};  
# Bảng lưu 8 hướng của 1 ô trống -> phối hợp để tra cứu điểm TH
MapPlayer = []; MapAI = [] 
# Dir lưu tọa độ các điểm có cùng Value
T_player = {}; T_Ai = {}; T_Tong = {}
# Bảng lưu "Điểm đánh giá" 4 "chiều" của 1 ô trống
ScorePlayer = []; ScoreAI = []; ScoreTong = [];

directions = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
Direc = {(-1, 0): 1, (-1, 1): 2, (0, 1): 3, (1, 1): 4, (1, 0): 5, (1, -1):6, (0, -1):7, (-1, -1):8}

def AddT(T: dict, value: str, x: int, y: int) -> None:
    if value not in T:
        T[value] = []
    T[value].append((x,y))

def RemoveT(T: dict, value: str, x: int, y: int) -> None:
    if value in T:
        if (x,y) in T[value]:
            T[value].remove((x, y))
        if T[value] == []:
            T.pop(value)

def taoBangDanhGia(N: int) -> list:
    matrix = [["F"] * N for _ in range(N)]
    return matrix

def Init() -> None: 
    '''
        Hàm khởi tạo giá trị ban đầu của tất cả Biến toàn cục
        Được sử dụng ghi chương trình chạy lần đầu tiên
        Và khi người chơi muốn reset bàn cờ
    
    '''

    global banco;
    global player, AI, turn,  pre, game_over, LuotAI;
    global TH, MapPlayer, MapAI, T_player, T_Ai, T_Tong, ScorePlayer, ScoreAI, ScoreTong;

    banco = [ ['.']*nxn for _ in range(nxn)]
    player = "X"; AI = "O"; turn = player; pre = (0,0,"")
    game_over = False; LuotAI = False
    
    TH.clear()
    with open("H.txt", encoding="utf-8") as inp:
        for i in range(361):
            line = inp.readline().split(";"); xau = line[0]; diem = line[1]
            TH[xau] = diem 

    MapPlayer.clear(); MapAI.clear()
    for i in range(nxn):
        MapPlayer.append( [] ); MapAI.append( [] )
        for j in range(nxn):
            MapPlayer[i].append( [0] + ["00"]*8 + ["F","F","F","F"]) 
            MapAI[i].append( [0] + ["00"]*8 + ["F","F","F","F"]) 
            if i == 0:
                MapPlayer[i][j][1] = "-1"; MapAI[i][j][1] = "-1"
            if j == nxn-1: 
                MapPlayer[i][j][3] = "-1"; MapAI[i][j][3] = "-1"
            if i == nxn-1:
                MapPlayer[i][j][5] = "-1"; MapAI[i][j][5] = "-1"
            if j == 0:
                MapPlayer[i][j][7] = "-1"; MapAI[i][j][7] = "-1"

    ScorePlayer = taoBangDanhGia(nxn); ScoreAI = taoBangDanhGia(nxn); ScoreTong = taoBangDanhGia(nxn);
    T_player = {}; T_Ai = {}; T_Tong = {}
    for i in range(nxn):
        for j in range(nxn):
            value = ScorePlayer[i][j];
            AddT(T_player, value, i, j); AddT(T_Ai, value, i, j); AddT(T_Tong, value, i, j)  

# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
#               Phần giao diện 
# Set up
WINDOW_WIDTH = 760; WINDOW_HEIGHT = 760; 
SQUARE_SIZE = WINDOW_WIDTH // GRID_SIZE
WINDOW_WIDTH = WINDOW_WIDTH - WINDOW_WIDTH%SQUARE_SIZE
WINDOW_HEIGHT = WINDOW_WIDTH
WHITE = (255, 255, 255); BACKGROUND_COLOR = (255, 255, 255); LINE_COLOR = (0, 0, 0); 
X_COLOR = (0, 0, 0); O_COLOR = (0, 0, 0); Pre_COLOR = (0,0,255)

# Tạo cửa sổ
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('AI-Caro')
font = pygame.font.Font(None, 20)

# Lưu tọa độ nước cờ vừa đánh 
def Update_Pre(x: int, y: int, turn: str) -> None:
    global pre;
    pre = (x, y, turn)

# Hàm vẽ bàn cờ
def draw_board() -> None:
    screen.fill(BACKGROUND_COLOR)
    for row in range(1, GRID_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (0, row * SQUARE_SIZE) , (WINDOW_WIDTH, row * SQUARE_SIZE)  , 3); pygame.draw.line(screen, LINE_COLOR, (row * SQUARE_SIZE, 0) , (row * SQUARE_SIZE, WINDOW_HEIGHT) , 3)
    pygame.draw.line(screen, LINE_COLOR, (0, 0 * SQUARE_SIZE), (WINDOW_WIDTH, 0* SQUARE_SIZE), 5); pygame.draw.line(screen, LINE_COLOR, (0 * SQUARE_SIZE, 0), (0 * SQUARE_SIZE, WINDOW_HEIGHT), 5); pygame.draw.line(screen, LINE_COLOR, (0, GRID_SIZE * SQUARE_SIZE-2), (WINDOW_WIDTH, GRID_SIZE* SQUARE_SIZE-2), 5); pygame.draw.line(screen, LINE_COLOR, (GRID_SIZE * SQUARE_SIZE-1, 0), (GRID_SIZE * SQUARE_SIZE-1, WINDOW_HEIGHT), 5)

# Hàm vẽ X và O
X_cm = SQUARE_SIZE // 5; O_cm = SQUARE_SIZE//7
def draw_XO(banco: list) -> None:
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if banco[row][col] == 'X':
                pygame.draw.line(screen, X_COLOR, (col * SQUARE_SIZE + X_cm, row * SQUARE_SIZE + X_cm), (col * SQUARE_SIZE + SQUARE_SIZE - X_cm, row * SQUARE_SIZE + SQUARE_SIZE - X_cm), 5); 
                pygame.draw.line(screen, X_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE - X_cm, row * SQUARE_SIZE + X_cm), (col * SQUARE_SIZE + X_cm, row * SQUARE_SIZE + SQUARE_SIZE - X_cm), 5)
            elif banco[row][col] == 'O':
                pygame.draw.circle(screen, O_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - O_cm, 2) 
    row = pre[0]; col = pre[1]
    if pre[2] == "X":
        pygame.draw.line(screen, Pre_COLOR, (col * SQUARE_SIZE + X_cm, row * SQUARE_SIZE + X_cm), (col * SQUARE_SIZE + SQUARE_SIZE - X_cm, row * SQUARE_SIZE + SQUARE_SIZE - X_cm), 5); 
        pygame.draw.line(screen, Pre_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE - X_cm, row * SQUARE_SIZE + X_cm), (col * SQUARE_SIZE + X_cm, row * SQUARE_SIZE + SQUARE_SIZE - X_cm), 5)
    elif pre[2] == "O":
        pygame.draw.circle(screen, Pre_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - O_cm, 2) 

def draw_XY(turn: str, row: int, col: int) -> None:
    XY_COLOR = (255, 0, 0)
    if turn == "X":
        pygame.draw.line(screen, XY_COLOR, (col * SQUARE_SIZE + X_cm, row * SQUARE_SIZE + X_cm), (col * SQUARE_SIZE + SQUARE_SIZE - X_cm, row * SQUARE_SIZE + SQUARE_SIZE - X_cm), 5); 
        pygame.draw.line(screen, XY_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE - X_cm, row * SQUARE_SIZE + X_cm), (col * SQUARE_SIZE + X_cm, row * SQUARE_SIZE + SQUARE_SIZE - X_cm), 5)
    elif turn == "O":
        pygame.draw.circle(screen, XY_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - O_cm, 2) 
    pygame.time.wait(10)

def draw_XoaXY(turn: str, row: int, col: int) -> None:
    XY_COLOR = (255, 255, 255)
    if turn == "X":
        pygame.draw.line(screen, XY_COLOR, (col * SQUARE_SIZE + X_cm, row * SQUARE_SIZE + X_cm), (col * SQUARE_SIZE + SQUARE_SIZE - X_cm, row * SQUARE_SIZE + SQUARE_SIZE - X_cm), 5); 
        pygame.draw.line(screen, XY_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE - X_cm, row * SQUARE_SIZE + X_cm), (col * SQUARE_SIZE + X_cm, row * SQUARE_SIZE + SQUARE_SIZE - X_cm), 5)
    elif turn == "O":
        pygame.draw.circle(screen, XY_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - O_cm, 2) 

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

# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
#               Phần cập nhật Bảng đánh giá 
# Hàm check Win
def checkWin(banco: list, turn: str, x: int, y: int) -> bool:
    '''
        Hàm check Win
        Trả về True nếu "turn" Win
        Nếu không thì trả về False

    '''
    turn_X = [0, 0, 0, 0, 0, 0, 0, 0]
    for dx, dy in directions:
        dem = 0; i = 1
        while True:
            new_x = x + dx * i; new_y = y + dy * i
            if 0 <= new_x < nxn and 0 <= new_y < nxn:
                giatri = banco[new_x][new_y]
                if giatri == turn:
                    dem += 1
                else:
                    break
            else:
                break
            i += 1
        j = Direc[dx,dy]-1
        turn_X[j] = dem
        if j >= 4:
            if turn_X[j] + turn_X[j-4] >= 4:
                return True
    return False

def Update_Score(banco: list, Map: list, turn: str, x: int, y: int, dx: int, dy: int, ScorePlayer: list, ScoreAI: list, ScoreTong: list, T_player: dict, T_Ai: dict, T_Tong: dict) -> None:
    '''
        Hàm Tính lại điểm đánh giá cho ô trống theo hướng bị ảnh hưởng
        Cập nhật Các bảng đánh giá ScorePlayer, ScoreAI, ScoreTong
            và Các từ điển lưu vị trí T_player, T_Ai, T_Tong

    '''
    if turn == player:
        matrix = ScorePlayer; T_matrix = T_player
    else: 
        matrix = ScoreAI; T_matrix = T_Ai

    if (dx, dy) in [ (1, 0), (1, -1), (0, -1), (-1, -1) ]:
        xau = Map[x][y][Direc[(dx, dy)]] + "X" + Map[x][y][Direc[(-dx, -dy)]]   
    elif (dx, dy) in [ (-1, 0),(-1, 1),  (0, 1), ( 1, 1 ) ]:
        xau = Map[x][y][Direc[(-dx, -dy)]] +  "X" + Map[x][y][Direc[(dx, dy)]]
    k = Direc[(dx, dy)]
    if k > 4:
        k -= 4
    Map[x][y][8 + k] = TH[xau]

    oldScore = matrix[x][y]
    m = [Map[x][y][9],Map[x][y][10],Map[x][y][11],Map[x][y][12]]; m.sort();
    if m[0] == m[1] == "C":
        m[0] = "B"
    elif m[0] == m[1] == "D":
        m[0] = "C"

    Map[x][y][0] = "".join(m)

    newScore = Map[x][y][0];
    RemoveT(T_matrix, matrix[x][y], x, y); matrix[x][y] = newScore; AddT(T_matrix, matrix[x][y], x, y)
    
    RemoveT(T_Tong, ScoreTong[x][y], x, y);
    tong = ScorePlayer[x][y] + ScoreAI[x][y]; tong = list(tong); tong.sort(); ScoreTong[x][y] = "".join(tong[:4])
    AddT(T_Tong, ScoreTong[x][y], x, y);

def Update_Map(banco: list, Map: list, turn: str, x: int, y: int, dx: int, dy: int, ScorePlayer: list, ScoreAI: list, ScoreTong: list, T_player: dict, T_Ai: dict, T_Tong: dict) -> None:
    '''
        Hàm Cập nhật lại thông tin về hướng bị ảnh hưởng cho ô trống
        Truyền thông tin tới Update_Score

    '''
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

def SCAN(banco: list, Map: list, turn: str, x: int, y: int, ScorePlayer: list, ScoreAI: list, ScoreTong: list, T_player: dict, T_Ai: dict, T_Tong: dict) -> None:
    '''
        Hàm Quét các ô trống bị ảnh hưởng khi thực hiện 1 nước cờ
        Truyền tọa độ các ô trống đó và "hướng ảnh hưởng"
        vào Update_Map

    '''
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
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
#           Phần Áp dụng giải thuật MiniMax

diemABC = {"A": 100000, "B": 10000, "C": 1000, "D": 100, "E": 10, "F": 0}
def DiemBanCo(Tudien):
    # Tổng điểm của Bàn cờ là tổng điểm của tất cả các giá trị đã đánh giá trong danh sách
    e = 0; 
    for key in Tudien:
        diem_key = 0
        for j in key: # j: A B C D E F 
            diem_key += diemABC[j]
        e += diem_key*len(Tudien[key])
    return e

def minimax(Board: list, isMaximizing: bool, depth: int, alpha: int, beta: int, Score_Player: list, Score_AI: list, Score_Tong: list, Tplayer: dict, TAi: dict, TTong: dict, Map_Player: list, Map_AI: list, x: int = -1, y: int = -1) -> tuple[int, list[tuple[int, int]]]:
    '''
        Hàm tính toán minimax kết hợp với 1 loạt dữ liệu đánh giá có sẵn
        Trả về tọa độ của ô có điểm cao nhất

    '''
    if depth == 0:
        pygame.display.update()
        if isMaximizing:
            T_tancong = T_player; T_phongthu = TAi
        else:
            T_tancong = TAi; T_phongthu = T_player
        result = DiemBanCo(T_tancong) - DiemBanCo(T_phongthu)
        return result, None

    # -------------------------------------------------------------------------------------
    # Khối lấy ra N_o giá trị có "điểm đánh giá" cao nhất <=> nước đi khả thi nhất
    N_o = 5
    list_Best = []
    T = list(TTong.keys()); T.sort()
    for i in T:
        if i[0] == "A" or i[0] == "B":
            list_Best = TTong[i]
            break
        list_Best += TTong[i]
        if len(list_Best) > N_o:
            break
    #list_Best = list_Best[:N_o]
    # -------------------------------------------------------------------------------------

    if isMaximizing:
        maxVal = float('-inf');
        best_move = [list_Best[0]]
        for (x, y) in list_Best:
            # draw_XY(AI, x, y)
            # row = x; col = y
            Board[x][y] = AI;
            if checkWin(Board, AI, x, y):
                Val = 10000000
                Board[x][y] = "."
                maxVal = max(Val, maxVal); best_move = [(x, y)]
                break
            # -------------------------------------------------------------------------------------
            # Khối cập nhật, duy trì "data đánh giá"
            Board1 = copy.deepcopy(Board);  
            Score_Player1 = copy.deepcopy(Score_Player); Score_AI1 = copy.deepcopy(Score_AI); Score_Tong1 = copy.deepcopy(Score_Tong); Tplayer1 = copy.deepcopy(Tplayer); TAi1 = copy.deepcopy(TAi); TTong1 = copy.deepcopy(TTong); Map_Player1 = copy.deepcopy(Map_Player); Map_AI1 = copy.deepcopy(Map_AI);
            RemoveT(Tplayer1, Score_Player1[x][y], x, y); RemoveT(TAi1, Score_AI1[x][y], x, y); RemoveT(TTong1, Score_Tong1[x][y], x, y)
            SCAN(Board1, Map_Player1, player, x, y, Score_Player1, Score_AI1, Score_Tong1, Tplayer1, TAi1,  TTong1);
            SCAN(Board1, Map_AI1, AI, x, y, Score_Player1, Score_AI1, Score_Tong1, Tplayer1, TAi1,  TTong1);
            # -------------------------------------------------------------------------------------
            Val, move = minimax(Board1, False, depth-1, alpha, beta, Score_Player1, Score_AI1, Score_Tong1, Tplayer1, TAi1, TTong1, Map_Player1, Map_AI1, x, y)
            # draw_XoaXY(AI, x, y)
            Board[x][y] = "."

            if Val > maxVal:
                best_move.clear()
                maxVal = Val; best_move = [(x, y)]
            elif Val == maxVal:
                best_move.append((x, y))
            
            alpha = max(alpha, Val)
            if beta <= alpha:
                break

        return maxVal, best_move

    else:
        minVal = float('inf');
        best_move = [list_Best[0]]
        for (x, y) in list_Best:
            # draw_XY(player, x, y)
            # row = x; col = y
            Board[x][y] = player;
            if checkWin(Board, player, x, y):
                Val = -10000000
                Board[x][y] = "."
                minVal = min(Val, maxVal); best_move = [(x, y)]
                break
            # -------------------------------------------------------------------------------------
            # Khối cập nhật, duy trì "data đánh giá"
            Board1 = copy.deepcopy(Board);  
            Score_Player1 = copy.deepcopy(Score_Player); Score_AI1 = copy.deepcopy(Score_AI); Score_Tong1 = copy.deepcopy(Score_Tong); Tplayer1 = copy.deepcopy(Tplayer); TAi1 = copy.deepcopy(TAi); TTong1 = copy.deepcopy(TTong); Map_Player1 = copy.deepcopy(Map_Player); Map_AI1 = copy.deepcopy(Map_AI);
            RemoveT(Tplayer1, Score_Player1[x][y], x, y); RemoveT(TAi1, Score_AI1[x][y], x, y); RemoveT(TTong1, Score_Tong1[x][y], x, y)
            SCAN(Board1, Map_Player1, player, x, y, Score_Player1, Score_AI1, Score_Tong1, Tplayer1, TAi1,  TTong1);
            SCAN(Board1, Map_AI1, AI, x, y, Score_Player1, Score_AI1, Score_Tong1, Tplayer1, TAi1,  TTong1);
            # -------------------------------------------------------------------------------------
            Val, move = minimax(Board1, True, depth-1, alpha, beta, Score_Player1, Score_AI1, Score_Tong1, Tplayer1, TAi1, TTong1, Map_Player1, Map_AI1, x, y)
            # draw_XoaXY(player, x, y)
            Board[x][y] = "."


            if Val < minVal:
                minVal = Val; best_move = [(x, y)]
            elif Val == minVal:
                best_move.append((x, y))

            beta = min(beta, Val)
            if beta <= alpha:
                break
       
        return minVal, best_move
def UuTien_move(T_Ai: dict, T_player: dict) -> tuple[int, int]:
    '''
        Hàm xét các trường hợp chắc chắn cần đi
        Nếu không nằm trong các trường hợp chắc chắn -> (-1, -1)

    '''
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
    return (-1, -1)

def AI_move():
    (x, y) = UuTien_move(T_Ai, T_player)
    if (x, y) != (-1, -1):
        pygame.time.wait(1000)
        return (x, y)

    # deepcopy rất rất nhiều "data"
    Board = copy.deepcopy(banco);   
    Score_Player = copy.deepcopy(ScorePlayer); Score_AI = copy.deepcopy(ScoreAI); Score_Tong = copy.deepcopy(ScoreTong); Tplayer = copy.deepcopy(T_player); TAi = copy.deepcopy(T_Ai); TTong = copy.deepcopy(T_Tong); Map_Player = copy.deepcopy(MapPlayer); Map_AI = copy.deepcopy(MapAI);
    
    best_score, best_move = minimax(Board, True, max_depth,  float('-inf'), float('inf'), Score_Player, Score_AI, Score_Tong, Tplayer, TAi, TTong, Map_Player, Map_AI)
    
    return random.choice(best_move)

# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
#                   Phần khởi chạy, duy trì game
def game_loop():
    global ScorePlayer, ScoreAI, ScoreTong, T_Ai, T_player, T_Tong, MapPlayer, MapAI, banco, game_over, turn, LuotAI;
    while True:
        draw_board(); draw_XO(banco); 
        # draw_numbers()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over and not LuotAI:
                x_mouse, y_mouse = pygame.mouse.get_pos(); row, col = y_mouse // SQUARE_SIZE, x_mouse // SQUARE_SIZE
                if event.button == 1:
                    if banco[row][col] == '.':
                        banco[row][col] = player; Update_Pre(row, col, player)
                        RemoveT(T_player, ScorePlayer[row][col], row, col); RemoveT(T_Ai, ScoreAI[row][col], row, col); RemoveT(T_Tong, ScoreTong[row][col], row, col);
                        ScorePlayer[row][col] = "-1"; ScoreAI[row][col] = "-1"; ScoreTong[row][col] = "-1"
                        if checkWin(banco, player, row, col):
                            game_over = True; 
                            break
                        SCAN(banco, MapPlayer, player, row, col, ScorePlayer, ScoreAI, ScoreTong, T_player, T_Ai,  T_Tong);
                        SCAN(banco, MapAI, AI, row, col, ScorePlayer, ScoreAI, ScoreTong, T_player, T_Ai,  T_Tong);
                        LuotAI = True

            if LuotAI and not game_over:
                draw_board(); draw_XO(banco); # draw_numbers()
                pygame.display.update()
                (x, y) = AI_move()
                banco[x][y] = AI; Update_Pre(x, y, AI)
                RemoveT(T_player, ScorePlayer[x][y], x, y); RemoveT(T_Ai, ScoreAI[x][y], x, y); RemoveT(T_Tong, ScoreTong[x][y], x, y)
                ScorePlayer[x][y] = "-1"; ScoreAI[x][y] = "-1"; ScoreTong[x][y] = "-1"
                if checkWin(banco, AI, x, y):
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
            if turn == AI:
                winner_text = font.render(f'{turn} wins!', True, (255, 0, 0))
            else:
                winner_text = font.render(f'{turn} wins!', True, (0, 255, 0))
            Comment_1 = font.render('Press "R" to reset', True, (0, 0, 255))
            screen.blit(winner_text, (WINDOW_WIDTH // 2 - winner_text.get_width() // 2, WINDOW_HEIGHT // 2 - winner_text.get_height() // 2))
            screen.blit(Comment_1, (WINDOW_WIDTH // 2 - Comment_1.get_width() // 2, WINDOW_HEIGHT // 2 - Comment_1.get_height() // 2 + 50))

        pygame.display.flip()

Init();
game_loop()
# --------------------------------------------------------------------------

