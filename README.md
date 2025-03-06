# 🏆 Ứng dụng hàm đánh giá heuristic trong giải thuật Minimax và cắt tỉa Alpha-beta trong game cờ caro  

## 📌 Giới thiệu  
**Đây là một dự án AI chơi cờ caro**, được phát triển để thử nghiệm và tối ưu hóa thuật toán **Minimax** với độ sâu và cắt tỉa **Alpha-Beta**, kết hợp với hàm đánh giá heuristic.

---

## 🔧 Công nghệ sử dụng  
- **Ngôn ngữ lập trình:** Python  
- **Thư viện:** Pygame  

---

## ⚙️ Cách hoạt động cơ bản  
- Các ô trống **bị ảnh hưởng bởi các nước cờ X/O** sẽ được **đánh giá điểm bằng heuristic**.  
- Chọn ra **5 ô có điểm cao nhất** để duyệt thuật toán **Minimax**, giúp **giảm không gian tìm kiếm** và tối ưu hóa hiệu suất.  

---

## 📊 Đánh giá  
✔️ **AI có thể chủ động tấn công người chơi.**  
❌ **Tỉ lệ thắng của AI vẫn còn thấp.**  
⚠️ **Nếu người chơi sử dụng một chiến thuật cố định không nguy hiểm, AI có thể lặp lại trạng thái từ những ván trước (cứng nhắc, không học hỏi).**  

---

## 🛠️ Hướng dẫn cài đặt  
### **Cài đặt thư viện cần thiết**  
```bash
pip install -U pygame
