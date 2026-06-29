import socket
from collections import Counter
from pathlib import Path

from server2 import BUFFER_SIZE, HOST, SERVER2_PORT


BASE_DIR = Path(__file__).resolve().parent
SERVER1_DATA_FILE = BASE_DIR / "server1" / "data.txt"
SERVER2_DATA_FILE = BASE_DIR / "server2" / "data.txt"


def read_lines(file_path):
    return file_path.read_text(encoding="utf-8").splitlines()


def find_missing_lines(server1_lines, server2_lines):
    available_on_server2 = Counter(server2_lines)
    missing_lines = []

    for line_number, line in enumerate(server1_lines, start=1):
        if available_on_server2[line] > 0:
            available_on_server2[line] -= 1
        else:
            missing_lines.append((line_number, line))

    return missing_lines


def wait_for_server2_ready():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server1_socket:
        server1_socket.connect((HOST, SERVER2_PORT))
        message = server1_socket.recv(BUFFER_SIZE).decode("utf-8")
        print(f"Server1: primljena potvrda od Server2: {message}")


def run_server1():
    wait_for_server2_ready()

    server1_lines = read_lines(SERVER1_DATA_FILE)
    server2_lines = read_lines(SERVER2_DATA_FILE)
    missing_lines = find_missing_lines(server1_lines, server2_lines)

    print()
    print("Server1: redovi koje Server2 nema i koje bi trebalo poslati:")

    if not missing_lines:
        print("Server2 vec ima sve redove iz Server1 fajla.")
        return

    for line_number, line in missing_lines:
        print(f"- red {line_number}: {line}")


if __name__ == "__main__":
    run_server1()
