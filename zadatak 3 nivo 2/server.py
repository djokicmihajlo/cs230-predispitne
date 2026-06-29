import socket
import threading


HOST = "127.0.0.1"
SERVER_PORT = 6001
BUFFER_SIZE = 1024


def handle_client(client_socket, client_address):
    with client_socket:
        request = client_socket.recv(BUFFER_SIZE).decode("utf-8")
        print(f"Server: primljen zahtev od {client_address}: {request}")
        response = f"Server je obradio zahtev: {request}"
        client_socket.sendall(response.encode("utf-8"))


def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, SERVER_PORT))
        server_socket.listen()
        print(f"Server pokrenut na {HOST}:{SERVER_PORT}")

        while True:
            client_socket, client_address = server_socket.accept()
            thread = threading.Thread(
                target=handle_client,
                args=(client_socket, client_address),
                daemon=True,
            )
            thread.start()


if __name__ == "__main__":
    run_server()
