import sys

from .options import get_parser, parse_args, validate


NAME = 'deps2dot'


def generate(_):
    pass


def main():
    # setup.py install/develop creates an executable that calls this function
    generate(
        validate(
            parse_args(
                get_parser(NAME), sys.argv[1:]
            )
        )
    )
