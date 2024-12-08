import pygame
import sys
import checkWin

# Khởi tạo Pygame
pygame.init()

# Số lượng ô vuông trên bàn cờ 
GRID_SIZE = 15; 
nxn = GRID_SIZE; banco = []; NumberToWin = 5; player = ""
for i in range(nxn):
    banco.append([])
    for j in range(nxn):
        banco[i].append('.')
# Lấy kích thước màn hình
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h
# print(screen_width, screen_height)
T = {} # 

def addT (value, x, y):
    if value not in T:
        T[value] = []
    T[value].append((x,y))

def checkR(value, x, y):
    if value in T:
        T[value].remove( (x, y))


def taoBangDanhGia(N):
    matrix = [[0] * N for _ in range(N)]
    num_layers = (N + 1) // 2

    for layer in range(num_layers):
        value = layer + 1
        for i in range(layer, N - layer):
            matrix[layer][i] = value
            if value not in T:
                T[value] = []
            T[value].append((layer, i))
        for i in range(layer, N - layer):
            matrix[N - layer - 1][i] = value
            if value not in T:
                T[value] = []
            T[value].append((N - layer - 1, i))
        for i in range(layer + 1, N - layer - 1):
            matrix[i][layer] = value
            if value not in T:
                T[value] = []
            T[value].append((i, layer))
        for i in range(layer + 1, N - layer - 1):
            matrix[i][N - layer - 1] = value
            if value not in T:
                T[value] = []
            T[value].append((i, N - layer - 1))

    for i in range(N):
        checkR(matrix[i][i], i, i); matrix[i][i] += 1; addT(matrix[i][i], i, i)
        checkR(matrix[i][N - i - 1], i, N - i - 1); matrix[i][N - i - 1] += 1; addT(matrix[i][N - i - 1], i, N - i - 1)
    return matrix

def print_matrix(matrix):
    for row in matrix:
        print(" ".join(f"{value:2}" for value in row))

Score = taoBangDanhGia(nxn); print_matrix(Score); #print(T)

scoreMax = 0; List_scoreMax = []

# Kích thước của cửa sổ
WINDOW_WIDTH = 800; WINDOW_HEIGHT = 800
SQUARE_SIZE = min(WINDOW_WIDTH, WINDOW_HEIGHT) // GRID_SIZE # Tính toán kích thước mỗi ô vuông
# Màu sắc
WHITE = (255, 255, 255); BACKGROUND_COLOR = (255, 255, 255); LINE_COLOR = (0, 0, 0); X_COLOR = (0, 0, 0); O_COLOR = (0, 0, 0)
# Tạo cửa sổ
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Bàn cờ XO')
# Hàm vẽ bàn cờ
def draw_board():
    screen.fill(BACKGROUND_COLOR)
    # Vẽ các đường kẻ
    #      pygame.draw.circle(screen, WHITE, (x,y), r))
    # -> vẽ hình tròn trên screen, màu, tâm có tọa độ (x,y), bán kính r

    for row in range(1, GRID_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (0, row * SQUARE_SIZE) , (WINDOW_WIDTH, row * SQUARE_SIZE)  , 3)
        pygame.draw.line(screen, LINE_COLOR, (row * SQUARE_SIZE, 0) , (row * SQUARE_SIZE, WINDOW_HEIGHT) , 3)
    pygame.draw.line(screen, LINE_COLOR, (0, 0 * SQUARE_SIZE), (WINDOW_WIDTH, 0* SQUARE_SIZE), 5); pygame.draw.line(screen, LINE_COLOR, (0 * SQUARE_SIZE, 0), (0 * SQUARE_SIZE, WINDOW_HEIGHT), 5)
    pygame.draw.line(screen, LINE_COLOR, (0, GRID_SIZE * SQUARE_SIZE-2), (WINDOW_WIDTH, GRID_SIZE* SQUARE_SIZE-2), 5); pygame.draw.line(screen, LINE_COLOR, (GRID_SIZE * SQUARE_SIZE-1, 0), (GRID_SIZE * SQUARE_SIZE-1, WINDOW_HEIGHT), 5)
# Hàm vẽ X và O
def draw_XO(banco):
	# liên tục phải vẽ X và O lên màn hình ==> vậy thì check luôn xem list các ô có điểm lớn nhất đang là những ô nào 
    global scoreMax; global List_scoreMax
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if banco[row][col] == 'X':
                pygame.draw.line(screen, X_COLOR, (col * SQUARE_SIZE + 20, row * SQUARE_SIZE + 20), 
                                 (col * SQUARE_SIZE + SQUARE_SIZE - 20, row * SQUARE_SIZE + SQUARE_SIZE - 20), 5)
                pygame.draw.line(screen, X_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE - 20, row * SQUARE_SIZE + 20), 
                                 (col * SQUARE_SIZE + 20, row * SQUARE_SIZE + SQUARE_SIZE - 20), 5)
               	if (row,col) in List_scoreMax:
               		List_scoreMax.remove( (row, col)); scoreMax = 0
            elif banco[row][col] == 'O':
                #pygame.draw.circle(screen, WHITE, (x,y), r))
                pygame.draw.circle(screen, O_COLOR, 
                                   (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 
                                   SQUARE_SIZE // 2 - 7, 2) 
                if (row,col) in List_scoreMax:
               		List_scoreMax.remove( (row, col)); scoreMax = 0
            else:
            	if (row,col) not in List_scoreMax:
	                t = Score[row][col]
	                if t > scoreMax:
	                    scoreMax = t
	                    List_scoreMax = [(row,col)]
	                elif t == scoreMax:
	                    List_scoreMax.append( (row, col))

def update_score(matrix, player, x, y):
    e = []

    directions = [ # kim dong ho tu huong 12h
        (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (-1, -1), (0, -1), (-1, -1)
    ]
    
    # Duyệt qua các hướng và kiểm tra các ô xung quanh
    for dx, dy in directions:
        for i in range(1, 3):  # Kiểm tra 2 ô ở mỗi hướng
            new_x = x + dx * i; 	new_y = y + dy * i
            # Kiểm tra nếu (new_x, new_y) là tọa độ hợp lệ trong ma trận
            if 0 <= new_x < nxn and 0 <= new_y < nxn:
                e.append( (banco[new_x][new_y], new_x, new_y) )
            else:
                e.append(None)  # Nếu ra ngoài ma trận, thêm None
    print(e)


# Hàm quản lý sự kiện chơi cờ
def game_loop():
    global player; global scoreMax
    player = 'X'  # Bắt đầu với X
    game_over = False

    while True:
        draw_board()
        draw_XO(banco)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x_mouse, y_mouse = pygame.mouse.get_pos()
                row, col = y_mouse // SQUARE_SIZE, x_mouse // SQUARE_SIZE
                if banco[row][col] == '.':
                    banco[row][col] = player; Score[row][col] = -1000
                    # print(scoreMax, List_scoreMax)
                    update_score(Score, player, row, col)
                    if checkWin.checkWin(banco, player, row+1, col+1, nxn, NumberToWin) == "Win":
                        game_over = True
                        break
                    if player == "X":
                        player = "O"
                    else:
                        player = "X"

        if game_over:
            font = pygame.font.Font(None, 74)
            winner_text = font.render(f'{player} wins!', True, (0, 0, 0))
            screen.blit(winner_text, (WINDOW_WIDTH // 2 - winner_text.get_width() // 2, WINDOW_HEIGHT // 2 - winner_text.get_height() // 2))

        pygame.display.flip()

# Bắt đầu trò chơi
game_loop()
