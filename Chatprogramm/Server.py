import socket
import threading # 并发处理多个客户端链接
import random

nouns = ["cat", "dog", "man", "woman", "car", "bicycle", "tree", "house"]
verbs = ["jumps", "runs", "drives", "flies", "eats", "sleeps", "walks"]
adjectives = ["big", "small", "red", "blue", "fast", "slow", "bright", "dark"]
adverbs = ["quickly", "slowly", "gracefully", "awkwardly", "happily", "sadly"]
prepositions = ["on", "in", "under", "over", "beside", "with", "without"]

def generate_sentence():
    noun1 = random.choice(nouns)
    noun2 = random.choice(nouns)
    verb = random.choice(verbs)
    adjective = random.choice(adjectives)
    adverb = random.choice(adverbs)
    preposition = random.choice(prepositions)
    
    sentence = f"The {adjective} {noun1} {verb} {adverb} {preposition} the {noun2}."
    return sentence

def handle_client(client_socket):# 处理每个客户端的链接的函数
    with client_socket:
        print(f"Connected by {client_socket.getpeername()}")
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            response = generate_sentence()
            client_socket.sendall(response.encode())
        print(f"Connection closed by {client_socket.getpeername()}")

def start_server(host='127.0.0.1', port=65432):#创建并启动服务器。
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: #创建 TCP/IP 套接字
        s.bind((host, port)) #链接
        s.listen() #监听
        print(f"Server listening on {host}:{port}")
        
        
        while True:
            conn, addr = s.accept()
            client_handler = threading.Thread(target=handle_client, args=(conn,))
            client_handler.start()

if __name__ == "__main__":
    start_server()
