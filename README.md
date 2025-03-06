Ứng dụng hàm đánh giá heuristic trong giải thuật Minimax và cắt tỉa Alpha-beta trong game cờ caro

Giới thiệu
Đây là một dự án AI chơi cờ caro, được phát triển để thử nghiệm và tối ưu hóa thuật toán Minimax với độ sâu và cắt tỉa Alpha-Beta cùng với hàm đánh giá heuristic

Công nghệ sử dụng
Ngôn ngữ lập trình: Python
Thư viện: Pygame
Cách hoạt động cơ bản
Với các ô trống bị ảnh hưởng bởi các nước cờ X/O được dùng hàm đánh giá heuristic điểm để có thể chọn ra 5 điểm có số điểm cao nhất phục vụ cho duyệt Minimax giúp giảm không gian tìm kiếm
Thuật toán Minimax với độ sâu hạn chế là 2: AI đánh giá tất cả các nước đi khả thi để tìm ra nước đi tốt nhất dựa trên cây trạng thái.
Cắt tỉa Alpha-Beta: tăng tốc thuật toán Minimax bằng cách loại bỏ các nhánh không cần thiết.
Đánh giá
AI có thể chủ động tấn công người chơi
Tỉ lệ thắng AI vẫn còn thấp
Nếu người chơi dùng đúng một form đánh mà không nguy hiểm thì AI cũng sẽ lặp lại trạng thái đã dùng từ những ván trước (không có sự thay đổi, cứng nhắc)
Hướng dẫn cài đặt

Cài đặt thư viện cần thiết
pip install -U pygame
Chạy chương trình
python main.py

Trên Windows bạn có thể trải nghiệm ngay với file .exe
