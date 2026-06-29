import socket
import threading

from server import BUFFER_SIZE, HOST, SERVER_PORTS


LOAD_BALANCER_PORT = 5000


def choose_redirect_port(selected_port):
    if selected_port not in SERVER_PORTS:
        raise ValueError("Nepoznat port servera.")

    return SERVER_PORTS[1] if selected_port == SERVER_PORTS[0] else SERVER_PORTS[0]


def handle_client(client_socket, client_address):
    with client_socket:
        selected_port_data = client_socket.recv(BUFFER_SIZE).decode("utf-8").strip()
        selected_port = int(selected_port_data)
        redirect_port = choose_redirect_port(selected_port)

        print(
            "Load balancer: klijent "
            f"{client_address} je izabrao {selected_port}, "
            f"preusmerava se na {redirect_port}."
        )

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.connect((HOST, redirect_port))
            server_socket.sendall(f"Redirected from {selected_port}".encode("utf-8"))
            response = server_socket.recv(BUFFER_SIZE)

        client_socket.sendall(response)


def run_load_balancer():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as balancer_socket:
        balancer_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        balancer_socket.bind((HOST, LOAD_BALANCER_PORT))
        balancer_socket.listen()
        print(f"Load balancer pokrenut na {HOST}:{LOAD_BALANCER_PORT}")

        while True:
            client_socket, client_address = balancer_socket.accept()
            thread = threading.Thread(
                target=handle_client,
                args=(client_socket, client_address),
                daemon=True,
            )
            thread.start()


def start_load_balancer(threaded=False):
    if threaded:
        thread = threading.Thread(target=run_load_balancer, daemon=True)
        thread.start()
        return thread

    run_load_balancer()


if __name__ == "__main__":
    run_load_balancer()
