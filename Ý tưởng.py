

@ AI chơi cờ caro - Phiên bản đơn giản

- Đầu tiên là biểu diễn bàn cờ:   Bàn cờ 19x19 với các ô chưa đánh là ".", "X" và "O"

	1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 						 	2  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  2
	. . . . . . . . . . . . . . . . . . . 1 						1  3  2  2  2  2  2  2  2  2  2  2  2  2  2  2  2  3  1
	. . . . . . . . . . . . . . . . . . . 2 						1  2  4  3  3  3  3  3  3  3  3  3  3  3  3  3  4  2  1
	. . . . . . . . . . . . . . . . . . . 3 						1  2  3  5  4  4  4  4  4  4  4  4  4  4  4  5  3  2  1
	. . . . . . . . . . . . . . . . . . . 4 						1  2  3  4  6  5  5  5  5  5  5  5  5  5  6  4  3  2  1
	. . . . . . . . . . . . . . . . . . . 5 						1  2  3  4  5  7  6  6  6  6  6  6  6  7  5  4  3  2  1
	. . . . . . . . . . . . . . . . . . . 6							1  2  3  4  5  6  8  7  7  7  7  7  8  6  5  4  3  2  1
	. . . . . . . . . . . . . . . . . . . 7							1  2  3  4  5  6  7  9  8  8  8  9  7  6  5  4  3  2  1
	. . . . . . . . . . . . . . . . . . . 8							1  2  3  4  5  6  7  8 10  9 10  8  7  6  5  4  3  2  1
	. . . . . . . . . . . . . . . . . . . 9							1  2  3  4  5  6  7  8  9 12  9  8  7  6  5  4  3  2  1
	. . . . . . . . . . . . . . . . . . . 0							1  2  3  4  5  6  7  8 10  9 10  8  7  6  5  4  3  2  1
	. . . . . . . . . . . . . . . . . . . 1							1  2  3  4  5  6  7  9  8  8  8  9  7  6  5  4  3  2  1
	. . . . . . . . . . . . . . . . . . . 2							1  2  3  4  5  6  8  7  7  7  7  7  8  6  5  4  3  2  1
	. . . . . . . . . . . . . . . . . . . 3							1  2  3  4  5  7  6  6  6  6  6  6  6  7  5  4  3  2  1
	. . . . . . . . . . . . . . . . . . . 4							1  2  3  4  6  5  5  5  5  5  5  5  5  5  6  4  3  2  1
	. . . . . . . . . . . . . . . . . . . 5							1  2  3  5  4  4  4  4  4  4  4  4  4  4  4  5  3  2  1
	. . . . . . . . . . . . . . . . . . . 6							1  2  4  3  3  3  3  3  3  3  3  3  3  3  3  3  4  2  1
	. . . . . . . . . . . . . . . . . . . 7							1  3  2  2  2  2  2  2  2  2  2  2  2  2  2  2  2  3  1
	. . . . . . . . . . . . . . . . . . . 8							2  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  2
	. . . . . . . . . . . . . . . . . . . 9						# đi kèm với 1 bảng đánh giá "Giá trị" các ô 
	 						
@@ Ý tưởng là:
		@@ Mỗi khi 1 ô được đánh X hoặc O thì nó cũng chỉ "ảnh hưởng" tới 16 vị trí theo 8 hướng
												
	Trong trường hợp này khi đánh X vào tọa độ (8,11)	
														các ô mà nó ảnh hưởng tới sẽ là  (Y)
			1 2 3 4 5 6 7 8 9 0 1 2 3 4 5				1 2 3 4 5 6 7 8 9 0 1 2 3 4 5				
			. . . . . . . . . . . . . . . 1				. . . . . . . . . . . . . . . 1 			
			. . . . . . . . . . . . . . . 2				. . . . . . . . . . . . . . . 2 			
			. . . . . . . . . . . . . . . 3				. . . . . . . . . . . . . . . 3
			. . . . . . . . . . . . . . . 4				. . . . . . . . . . . . . . . 4
			. . . . . . . . . . . . . . . 5				. . . . . . . . . . . . . . . 5
			. . . . . . . . . . . . . . . 6				. . . . . . . . Y . Y . Y . . 6
			. . . . . . . . . . . . . . . 7				. . . . . . . . . Y Y Y . . . 7
			. . . . . . . . . . X . . . . 8				. . . . . . . . Y Y - Y Y . . 8
			. . . . . . . . . . . . . . . 9				. . . . . . . . . Y Y Y . . . 9
			. . . . . . . . . . . . . . . 0				. . . . . . . . Y . Y . Y . . 0
			. . . . . . . . . . . . . . . 1				. . . . . . . . . . . . . . . 1
			. . . . . . . . . . . . . . . 2				. . . . . . . . . . . . . . . 2
			. . . . . . . . . . . . . . . 3				. . . . . . . . . . . . . . . 3
			. . . . . . . . . . . . . . . 4				. . . . . . . . . . . . . . . 4
			. . . . . . . . . . . . . . . 5				. . . . . . . . . . . . . . . 5
    												#Code của tôi mới chỉ lấy ra 16 vị trí này 

    @@@ Ta có thể cập nhật bảng đánh giá chỉ cho 16 vị trí này 
    Ví dụ: lượt vừa đánh là X, ta xét 16 vị trí phía trên
    Cộng 10 điểm nếu vị trí đang xét khiến O chiến thắng ngay lập tức
    Cộng 8  điểm nếu vị trí đang xét ngăn chặn X chiến thắng
    Cộng ... điểm nếu tạo ra 2 hàng 3 ô liên tiếp (mở ra cơ hội chiến thắng cho O)
    Cộng ... điểm nếu ngăn chặn cơ hội chiến thắng của X 
    => Sau khi tính toán lại điểm cho 16 vị trí, ta có 1 bảng đánh giá hoàn chỉnh, 
    có thể áp dụng thêm thuật toán tìm kiếm A* hoặc MiniMax để code tính toán thêm vài bước tiếp theo

  @ Thuật toán vẫn sẽ chọn được nước đi mà nó cho là tốt nhất
