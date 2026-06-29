import socket
import threading
from pathlib import Path

from storage_server import BUFFER_SIZE, HOST, STORAGE_SERVERS


MIDDLEWARE_PORT = 7100


def normalize_request_path(request_path):
    cleaned = request_path.strip()
    if not cleaned.startswith("/"):
        cleaned = "/" + cleaned
    return cleaned


def local_path_for_server(server_name, request_path):
    server_root = STORAGE_SERVERS[server_name]["root"]
    relative = request_path.lstrip("/")

    if relative.startswith(server_name + "/"):
        relative = relative[len(server_name) + 1 :]

    return server_root / relative


def find_server_that_contains_file(request_path):
    first_part = request_path.strip("/").split("/", 1)[0]

    if first_part in STORAGE_SERVERS:
        local_path = local_path_for_server(first_part, request_path)
        if local_path.is_file():
            return first_part
        return None

    for server_name in STORAGE_SERVERS:
        local_path = local_path_for_server(server_name, request_path)
        if local_path.is_file():
            return server_name

    return None


def nearest_existing_path(request_path):
    candidates = []

    for server_name, config in STORAGE_SERVERS.items():
        parts = request_path.strip("/").split("/")
        if parts and parts[0] == server_name:
            parts = parts[1:]

        current = config["root"]
        virtual_parts = [server_name]
        best = f"/{server_name}"

        for part in parts:
            current = current / part
            virtual_parts.append(part)
            if current.exists():
                best = "/" + "/".join(virtual_parts)
            else:
                break

        candidates.append(best)

    return max(candidates, key=lambda path: len(Path(path).parts))


def forward_to_storage_server(server_name, request_path):
    port = STORAGE_SERVERS[server_name]["port"]

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.connect((HOST, port))
        server_socket.sendall(request_path.encode("utf-8"))
        return server_socket.recv(BUFFER_SIZE).decode("utf-8")


def handle_client(client_socket, client_address):
    with client_socket:
        request_path = normalize_request_path(
            client_socket.recv(BUFFER_SIZE).decode("utf-8")
        )
        print(f"Middleware: klijent {client_address} trazi {request_path}")

        server_name = find_server_that_contains_file(request_path)

        if server_name is None:
            closest_path = nearest_existing_path(request_path)
            response = f"Fajl ne postoji. Najbliza postojeca putanja je: {closest_path}"
        else:
            response = forward_to_storage_server(server_name, request_path)

        client_socket.sendall(response.encode("utf-8"))


def run_middleware():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as middleware_socket:
        middleware_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        middleware_socket.bind((HOST, MIDDLEWARE_PORT))
        middleware_socket.listen()
        print(f"Middleware pokrenut na {HOST}:{MIDDLEWARE_PORT}")

        while True:
            client_socket, client_address = middleware_socket.accept()
            thread = threading.Thread(
                target=handle_client,
                args=(client_socket, client_address),
                daemon=True,
            )
            thread.start()


def start_middleware(threaded=False):
    if threaded:
        thread = threading.Thread(target=run_middleware, daemon=True)
        thread.start()
        return thread

    run_middleware()


if __name__ == "__main__":
    run_middleware()
