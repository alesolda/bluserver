# -*- coding: utf-8 -*-

"""Top-level package for Blu Server ."""
from logging import config as logging_config

import structlog
import yaml

from bluserver.definitions import LOGGING_CONFIG

__author__ = """Alejandro Solda"""
__email__ = 'alejandrosolda at g m a i l dot c o m'
__version__ = '0.0.1'


def initialize_logging(verbose=False):
    """Initialize the loggers from the YAML configuration."""
    structlog.configure(
        processors=[
            structlog.processors.KeyValueRenderer(
                key_order=['uuid', 'pname', 'pid', 'event'],
            ),
        ],
        context_class=structlog.threadlocal.wrap_dict(dict),
        logger_factory=structlog.stdlib.LoggerFactory(),
    )

    with open(LOGGING_CONFIG) as infile:
        config = yaml.load(infile)
        if verbose:
            # Requires that there is a stdout handler defined at
            # logger configuration
            config['root']['handlers'].append('stdout')

        logging_config.dictConfig(config)
