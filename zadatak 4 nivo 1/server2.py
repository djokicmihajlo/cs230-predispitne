import socket
import threading


HOST = "127.0.0.1"
SERVER2_PORT = 7002
BUFFER_SIZE = 1024
READY_MESSAGE = "Server2 je spreman za replikaciju."


def handle_connection(client_socket, client_address):
    with client_socket:
        print(f"Server2: povezan je Server1 sa adrese {client_address}.")
        client_socket.sendall(READY_MESSAGE.encode("utf-8"))


def run_server2():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, SERVER2_PORT))
        server_socket.listen()
        print(f"Server2 pokrenut na {HOST}:{SERVER2_PORT}")

        while True:
            client_socket, client_address = server_socket.accept()
            thread = threading.Thread(
                target=handle_connection,
                args=(client_socket, client_address),
                daemon=True,
            )
            thread.start()


def start_server2(threaded=False):
    if threaded:
        thread = threading.Thread(target=run_server2, daemon=True)
        thread.start()
        return thread

    run_server2()


if __name__ == "__main__":
    run_server2()
