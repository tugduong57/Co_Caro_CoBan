import pygame, sys, checkWin
# import os
# os.chdir("E:/ThisPC/Desktop/Code/Caro")
# Khởi tạo Pygame
pygame.init()
# Số lượng ô vuông trên bàn cờ 
GRID_SIZE = 15; 
# Cách biến toàn cục
nxn = GRID_SIZE; banco = []; NumberToWin = 5; player = ""; AI = ""; turn = ""
banco = [ ['.']*nxn for _ in range(nxn)]

def taoBangDanhGia(N):
    matrix = [[0] * N for _ in range(N)]
    num_layers = (N + 1) // 2
    for layer in range(5,num_layers):
        value = layer + 1
        for i in range(layer, N - layer):
            matrix[layer][i] = value; matrix[N - layer - 1][i] = value
        for i in range(layer + 1, N - layer - 1):
            matrix[i][layer] = value; matrix[i][N - layer - 1] = value
    for i in range(N):
        matrix[i][i] += 1; matrix[i][N - i - 1] += 1
    return matrix

def print_matrix(matrix):
    for row in matrix:
        print(" ".join(f"{value:5}" for value in row))

Score = taoBangDanhGia(nxn); print_matrix(Score); 
Map = []  # 1 ma trận với mỗi vị trí nó lưu 1 giá trị tổng và 8 xâu cho 8 hướng
# Map[i] -> [value, "North", "N-E", "East", "S-E", "South", "S-W", "West", "N-W"] 
#                   5 -> 1; 6 -> 2; 7 -> 3; 8 -> 4
for i in range(nxn):
    Map.append( [] )
    for j in range(nxn):
        Map[i].append( [0] + ["00"]*8 + [0,0,0,0])
        if i == 0:
            Map[i][j][1] = "-1"
        if j == nxn-1: 
            Map[i][j][3] = "-1"
        if i == nxn-1:
            Map[i][j][5] = "-1"
        if j == 0:
            Map[i][j][7] = "-1"

for i in range(nxn):
    print(Map[i])

# TH: bảng tra cứu điểm
BangDiem = {}
with open("BangDiem.txt", encoding="utf-8") as inp:
    for i in range(34):
        line = inp.readline().split(";")
        BangDiem[line[0]] = int(line[1])
TH = {}
with open("G.txt", encoding="utf-8") as inp:
    for i in range(361):
        xau = "".join(inp.readline().split())
        line = inp.readline().split(";")
        TH[xau] = BangDiem[line[0]] + BangDiem[line[1]]
        
        
Direc = {(-1, 0): 1, (-1, 1): 2, (0, 1): 3, (1, 1): 4, (1, 0): 5, (1, -1):6, (0, -1):7, (-1, -1):8}


# T: dir lưu tọa độ các điểm có cùng value
T = {} # 

def AddT(value, x, y):
    if value not in T:
        T[value] = []
    T[value].append((x,y))

def RemoveT(value, x, y):
    if value in T:
        if (x,y) in T[value]:
            T[value].remove((x, y))
    if T[value] == []:
        T.pop(value)

for i in range(nxn):
    for j in range(nxn):
        value = Score[i][j]
        AddT(value, i, j)       

# Set up
WINDOW_WIDTH = 800; WINDOW_HEIGHT = 800; SQUARE_SIZE = min(WINDOW_WIDTH, WINDOW_HEIGHT) // GRID_SIZE
WHITE = (255, 255, 255); BACKGROUND_COLOR = (255, 255, 255); LINE_COLOR = (0, 0, 0); X_COLOR = (0, 0, 0); O_COLOR = (0, 0, 0)

# Tạo cửa sổ
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Bàn cờ XO')
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

def tinh_score(x, y,dx, dy):
    if (dx, dy) in [ (1, 0), (1, -1), (0, -1), (-1, -1) ]:
        xau = Map[x][y][Direc[(dx, dy)]] + "X" + Map[x][y][Direc[(-dx, -dy)]]   
    elif (dx, dy) in [ (-1, 0),(-1, 1),  (0, 1), ( 1, 1 ) ]:
        xau = Map[x][y][Direc[(-dx, -dy)]] +  "X" + Map[x][y][Direc[(dx, dy)]]
    k = Direc[(dx, dy)]
    if k > 4:
        k -= 4

    Map[x][y][8 + k] = TH[xau]
    oldScore = Score[x][y]
    #RemoveT(Score[x][y], x, y); Score[x][y] -= Map[x][y][0]
    
    Map[x][y][0] = Map[x][y][9] + Map[x][y][10] + Map[x][y][11] + Map[x][y][12]
    newScore = oldScore + Map[x][y][0];
    
    RemoveT(Score[x][y], x, y); Score[x][y] = newScore; AddT(Score[x][y], x, y)

    #Score[x][y] += Map[x][y][0]; AddT(Score[x][y], x, y)

