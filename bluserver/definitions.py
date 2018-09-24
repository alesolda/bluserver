"""Path and global configuration variables for the whole project."""

from os.path import (
    abspath,
    dirname,
    join,
)

# Project global directories and files

PROJECT_ROOT = dirname(abspath(__file__))
LOGGING_CONFIG = join(PROJECT_ROOT, 'logging.yml')
