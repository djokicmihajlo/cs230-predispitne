import time

from server1 import run_server1
from server2 import SERVER2_PORT, start_server2


def main():
    start_server2(threaded=True)
    time.sleep(1)

    print("Server2 je pokrenut i ceka vezu.")
    print(f"Server2 port: {SERVER2_PORT}")
    print()

    run_server1()


if __name__ == "__main__":
    main()
