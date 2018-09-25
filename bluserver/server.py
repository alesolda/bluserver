"""This module holds the main logic for the server."""

import selectors
import signal
import socket
import multiprocessing as mp

from structlog import get_logger

from bluserver.exceptions import ServerException
from bluserver.client_manager import manage


logger = get_logger()


keep_running = True


def signal_handler(signum, frame):
    """Custom handler to be executed when a signal is received.

    Args:
        signum: signal number
        frame: current stack frame

    Returns:
        None

    """
    global keep_running

    if signum in (signal.SIGINT, signal.SIGTERM):
        logger.info('Trying to do a gracefully server shutdown', signal=signum)
        keep_running = False


def run_server(address, port, num_processes):
    """Run the server.

    Main entry point to run this server. Executes the server in a continuous
    loop until a signal indicating its termination is received (SIGINT or
    SIGTERM)

    Args:
        address (str): ip address or localhost
        port (int): port in which this server will listen
        num_processes: number of processed used to process each client input

    Returns:
        None

    """
    logger.info('Start server')

    try:
        # trap SIGINT/CTR-C or SIGTERM signals
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        # prepare socket to accept incoming connections
        sock = socket.socket()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((address, port))
        sock.listen(100)
        sock.setblocking(False)

        # listen when some incoming connection is received
        # this technique needs a non-blocking listening socket
        selector = selectors.DefaultSelector()
        selector.register(sock, selectors.EVENT_READ)

        # this list holds all processes created to manage
        # each incoming connection
        processes = []

        while keep_running:
            # Return list of all live children of the current process.
            # Calling this has the side effect of “joining” any processes
            # which have already finished.
            mp.active_children()

            for key, mask in selector.select(timeout=1):

                if mask & selectors.EVENT_READ:
                    sock = key.fileobj

                    conn, addr = sock.accept()  # Should be ready
                    logger.info('Incoming connection', conn=conn, addr=addr)

                    p = mp.Process(target=manage, args=(conn, num_processes))
                    logger.info(
                        'Forked process for incoming connection', process=p.name)

                    processes.append(p)
                    p.start()

                else:
                    logger.error('Server main loop received an unexpected selector')
                    raise RuntimeError()

        # keep_running == False
        else:
            # join all processes
            logger.info('Trying to finalize gracefully all children')
            for p in processes:
                p.join(5)
                if not p.is_alive():
                    continue
                logger.info('Terminating unresponsive child', pid=p.pid, pname=p.name)
                p.terminate()

            logger.info('Server stopped')

    except OSError:
        logger.exception('There was a problem initializing the listening socket')
        raise ServerException

    except RuntimeError:
        logger.exception('An unregistered event was caught by the main loop')
        raise ServerException

    except Exception:
        logger.exception('There was an unexpected problem')
        raise ServerException
