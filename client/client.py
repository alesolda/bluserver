"""Tiny & simple client for bluserver."""

import os
import socket
from struct import pack, unpack

from structlog import get_logger

from tools import (
    recv,
    send,
)


logger = get_logger()


INPUT_FILE = './operations.txt'
OUTPUT_FILE = './output.txt'
CHUNK_SIZE = 1024 * 1024  # 1 MiB
ADDRESS = ('localhost', 1982)


def get_file_chunk():
    with open(INPUT_FILE, 'rb') as fb:
        while True:
            data = fb.read(CHUNK_SIZE)
            if not data:
                raise StopIteration
            yield data


def get_file_size():
    stat_info = os.stat(INPUT_FILE)
    return stat_info.st_size


if __name__ == '__main__':
    logger.info('Starting tiny client')

    # socket initialization
    server_address = ADDRESS
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)

    # send file size
    # use struct to mak e sure we have a consistent endianness on the length
    send(sock, pack('>Q', get_file_size()))

    # send data
    for data in get_file_chunk():
        send(sock, data)

    sock.shutdown(socket.SHUT_WR)
    logger.info('All data was sent, socket was switched to read-only')

    # recv data
    # first message has the total size
    data_len, = unpack('>Q', recv(sock, 8))

    # receive all data
    data = recv(sock, data_len)
    logger.info(f'Received {data_len} bytes')

    with open(OUTPUT_FILE, 'wb') as output_file:
        output_file.write(data)

    sock.close()
    logger.info('Connection was closed')

    logger.info('End Tiny Client')
