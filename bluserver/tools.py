"""This module holds network and server related functions."""

from structlog import get_logger


logger = get_logger()


# Chunk size when dealing with socket primitives
NET_BLOCK_SIZE = 4096


def send(conn, data):
    """Send a chunk of data.

    Args:
        conn (socket): connection used to send the data
        data (bytes): chunk of data to be send

    Returns:
        None

    Raises:
        RuntimeError: When trying a closed state socket

    """
    total_sent = 0
    while total_sent < len(data):
        sent = conn.send(data[total_sent:])
        if sent == 0:
            logger.exception('Socket connection broken')
            raise RuntimeError("Socket connection is broken")
        total_sent = total_sent + sent

    logger.info('Sent data to client', bytes=len(data))


def recv(conn, data_len):
    """Receive a chunk of data.

    Args:
        conn (socket): connection used to receive the data
        data_len (int): length of the data (in bytes) to be received

    Returns:
        msg (bytearray): the data received

    Raises:
        RuntimeError: When trying a closed state socket

    """
    logger.info('Starting to receive data from client', bytes=data_len)

    bytes_recd = 0
    msg = bytearray()
    while bytes_recd < data_len:
        chunk = conn.recv(min(data_len - bytes_recd, NET_BLOCK_SIZE))
        if chunk == b'':
            logger.exception('Socket connection broken')
            raise RuntimeError('Socket connection broken')
        msg.extend(chunk)
        bytes_recd = bytes_recd + len(chunk)
        logger.debug('Received data chunk', bytes=len(chunk))

    logger.info('Received data from client', bytes=bytes_recd)

    return msg


def get_slice(total_items, partitions):
    """Calculate slices based in a length and partitions.

    This function will calculate the slices (begin:end) necessarily to divide
    a chunk of items in equally partitions.

    For example:
        total_items: 20, partitions: 3
         * slice(0, 6, None)
         * slice(6, 12, None)
         * slice(12, -1, None)

    Args:
        total_items (int): the number of items
        partitions: in many partitions the items will be divided

    Returns:
        Slice: for each call returns one of the calculated slices

    """
    if partitions > total_items:
        partitions = total_items

    chunk_size = total_items // partitions

    for i in range(0, partitions - 1):
        yield slice(i*chunk_size, (i+1)*chunk_size)

    yield slice((partitions - 1) * chunk_size, -1)
