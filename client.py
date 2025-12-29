import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

HOST = '127.0.0.1'
PORT = 65432

class CollaborativeEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Trình soạn thảo cộng tác (Distributed System Lab)")
        
        # Khu vực soạn thảo văn bản
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20)
        self.text_area.pack(padx=10, pady=10)
        
        # Sự kiện: Khi nhả phím (KeyRelease) thì gửi dữ liệu
        self.text_area.bind('<KeyRelease>', self.send_update)

        # Kết nối đến server
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((HOST, PORT))
            
            # Tạo luồng để luôn lắng nghe dữ liệu từ server
            receive_thread = threading.Thread(target=self.receive_updates)
            receive_thread.daemon = True # Tắt luồng khi tắt app
            receive_thread.start()
        except Exception as e:
            print(f"Không thể kết nối đến Server: {e}")

    def send_update(self, event):
        """Gửi toàn bộ nội dung văn bản lên server"""
        # Bỏ qua các phím điều hướng để tránh spam traffic không cần thiết
        if event.keysym in ['Up', 'Down', 'Left', 'Right']:
            return
            
        content = self.text_area.get("1.0", tk.END) # Lấy toàn bộ text
        try:
            self.client_socket.send(content.encode('utf-8'))
        except Exception as e:
            print(f"Lỗi gửi dữ liệu: {e}")

    def receive_updates(self):
        """Nhận dữ liệu từ server và cập nhật giao diện"""
        while True:
            try:
                data = self.client_socket.recv(4096)
                if not data:
                    break
                
                new_content = data.decode('utf-8')
                
                # Cập nhật giao diện (xóa cũ, điền mới)
                # Lưu ý: Trong thực tế cần dùng thuật toán OT/CRDT để tránh xung đột con trỏ
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert("1.0", new_content.strip()) # strip để bỏ dòng trống thừa
            except:
                break

if __name__ == "__main__":
    root = tk.Tk()
    app = CollaborativeEditor(root)
    root.mainloop()