import sys

from blessings import Terminal

import runner
from befunge.caret import Caret
from befunge.field import Field
from befunge.utils import Stack


def test_runner_load():
    try:
        runner.from_file = True
        runner.filename = "tests/fld_test_program.txt"
        runner.main(False)
    except Exception as e:
        raise e


def test_runner_run():
    try:
        runner.from_file = True
        runner.filename = "tests/fld_test_program.txt"
        runner.main(True)
    except Exception as e:
        raise e


def test_runner_implicit_run():
    try:
        sys.argv.append('-f')
        sys.argv.append("tests/fld_test_program.txt")
        import runner
    except Exception as e:
        raise e


def test_field_print():
    try:
        field = Field.load_file("tests/fld_test_program.txt")
        stack = Stack()
        caret = Caret(stack, field, True)
        term = Terminal()
        runner.print_field(caret, field, term)
    except Exception as e:
        raise e
