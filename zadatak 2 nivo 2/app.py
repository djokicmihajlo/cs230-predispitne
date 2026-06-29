import time

from client import run_client
from load_balancer import LOAD_BALANCER_PORT, start_load_balancer
from server import SERVER_PORTS, start_server


def main():
    for port in SERVER_PORTS:
        start_server(port, threaded=True)

    start_load_balancer(threaded=True)
    time.sleep(1)

    print("Simulacija klastera je pokrenuta.")
    print(f"Serveri rade na portovima: {SERVER_PORTS[0]} i {SERVER_PORTS[1]}")
    print(f"Load balancer radi na portu: {LOAD_BALANCER_PORT}")
    print()

    run_client()


if __name__ == "__main__":
    main()
