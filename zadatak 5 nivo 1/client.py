import socket

from middleware import MIDDLEWARE_PORT
from server import BUFFER_SIZE, HOST


def run_client(request):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, MIDDLEWARE_PORT))
        client_socket.sendall(request.encode("utf-8"))
        response = client_socket.recv(BUFFER_SIZE).decode("utf-8")

    print(f"Klijent: zahtev={request}")
    print(f"Klijent: odgovor={response}")
    print()
    return response


if __name__ == "__main__":
    run_client("normalan zahtev")
