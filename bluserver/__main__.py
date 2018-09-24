# -*- coding: utf-8 -*-

"""Main module."""
import os

from structlog import get_logger

from bluserver import initialize_logging
from bluserver.cli import get_arg_parser
from bluserver.exceptions import ServerBaseException
from bluserver.server import run_server


logger = get_logger('bluserver')


def main():
    """Main entry point for this project."""
    cli_parser = get_arg_parser()
    cli_args = cli_parser.parse_args()

    initialize_logging(verbose=cli_args.verbose)

    logger.bind(pname="server", pid=os.getpid())

    logger.info("Blu Server invoked", cli_args=cli_args)

    output = {
        "status": None,
        "reason": None,
    }

    try:
        logger.info("Cli arguments parse")

        # arguments
        address = cli_args.address
        port = int(cli_args.port)
        num_processes = int(cli_args.number_processes)

        # run the server
        run_server(address, port, num_processes)

        output["status"] = "TERMINATED"
        output["reason"] = "Server gracefully terminated"

    except ServerBaseException as err:
        output["status"] = "FAILED"
        output["reason"] = str(err)

    except Exception as err:
        logger.exception("Unexpected error")
        output["status"] = "CRASHED"
        output["reason"] = str(err)

    logger.info(output=output)


if __name__ == "__main__":
    main()
