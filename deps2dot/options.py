import argparse
import sys

from . import __doc__ as DESCRIPTION, __version__


EPILOG = '''
Documentation & downloads: http://pypi.python.org/pypi/%(prog)s/

Version {}
'''


def _exit(message):
    '''
    Print message on stderr and exit. A handy function for tests to mock out.
    '''
    sys.stderr.write(message + '\n')
    sys.exit(2)


def get_parser(name):
    parser = argparse.ArgumentParser(
        description=DESCRIPTION,
        prog=name,
        epilog=EPILOG.format(__version__),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument('--version',
        action='version', version='%(prog)s v' + __version__)
    return parser


def parse_args(parser, args):
    return parser.parse_args(args)


def validate(options):
    return options

