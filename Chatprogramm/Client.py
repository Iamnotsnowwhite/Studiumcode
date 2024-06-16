import socket

def start_client(host='127.0.0.1', port=65432):#用于启动客户端并连接到服务器
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print("Connected to the server.")
        
        while True:
            message = input("You: ")
            if message.lower() == 'exit':
                break
            s.sendall(message.encode())
            data = s.recv(1024)
            print(f"Server: {data.decode()}")

if __name__ == "__main__":
    start_client()
