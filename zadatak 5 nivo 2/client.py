import socket

from load_balancer import LOAD_BALANCER_PORT
from server import BUFFER_SIZE, HOST


def run_client(resource_path):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, LOAD_BALANCER_PORT))
        client_socket.sendall(resource_path.encode("utf-8"))
        response = client_socket.recv(BUFFER_SIZE).decode("utf-8")

    print(f"Klijent: zahtev={resource_path}")
    print(f"Klijent: odgovor={response}")
    print()
    return response


if __name__ == "__main__":
    run_client("/file.dat")
