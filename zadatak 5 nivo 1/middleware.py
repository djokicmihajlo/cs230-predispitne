import functools
import queue
import socket
import threading

from server import BUFFER_SIZE, HOST, SERVER_PORT


MIDDLEWARE_PORT = 7200
TIMEOUT_SECONDS = 2
TIMEOUT_MESSAGE = "Vreme čekanja isteklo"


def timeout_after(seconds):
    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            result_queue = queue.Queue(maxsize=1)

            def target():
                try:
                    result_queue.put((True, function(*args, **kwargs)))
                except Exception as error:
                    result_queue.put((False, error))

            thread = threading.Thread(target=target, daemon=True)
            thread.start()
            thread.join(seconds)

            if thread.is_alive():
                raise TimeoutError

            success, result = result_queue.get()
            if success:
                return result

            raise result

        return wrapper

    return decorator


@timeout_after(TIMEOUT_SECONDS)
def forward_request_to_server(request):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.connect((HOST, SERVER_PORT))
        server_socket.sendall(request.encode("utf-8"))
        return server_socket.recv(BUFFER_SIZE).decode("utf-8")


def handle_client(client_socket, client_address):
    with client_socket:
        request = client_socket.recv(BUFFER_SIZE).decode("utf-8")
        print(f"Middleware: primljen zahtev od {client_address}: {request}")

        try:
            response = forward_request_to_server(request)
        except TimeoutError:
            response = TIMEOUT_MESSAGE

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
