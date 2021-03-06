import argparse
import log
import logging
import sys

from .. import version

from .log import LogFormatter


def setup_logging(args):
    """ Set up logging given parsed logging arguments.
    """

    logging.root.setLevel(min(args.log_levels))
    root = logging.getLogger()

    f_formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(message)s')

    root = logging.getLogger()
    root.setLevel(min(args.log_levels))

    s_handler = logging.StreamHandler(sys.stdout)
    s_handler.setFormatter(LogFormatter(color_off=args.color_off))
    root.addHandler(s_handler)

    if args.log_file:
        f_handler = logging.FileHandler(args.log_file.name)
        f_handler.setFormatter(f_formatter)
        root.addHandler(f_handler)

    # the requests library has it's own log statements, and it bundles itself without asking
    logging.getLogger("requests").setLevel(logging.WARNING)


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
        default=None,
        help='Save logs to file. Amount logged affected by --debug',
    )

    parser.add_argument('--color_off',
        dest='color_off',
        action='store_true',
        help='Disable colored output',
    )
