import socket
import threading

from server import BUFFER_SIZE, HOST, SERVERS


LOAD_BALANCER_PORT = 7300

active_requests = {server_name: 0 for server_name in SERVERS}
active_requests_lock = threading.Lock()


def choose_least_loaded_server():
    with active_requests_lock:
        server_name = min(active_requests, key=active_requests.get)
        active_requests[server_name] += 1
        snapshot = dict(active_requests)

    print(f"Load balancer: izabran {server_name}; aktivni zahtevi: {snapshot}")
    return server_name


def release_server(server_name):
    with active_requests_lock:
        active_requests[server_name] -= 1


def forward_to_server(server_name, resource_path):
    port = SERVERS[server_name]["port"]

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.connect((HOST, port))
        server_socket.sendall(resource_path.encode("utf-8"))
        return server_socket.recv(BUFFER_SIZE).decode("utf-8")


def handle_client(client_socket, client_address):
    with client_socket:
        resource_path = client_socket.recv(BUFFER_SIZE).decode("utf-8").strip()
        print(f"Load balancer: klijent {client_address} trazi {resource_path}")

        server_name = choose_least_loaded_server()
        try:
            response = forward_to_server(server_name, resource_path)
        finally:
            release_server(server_name)

        client_socket.sendall(response.encode("utf-8"))


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
