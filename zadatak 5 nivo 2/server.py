import socket
import threading
import time
from pathlib import Path


HOST = "127.0.0.1"
BUFFER_SIZE = 4096
BASE_DIR = Path(__file__).resolve().parent

SERVERS = {
    "server1": {
        "port": 7301,
        "root": BASE_DIR / "server1" / "resources",
    },
    "server2": {
        "port": 7302,
        "root": BASE_DIR / "server2" / "resources",
    },
}


def safe_resource_path(root, resource_path):
    relative_path = resource_path.strip().lstrip("/")
    resolved = (root / relative_path).resolve()
    root_resolved = root.resolve()

    if resolved != root_resolved and root_resolved not in resolved.parents:
        raise ValueError("Zahtevana putanja nije dozvoljena.")

    return resolved


def handle_client(client_socket, client_address, server_name, root):
    with client_socket:
        resource_path = client_socket.recv(BUFFER_SIZE).decode("utf-8").strip()
        print(f"{server_name}: primljen zahtev od {client_address}: {resource_path}")

        try:
            file_path = safe_resource_path(root, resource_path)
            if not file_path.is_file():
                response = f"NOT_FOUND|{server_name}|Resurs ne postoji."
            else:
                time.sleep(1)
                content = file_path.read_text(encoding="utf-8")
                response = f"FOUND|{server_name}|{content}"
        except (OSError, ValueError) as error:
            response = f"ERROR|{server_name}|{error}"

        client_socket.sendall(response.encode("utf-8"))


def run_server(server_name, config):
    port = config["port"]
    root = config["root"]

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, port))
        server_socket.listen()
        print(f"{server_name} pokrenut na {HOST}:{port}")

        while True:
            client_socket, client_address = server_socket.accept()
            thread = threading.Thread(
                target=handle_client,
                args=(client_socket, client_address, server_name, root),
                daemon=True,
            )
            thread.start()


def start_server(server_name, config, threaded=False):
    if threaded:
        thread = threading.Thread(
            target=run_server,
            args=(server_name, config),
            daemon=True,
        )
        thread.start()
        return thread

    run_server(server_name, config)


if __name__ == "__main__":
    for name, server_config in SERVERS.items():
        start_server(name, server_config, threaded=True)

    print("Serveri su pokrenuti. Pritisnite Ctrl+C za prekid.")
    threading.Event().wait()
