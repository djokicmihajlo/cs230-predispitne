import time

from client import run_client
from middleware import MIDDLEWARE_PORT, start_middleware
from storage_server import STORAGE_SERVERS, start_storage_server


def main():
    for server_name, config in STORAGE_SERVERS.items():
        start_storage_server(server_name, config, threaded=True)

    start_middleware(threaded=True)
    time.sleep(1)

    print("Distribuirani fajl sistem je pokrenut.")
    print(f"Middleware port: {MIDDLEWARE_PORT}")
    print("Primeri zahteva:")
    print("- /server1/data/projects/spec.dat")
    print("- /server2/data/reports/january.csv")
    print("- /server2/data/reports/missing.csv")
    print()

    run_client("/server1/data/projects/spec.dat")
    run_client("/server2/data/reports/missing.csv")


if __name__ == "__main__":
    main()
