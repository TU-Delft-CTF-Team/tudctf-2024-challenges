import socket

with open('flag', 'r') as file:
    flag = file.read()

def main():
    host = '127.0.0.1'
    port = 80
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print("Server is listening on port", port)

    while True:
        client_socket, client_address = server_socket.accept()
        print("Connection from", client_address)
        client_socket.send(flag.encode('utf-8'))
        client_socket.close()

if __name__ == "__main__":
    main()
