import socket
import threading
import json

HOST = '127.0.0.1'
PORT = 65432

# --- CẤU HÌNH GLOBAL ---
clients = {} # {socket: name}
current_text = ""
lock = threading.Lock()

def save_to_file():
    with lock:
        try:
            with open("shared_doc.txt", "w", encoding="utf-8") as f:
                f.write(current_text)
        except Exception as e:
            print(f"[!] Lỗi ghi file: {e}")

def load_from_file():
    global current_text
    try:
        with open("shared_doc.txt", "r", encoding="utf-8") as f:
            current_text = f.read()
            print("[*] Đã khôi phục dữ liệu từ file.")
    except FileNotFoundError:
        current_text = ""

def send_json(sock, data_dict):
    """Hàm hỗ trợ gửi JSON kèm ký tự xuống dòng"""
    try:
        # QUAN TRỌNG: Thêm \n vào cuối để client biết đâu là kết thúc gói tin
        json_str = json.dumps(data_dict) + "\n"
        sock.sendall(json_str.encode('utf-8'))
    except (ConnectionResetError, BrokenPipeError):
        pass

def broadcast(message_dict, sender_socket=None):
    with lock:
        all_sockets = list(clients.keys())
        
    for client_sock in all_sockets:
        if client_sock != sender_socket:
            send_json(client_sock, message_dict)

def remove_client(client_socket):
    with lock:
        if client_socket in clients:
            name = clients[client_socket]
            del clients[client_socket]
            client_socket.close()
            print(f"[-] {name} đã thoát.")
            return name
    return None

def handle_client(client_socket):
    global current_text
    name = "Unknown"
    buffer = "" # Bộ đệm riêng cho mỗi client để xử lý dính gói tin
    
    try:
        # 1. Handshake
        name = client_socket.recv(1024).decode('utf-8')
        with lock:
            clients[client_socket] = name
        
        print(f"[+] {name} đã kết nối.")
        broadcast({"type": "notification", "content": f"🔵 {name} đã tham gia!"}, client_socket)
        
        # Gửi dữ liệu hiện tại
        with lock:
            msg = {"type": "full_text", "content": current_text}
        send_json(client_socket, msg)

        # 2. Vòng lặp nhận tin (Xử lý Stream)
        while True:
            data = client_socket.recv(4096)
            if not data: break
            
            buffer += data.decode('utf-8')
            
            # Xử lý cắt dòng lệnh \n
            while "\n" in buffer:
                message, buffer = buffer.split("\n", 1)
                if not message.strip(): continue
                
                try:
                    request = json.loads(message)
                    if request['type'] == 'update_text':
                        with lock:
                            current_text = request['content']
                        save_to_file()
                        broadcast({"type": "update_text", "content": request['content']}, client_socket)
                except json.JSONDecodeError:
                    continue

    except Exception as e:
        print(f"[!] Lỗi kết nối {name}: {e}")
    finally:
        removed_name = remove_client(client_socket)
        if removed_name:
            broadcast({"type": "notification", "content": f"🔴 {removed_name} đã rời đi."})

def start_server():
    load_from_file()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[*] Server V3.0 (Line-Delimited) chạy tại {HOST}:{PORT}")

    while True:
        client_sock, addr = server.accept()
        threading.Thread(target=handle_client, args=(client_sock,), daemon=True).start()

if __name__ == "__main__":
    start_server()