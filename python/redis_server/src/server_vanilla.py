"""
Vanilla server implementation.
"""

import socket
import logging


from utils import parse_arguments
from resp import RespDecoder

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("server_vanilla.log"), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)
# logging.basicConfig(filename="server.log", encoding="utf-8", level=logging.INFO)


def handle_redis_client(client):
    with client:
        while True:
            data = client.recv(1024)
            if not data:
                break
            logging.info(f"DATA: {data}")
            logger.info(f"Parser output: {RespDecoder(data).parse()}")
            client.sendall(b"+PONG\r\n")


def main():
    args = parse_arguments()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        logging.info(f"Initializing server at {args.host}:{args.port}")
        server.bind((args.host, args.port))
        server.listen()
        while True:
            client, address = server.accept()
            logging.info(f"Connected by {address}")
            handle_redis_client(client)


if __name__ == "__main__":
    main()
