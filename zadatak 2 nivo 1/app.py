import argparse
import socket
import time


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 5000
DEFAULT_INTERVAL_SECONDS = 5
STARTING_SENDS = 10


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="TCP klijent koji salje OOB timeout upozorenja serveru."
    )
    parser.add_argument(
        "--host",
        default=DEFAULT_HOST,
        help=f"Adresa servera. Podrazumevano: {DEFAULT_HOST}",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help=f"Port servera. Podrazumevano: {DEFAULT_PORT}",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=DEFAULT_INTERVAL_SECONDS,
        help=f"Pauza izmedju OOB poruka u sekundama. Podrazumevano: {DEFAULT_INTERVAL_SECONDS}",
    )
    return parser.parse_args()


def send_oob_warnings(host, port, interval):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        print(f"Povezivanje sa serverom {host}:{port}...")
        client_socket.connect((host, port))
        print("Veza je uspostavljena.")

        for sends_remaining in range(STARTING_SENDS, -1, -1):
            message = f"{sends_remaining} sends remaining..."
            client_socket.send(message.encode("utf-8"), socket.MSG_OOB)
            print(f"Poslato OOB upozorenje: {message}")

            if sends_remaining > 0:
                time.sleep(interval)

        print("Odbrojavanje je zavrseno. Klijent raskida vezu.")


def main():
    args = parse_arguments()
    send_oob_warnings(args.host, args.port, args.interval)


if __name__ == "__main__":
    main()
