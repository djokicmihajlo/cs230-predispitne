import time

from client import run_client
from middleware import MIDDLEWARE_PORT, start_middleware
from server import SERVER_PORT, start_server


def main():
    start_server(threaded=True)
    start_middleware(threaded=True)
    time.sleep(1)

    print("Server i middleware su pokrenuti.")
    print(f"Server port: {SERVER_PORT}")
    print(f"Middleware port: {MIDDLEWARE_PORT}")
    print()

    run_client("normalan zahtev")
    run_client("spor zahtev")


if __name__ == "__main__":
    main()
