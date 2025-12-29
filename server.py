import socket
import threading

# Cấu hình kết nối
HOST = '127.0.0.1'
PORT = 65432

# Biến toàn cục lưu trữ các client và nội dung văn bản
clients = []
current_text = ""

def broadcast(message, sender_socket):
    """Gửi tin nhắn đến tất cả client ngoại trừ người gửi"""
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                client.close()
                clients.remove(client)

def handle_client(client_socket):
    """Xử lý kết nối với từng client riêng biệt"""
    global current_text
    
    # Gửi nội dung hiện tại cho client vừa kết nối
    try:
        client_socket.send(current_text.encode('utf-8'))
    except:
        pass

    while True:
        try:
            # Nhận dữ liệu từ client (tối đa 4096 bytes)
            data = client_socket.recv(4096)
            if not data:
                break
            
            # Cập nhật văn bản gốc trên server
            current_text = data.decode('utf-8')
            
            # Đồng bộ hóa (Broadcast) nội dung mới cho các client khác
            broadcast(data, client_socket)
            
        except ConnectionResetError:
            break

    # Đóng kết nối nếu client ngắt
    if client_socket in clients:
        clients.remove(client_socket)
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[*] Server đang chạy tại {HOST}:{PORT}")

    while True:
        client_sock, addr = server.accept()
        print(f"[+] Kết nối mới từ: {addr}")
        clients.append(client_sock)
        
        # Tạo luồng (Thread) riêng cho mỗi client - Kiến thức Chương 5 (Tiến trình/Luồng)
        thread = threading.Thread(target=handle_client, args=(client_sock,))
        thread.start()

if __name__ == "__main__":
    start_server()