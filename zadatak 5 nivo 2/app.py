import threading
import time

from client import run_client
from load_balancer import LOAD_BALANCER_PORT, start_load_balancer
from server import SERVERS, start_server


def main():
    for server_name, config in SERVERS.items():
        start_server(server_name, config, threaded=True)

    start_load_balancer(threaded=True)
    time.sleep(1)

    print("Serveri i load balancer su pokrenuti.")
    print(f"Load balancer port: {LOAD_BALANCER_PORT}")
    print("Resurs za test: /file.dat")
    print()

    threads = [
        threading.Thread(target=run_client, args=("/file.dat",), daemon=True)
        for _ in range(4)
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
