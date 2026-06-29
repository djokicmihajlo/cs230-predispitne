import socket
import threading
from pathlib import Path


HOST = "127.0.0.1"
BUFFER_SIZE = 4096
BASE_DIR = Path(__file__).resolve().parent

STORAGE_SERVERS = {
    "server1": {
        "port": 7101,
        "root": BASE_DIR / "server1",
    },
    "server2": {
        "port": 7102,
        "root": BASE_DIR / "server2",
    },
}


def resolve_safe_path(root, virtual_path):
    relative_path = virtual_path.lstrip("/")
    if relative_path.startswith(root.name + "/"):
        relative_path = relative_path[len(root.name) + 1 :]

    resolved = (root / relative_path).resolve()
    root_resolved = root.resolve()

    if root_resolved != resolved and root_resolved not in resolved.parents:
        raise ValueError("Putanja izlazi iz root direktorijuma servera.")

    return resolved


def handle_client(client_socket, client_address, server_name, root):
    with client_socket:
        requested_path = client_socket.recv(BUFFER_SIZE).decode("utf-8").strip()
        print(f"{server_name}: primljen zahtev od {client_address}: {requested_path}")

        try:
            file_path = resolve_safe_path(root, requested_path)
            if file_path.is_file():
                response = f"FOUND|{server_name}|{file_path.read_text(encoding='utf-8')}"
            else:
                response = f"NOT_FOUND|{server_name}|Fajl nije pronadjen na serveru."
        except OSError as error:
            response = f"ERROR|{server_name}|{error}"

        client_socket.sendall(response.encode("utf-8"))


def run_storage_server(server_name, config):
    port = config["port"]
    root = config["root"]

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, port))
        server_socket.listen()
        print(f"{server_name} pokrenut na {HOST}:{port}, root={root}")

        while True:
            client_socket, client_address = server_socket.accept()
            thread = threading.Thread(
                target=handle_client,
                args=(client_socket, client_address, server_name, root),
                daemon=True,
            )
            thread.start()


def start_storage_server(server_name, config, threaded=False):
    if threaded:
        thread = threading.Thread(
            target=run_storage_server,
            args=(server_name, config),
            daemon=True,
        )
        thread.start()
        return thread

    run_storage_server(server_name, config)


if __name__ == "__main__":
    for name, server_config in STORAGE_SERVERS.items():
        start_storage_server(name, server_config, threaded=True)

    print("Storage serveri su pokrenuti. Pritisnite Ctrl+C za prekid.")
    threading.Event().wait()
