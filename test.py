def check_surrounding_values(matrix, x, y, X):
    # Khởi tạo danh sách kết quả
    surrounding_values = []

    # Danh sách các hướng: (dx, dy) = (delta x, delta y)
    directions = [
        # kim dong ho tu huong 12h
        (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (-1, -1), (0, -1), (-1, -1)
    ]
    
    # Duyệt qua các hướng và kiểm tra các ô xung quanh
    for dx, dy in directions:
        for i in range(1, 3):  # Kiểm tra 2 ô ở mỗi hướng
            new_x = x + dx * i
            new_y = y + dy * i
            # Kiểm tra nếu (new_x, new_y) là tọa độ hợp lệ trong ma trận
            if 0 <= new_x < len(matrix) and 0 <= new_y < len(matrix[0]):
                surrounding_values.append(matrix[new_x][new_y])
            else:
                surrounding_values.append(None)  # Nếu ra ngoài ma trận, thêm None
    
    return surrounding_values

# Ví dụ sử dụng:
matrix = [
    [1, 2, 3, 4, 5],
    [6, 7, 8, 9, 10],
    [11, 12, 13, 14, 15],
    [16, 17, 18, 19, 20],
    [21, 22, 23, 24, 25]
]

x, y = 2, 2  # Toạ độ của ô (13 trong ví dụ)
X = matrix[x][y]  # Giá trị tại ô (x, y)

result = check_surrounding_values(matrix, x, y, X)
print(result)
