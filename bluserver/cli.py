"""Definition of the cli argument parser."""
import argparse


def get_arg_parser():
    """Initialize argument parser."""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-a',
        '--address',
        help="The ip address in which this server will run.",
        metavar="address",
        default="localhost",
        required=False
    )

    parser.add_argument(
        '-p',
        '--port',
        help="The port in which this server will run.",
        metavar="port",
        default="1982",
        required=False
    )

    parser.add_argument(
        '-n',
        '--number-processes',
        help="The number of sub processes this server will use to process for each incoming client.",
        metavar="number_processes",
        default="2",
        required=False
    )

    parser.add_argument(
        '-v',
        '--verbose',
        help="Adds stdout as an additional output for logging.",
        action='store_true'
    )

    return parser
