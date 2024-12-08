#pygame
# thư viên pygame
# chuyển clock.py -> clock.ese dùng pyinstaller

#C:\Users\iwant\Desktop\Python\Sublime Text>pip install pygame : tải thư viện pygame
#Ctrl + C trong Command khi chưa thiết kế nút Kick

#Vẽ lên màn hình: 
# pygame.draw.rect(screen, WHITE, (x,y,Ngang,Dọc))
# -> vẽ hình vuông trên screen, màu WHITE, tại tọa độ (x,y), Ngang, Dọc
# pygame.draw.circle(screen, WHITE, (x,y), r))
# -> vẽ hình tròn trên screen, màu WHITE, tâm có tọa độ (x,y), bán kính r
# pygame.draw.line(screen, WHITE, (x,y), r))
# -> vẽ đường thẳng trên screen, màu WHITE, tâm có tọa độ (x,y), độ dài r

#Tạo kí tự:
#font = pygame.font.SysFont('sans',50)
#text_1 = font.render('<kí tự>', True, <màu>)

#Viết kí tự:
#screen.blit(text_1, (x,y)) 
# -> viết text_1 lên screen, tọa độ (x,y)

#Tạo âm thanh
# sound = pygame.mixer.Sound('alarm.wav')
# file alarm.wav cùng thư mục 
# pygame.mixer.pause() : tạm dừng các kênh âm thanh
# pygame.mixer.Sound.play(sound) : phát âm thanh

# chuyển clock.py -> clock.ese dùng pyinstaller
# C:\Users\iwant\Desktop\Python\Sublime Text>pyinstaller Snake.py --onefile --noconsole --icon=Snake.ico # jpg to ico
# C:\Users\iwant\Desktop\Python\Sublime Text>pyinstaller a.py --tạo 1 file --không hiện console --icon= hình ảnh .ico


# Lấy kích thước màn hình
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h
# print(screen_width, screen_height)