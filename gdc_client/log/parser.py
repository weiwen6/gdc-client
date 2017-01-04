import argparse
import log
import logging
import sys

from .. import version

from .log import LogFormatter


def setup_logging(args):
    """ Set up logging given parsed logging arguments.
    """

    f_formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(message)s')

    root = logging.getLogger()
    root.setLevel(min(args.log_levels))

    s_handler = logging.StreamHandler(sys.stdout)
    s_handler.setFormatter(LogFormatter())
    root.addHandler(s_handler)

    f_handler = logging.FileHandler(args.log_file.name)
    f_handler.setFormatter(f_formatter)
    root.addHandler(f_handler)


def config(parser):
    """ Configure an argparse parser for logging.
    """

    parser.set_defaults(log_levels=[logging.INFO])

    parser.add_argument('--debug',
        action='append_const',
        dest='log_levels',
        const=logging.DEBUG,
        help='Enable debug logging. If a failure occurs, the program will stop.',
    )

    '''
    # verbose by default now
    parser.add_argument('-v', '--verbose',
        action='append_const',
        dest='log_levels',
        const=logging.INFO,
        help='Enable verbose logging',
    )
    '''

    parser.add_argument('--log-file',
        dest='log_file',
        type=argparse.FileType('a'),
        default=sys.stderr,
        help='Save logs to file. Amount logged affected by --debug, and --verbose flags',
    )
