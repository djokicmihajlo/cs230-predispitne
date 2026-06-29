import time

from client import run_client
from middleware import MIDDLEWARE_PORT, start_middleware
from server import SERVER_PORT


def main():
    start_middleware(threaded=True)
    time.sleep(1)

    print("Middleware je pokrenut.")
    print(f"Middleware port: {MIDDLEWARE_PORT}")
    print(f"Server port koji se proverava: {SERVER_PORT}")
    print("Server namerno nije pokrenut u ovoj demonstraciji.")
    print()

    run_client("GET /data")


if __name__ == "__main__":
    main()
