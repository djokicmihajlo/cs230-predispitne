import socket
import threading
from datetime import datetime
from pathlib import Path

from server import BUFFER_SIZE, HOST, SERVER_PORT


MIDDLEWARE_PORT = 6000
TIMEOUT_SECONDS = 3
FAILED_REQUESTS_LOG = Path(__file__).with_name("failed_requests.log")
UNAVAILABLE_MESSAGE = "Server trenutno nije dostupan, zahtev je zapamćen."


def log_failed_request(request, reason):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(FAILED_REQUESTS_LOG, "a", encoding="utf-8") as log_file:
        log_file.write(f"[{timestamp}] reason={reason}; request={request}\n")


def forward_to_server(request):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.settimeout(TIMEOUT_SECONDS)
        server_socket.connect((HOST, SERVER_PORT))
        server_socket.sendall(request.encode("utf-8"))
        return server_socket.recv(BUFFER_SIZE).decode("utf-8")


def handle_client(client_socket, client_address):
    with client_socket:
        request = client_socket.recv(BUFFER_SIZE).decode("utf-8")
        print(f"Middleware: primljen zahtev od {client_address}: {request}")

        try:
            response = forward_to_server(request)
        except (ConnectionRefusedError, TimeoutError, socket.timeout, OSError) as error:
            log_failed_request(request, type(error).__name__)
            response = UNAVAILABLE_MESSAGE

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
