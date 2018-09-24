"""This module groups the logic that handle each incoming client."""
import os
import time
import socket
import uuid
from multiprocessing import (
    current_process,
    Pipe,
    Process,
)
from struct import (
    pack,
    unpack,
)

from structlog import get_logger

from bluserver.calculator import calculate
from bluserver.exceptions import (
    CalculatorException,
    ServerException,
)
from bluserver.tools import (
    get_slice,
    recv,
    send,
)


logger = get_logger()


def do_calculations(pipe, data):
    """Target function used in sub-processing client calculations.

    Upon the server invoked parameters, for each client will be spawned
    N sub-processes in order to evaluate the received input, each of this
    sub-processes will use this function as the target.

    Args:
        pipe (Pipe): The pipe endpoint for the spawned sub-process running here
        data (List[Bytes]): the chuck of data to be processed

    Returns:
        array[Float]: Array with results for each one of the calculations
    """
    logger.bind(pname=current_process().name, pid=os.getpid())

    logger.info('Started sub process calculation')

    results = []

    for expression in data:
        try:
            results.append(calculate(expression.decode('ascii')))
        except CalculatorException:
            logger.error(
                'Could not compute expression',
                expression=expression.decode("ascii"))

    logger.info('Pipe calculation results to parent', items=len(results))

    try:
        # The object must be picklable. Very large pickles (approximately
        # 32 MiB+, though it depends on the OS) may raise ValueError exception.
        pipe.send(results)

    except Exception:
        logger.exception('Could not sent data to parent process')

    finally:
        pipe.close()

    logger.info('Subprocess terminated')

    return


def manage(conn, num_processes):
    """Manage each client connecting to the server.

    Each client connected to this server will be served by a sub-process which
    will have this function as the target.

    Args:
        conn (Socket): The connected socket
        num_processes (Int): Number of sub-processes that will be used to serve
            the client's input

    Returns:
        None
    """
    logger.bind(uuid=str(uuid.uuid1()), pname='manage_client', pid=os.getpid())

    logger.info('Manage client started', client=conn)

    try:
        # first message has the total size
        data_len, = unpack('>Q', recv(conn, 8))
        logger.info('Client informed data size', bytes=data_len)

        if data_len > 1024 * 1024 * 100:
            logger.error('Server can handle size inputs less than 100 MiB')
            raise ServerException

        # receive all data (list of bytearrays)
        # split takes 0.02s each 10Mib chunk
        data = recv(conn, data_len).split(b'\n')

        logger.info(
            f'{num_processes} processes will be used to parallelize computations')

        processes = []
        pipes = []
        for sl in get_slice(len(data), num_processes):
            logger.info('Data slice calculated (lines)', slice=sl)

            pipe = Pipe()
            p = Process(target=do_calculations, args=(pipe[1], data[sl]))
            logger.info('Process created', name=p.name)

            pipes.append(pipe)
            processes.append(p)

        # time
        time_start = time.time()

        for p in processes:
            p.start()
            logger.info('Process started', name=p.name)

        # close child's end pipes in this process
        for p in pipes:
            p[1].close()

        logger.info("All child's pipe endpoints were closed")

        results = bytearray()

        for pipe in pipes:
            partial_result = pipe[0].recv()
            logger.info('Received calculations from child')
            pipe[0].close()
            for r in partial_result:
                results.extend(str(r).encode('ascii') + b'\n')

        for p in processes:
            p.join()
            logger.info('Joined process', process=p)

        # time
        time_end = time.time() - time_start
        logger.info(f'Calculations done in {time_end} seconds')

        # use struct to make sure we have a consistent endianness on the length
        send(conn, pack('>Q', len(results)))
        logger.info('Client was informed about result size', bytes=len(results))

        send(conn, results)
        logger.info('Results sent to client')

    except RuntimeError:
        logger.exception('The communication with client was interrupted')

    except ConnectionError:
        logger.exception('Client closed connection prematurely')

    except EOFError:
        logger.exception('Could not receive data from children process')

    except Exception:
        logger.exception('There was an unexpected problem')

    finally:
        try:
            conn.shutdown(socket.SHUT_RDWR)
            logger.info('Client connection gracefully shutdown')
        except Exception:
            pass

        conn.close()
        logger.info('Client connection closed')

        logger.info('Manage client terminated')
