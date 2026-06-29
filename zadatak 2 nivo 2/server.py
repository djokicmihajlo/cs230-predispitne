import socket
import threading


HOST = "127.0.0.1"
SERVER_PORTS = (5001, 5002)
BUFFER_SIZE = 1024


def handle_client(client_socket, client_address, port):
    with client_socket:
        client_socket.recv(BUFFER_SIZE)
        response = f"You have reacher server with port number {port}"
        client_socket.sendall(response.encode("utf-8"))
        print(f"Server {port}: odgovor poslat klijentu {client_address}.")


def run_server(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, port))
        server_socket.listen()
        print(f"Server pokrenut na {HOST}:{port}")

        while True:
            client_socket, client_address = server_socket.accept()
            thread = threading.Thread(
                target=handle_client,
                args=(client_socket, client_address, port),
                daemon=True,
            )
            thread.start()


def start_server(port, threaded=False):
    if threaded:
        thread = threading.Thread(target=run_server, args=(port,), daemon=True)
        thread.start()
        return thread

    run_server(port)


if __name__ == "__main__":
    for server_port in SERVER_PORTS:
        start_server(server_port, threaded=True)

    print("Serveri su pokrenuti. Pritisnite Ctrl+C za prekid.")
    threading.Event().wait()