# Hàm tính toán bảng đánh giá
def update_score(turn, matrix, x, y, dx, dy):
    # print("Check ")
    canhke = []
    trang = 1; i = 1
    while True:
        new_x = x + dx*i;     new_y = y + dy*i
        if 0 <= new_x < nxn and 0 <= new_y < nxn:
            giatri = banco[new_x][new_y]
            print(giatri)
            if giatri == turn:
                canhke.append('1') # nếu cùng loại, xét tiếp
                if trang != 0:
                    trang = 0
            elif giatri == ".":
                if trang == 1: # nếu là ô trống đầu tiên
                    canhke.append("0")
                    trang -= 1
                elif trang == 0:
                    canhke.append("0")
                    trang -= 1
                if trang == -1:
                    break
            else:
                canhke.append('-1'); 
                break # Nếu không cùng loại -> dừng
        else:
            canhke.append("-1"); 
            break
        i += 1
    print(Direc[(dx, dy)], canhke)
    if (dx, dy) in [ (1, 0), (1, -1), (0, -1), (-1, -1) ]:
        Map[x][y][Direc[(dx, dy)]] = "".join(canhke[::-1])       #xau = Map[x][y][Direc[(dx, dy)]] + "X" + Map[x][y][Direc[(-dx, -dy)]]    
    elif (dx, dy) in [ (-1, 0),(-1, 1),  (0, 1), ( 1, 1 ) ]:
        Map[x][y][Direc[(dx, dy)]] = "".join(canhke)            # print(Map[x][y][Direc[(-dx, -dy)]], "X", Map[x][y][Direc[(dx, dy)]])

    tinh_score(x,y,dx,dy)

def scan_score(matrix, turn, x, y):
    directions = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
    #               "North", "N-E", "East", "S-E", "South", "S-W", "West", "N-W"
    #                5 -> 1: ; 6 -> 2; 7 -> 3; 8 -> 4
    for dx, dy in directions: ## lan tỏa và check
        h = []; trang = 1; i = 1
        while True:
            new_x = x + dx * i; 	new_y = y + dy * i
            if 0 <= new_x < nxn and 0 <= new_y < nxn:
                giatri = banco[new_x][new_y]
                if giatri == turn: # nếu cùng loại, xét tiếp
                    if trang != 1:
                        trang -= 1
                if giatri == ".":
                    #print(new_x,new_y,turn,dx,dy)
                    trang -= 1;
                    update_score(turn, matrix, new_x, new_y, -dx, -dy)
                    if trang == -1:
                        break
                if giatri != turn and giatri != ".":
                    break # Nếu không cùng loại -> dừng
            else:
                break # Ra ngoài bàn cờ
            i += 1

def game_loop():
    global player; global AI; global turn; player = 'X'; AI = 'O'; turn = player
    game_over = False

    while True:
        draw_board(); draw_XO(banco)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x_mouse, y_mouse = pygame.mouse.get_pos(); row, col = y_mouse // SQUARE_SIZE, x_mouse // SQUARE_SIZE
                if banco[row][col] == '.':

                    banco[row][col] = player; 
                    RemoveT(Score[row][col], row, col)
                    Score[row][col] = -1000
                    if checkWin.checkWin(banco, player, row+1, col+1, nxn, NumberToWin) == "Win":
                        game_over = True; 
                        break
                    scan_score(Score, player, row, col)
                    print_matrix(Score); 

                    (x, y) = T[max(T.keys())][0] # @@@@@

                    banco[x][y] = AI; 
                    draw_board();
                    RemoveT(Score[x][y], x, y)
                    Score[x][y] = -1000
                    if checkWin.checkWin(banco, AI, x+1, y+1, nxn, NumberToWin) == "Win":
                        game_over = True; 
                        break
                    scan_score(Score, AI, x, y)     # check tấn công
                    scan_score(Score, player, x, y) # check phòng thủ
                    print_matrix(Score); 
                    

        if game_over:
            font = pygame.font.Font(None, 74)
            winner_text = font.render(f'{turn} wins!', True, (0, 0, 0))
            screen.blit(winner_text, (WINDOW_WIDTH // 2 - winner_text.get_width() // 2, WINDOW_HEIGHT // 2 - winner_text.get_height() // 2))
        pygame.display.flip()

game_loop()
