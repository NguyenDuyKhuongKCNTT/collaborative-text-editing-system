# 📝 Hệ Thống Soạn Thảo Văn Bản Cộng Tác (Real-time Collaborative Editor)

![Python](https://img.shields.io/badge/Language-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![System](https://img.shields.io/badge/System-Distributed-ff69b4?style=for-the-badge)
![Network](https://img.shields.io/badge/Protocol-TCP%2FSocket-orange?style=for-the-badge)

> **Bài tập lớn môn: Các Hệ thống Phân tán (Distributed Systems)** > Ứng dụng cho phép nhiều người dùng kết nối và cùng chỉnh sửa một văn bản trong thời gian thực.

---

## 📖 Giới thiệu (Overview)

Dự án này xây dựng một hệ thống mô phỏng tính năng cộng tác thời gian thực (tương tự như Google Docs đơn giản). Hệ thống giải quyết các bài toán cơ bản của lập trình phân tán bao gồm: truyền thông qua mạng, đồng bộ dữ liệu và xử lý đa luồng.

### 🚀 Tính năng chính
* **Real-time Synchronization:** Khi một người dùng gõ phím, nội dung được cập nhật ngay lập tức trên màn hình của người khác.
* **Multi-Client Support:** Hỗ trợ nhiều người dùng (Clients) kết nối đồng thời vào một máy chủ (Server).
* **GUI Friendly:** Giao diện đồ họa trực quan, dễ sử dụng (xây dựng bằng Tkinter).

---

## ⚙️ Kiến trúc Hệ thống (Architecture)

Hệ thống hoạt động dựa trên mô hình **Client-Server** kết hợp với cơ chế **Broadcasting**.

| Thành phần | Công nghệ / Kỹ thuật | Mô tả |
| :--- | :--- | :--- |
| **Giao thức** | TCP Socket | Đảm bảo tính tin cậy và thứ tự của dữ liệu truyền tải. |
| **Server** | Python Multithreading | Tạo luồng riêng biệt cho mỗi kết nối Client để xử lý song song. |
| **Consistency** | Last-Writer-Wins | Giải quyết xung đột dữ liệu bằng cách ưu tiên cập nhật mới nhất. |
| **Client** | Tkinter & Threading | Xử lý giao diện và luồng nhận dữ liệu ngầm (Background Listener). |

---

## 🛠️ Cài đặt & Hướng dẫn chạy

### 1. Yêu cầu (Prerequisites)
* [Python 3.x](https://www.python.org/downloads/)
* Git

### 2. Tải mã nguồn
Mở Terminal (hoặc CMD/PowerShell) và chạy lệnh:

```bash
git clone [https://github.com/NguyenDuyKhuongKCNTT/collaborative-text-editing-system.git](https://github.com/NguyenDuyKhuongKCNTT/collaborative-text-editing-system.git)
cd collaborative-text-editing-system
3. Khởi chạy hệ thống
Bước 1: Chạy Server (Máy chủ) Server phải được bật trước để lắng nghe kết nối.

Bash

python server.py
✅ Màn hình sẽ báo: [*] Server đang chạy tại 127.0.0.1:65432

Bước 2: Chạy Client (Người dùng) Mở một cửa sổ Terminal mới (giữ nguyên cửa sổ Server) và chạy:

Bash

python client.py
Bước 3: Giả lập người dùng thứ 2 Mở thêm một cửa sổ Terminal khác và chạy lại lệnh client:

Bash

python client.py
🧪 Kịch bản kiểm thử (Demo)
Để kiểm tra tính năng đồng bộ:

Mở 2 cửa sổ Client và đặt chúng cạnh nhau.

Tại cửa sổ Client A: Gõ dòng chữ Hello Distributed System.

Quan sát Client B: Bạn sẽ thấy dòng chữ xuất hiện gần như tức thời.

Thử xóa hoặc sửa nội dung từ bất kỳ phía nào, bên còn lại sẽ được đồng bộ.

📂 Cấu trúc thư mục
collaborative-text-editing-system/
├── 📄 server.py      # Mã nguồn Server (Socket, Multithreading, Broadcast)
├── 📄 client.py      # Mã nguồn Client (GUI, Event Handling)
└── 📄 README.md      # Tài liệu hướng dẫn này
👨‍💻 Tác giả
Nguyễn Duy Khương, Hồ Viết Sơn Tùng, Phạm Công Trường --- Dự án phục vụ mục đích học tập và nghiên cứu môn Các Hệ thống Phân tán.