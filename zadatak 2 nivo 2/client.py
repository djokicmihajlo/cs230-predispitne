import random
import socket

from load_balancer import LOAD_BALANCER_PORT
from server import BUFFER_SIZE, HOST, SERVER_PORTS


def run_client():
    selected_port = random.choice(SERVER_PORTS)
    print(f"Klijent: nasumicno izabran server sa portom {selected_port}.")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, LOAD_BALANCER_PORT))
        client_socket.sendall(str(selected_port).encode("utf-8"))
        response = client_socket.recv(BUFFER_SIZE).decode("utf-8")

    print(f"Klijent: odgovor servera: {response}")
    return response


if __name__ == "__main__":
    run_client()
