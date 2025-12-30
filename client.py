import socket
import threading
import json
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox

HOST = '127.0.0.1'
PORT = 65432

class CollaborativeEditor:
    def __init__(self, root):
        self.root = root
        self.root.withdraw()
        
        self.username = simpledialog.askstring("Đăng nhập", "Nhập tên của bạn:", parent=root)
        if not self.username:
            self.root.destroy()
            return
            
        self.root.deiconify()
        self.root.title(f"Editor V3.0 - {self.username}")
        
        # GUI Components
        self.status_label = tk.Label(root, text="Đang kết nối...", bd=1, relief=tk.SUNKEN, anchor=tk.W, bg="#e1e1e1")
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Arial", 12))
        self.text_area.pack(expand=True, fill='both', padx=5, pady=5)
        self.text_area.bind('<KeyRelease>', self.send_update)

        # Network setup
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((HOST, PORT))
            self.client_socket.send(self.username.encode('utf-8')) # Gửi tên thô (không cần JSON)
            
            # Start background thread
            threading.Thread(target=self.receive_updates, daemon=True).start()
            self.status_label.config(text=f"Đã kết nối tới {HOST}:{PORT}")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể kết nối Server: {e}")
            self.root.destroy()

    def send_update(self, event):
        if event.keysym in ['Up', 'Down', 'Left', 'Right']: return
            
        content = self.text_area.get("1.0", tk.END)
        packet = {"type": "update_text", "content": content}
        
        try:
            # QUAN TRỌNG: Thêm \n vào cuối gói tin gửi đi
            json_str = json.dumps(packet) + "\n"
            self.client_socket.sendall(json_str.encode('utf-8'))
        except:
            self.status_label.config(text="Mất kết nối!", fg="red")

    def receive_updates(self):
        buffer = "" # Bộ đệm lưu trữ dữ liệu chưa hoàn chỉnh
        
        while True:
            try:
                data = self.client_socket.recv(4096)
                if not data: break
                
                buffer += data.decode('utf-8')
                
                # Vòng lặp tách dòng: Xử lý từng gói tin JSON một
                while "\n" in buffer:
                    message, buffer = buffer.split("\n", 1)
                    if not message.strip(): continue
                    
                    try:
                        self.process_packet(json.loads(message))
                    except json.JSONDecodeError:
                        print(f"Lỗi JSON: {message}")
                        
            except Exception as e:
                print(f"Ngắt kết nối: {e}")
                break
    
    def process_packet(self, msg):
        """Hàm xử lý logic gói tin"""
        if msg['type'] == 'full_text' or msg['type'] == 'update_text':
            # Lưu vị trí con trỏ
            try:
                current_pos = self.text_area.index(tk.INSERT)
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert("1.0", msg['content'].strip())
                self.text_area.mark_set(tk.INSERT, current_pos)
            except:
                pass # Bỏ qua lỗi giao diện nhỏ
            
        elif msg['type'] == 'notification':
            self.status_label.config(text=msg['content'], fg="blue")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x400")
    app = CollaborativeEditor(root)
    root.mainloop()