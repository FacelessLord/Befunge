from blessings import Terminal

import runner
from befunge.caret import Caret
from befunge.field import Field
from befunge.utils import Stack


def test_runner_load():
    try:
        runner.main("tests/fld_test_program.txt", False)
    except Exception as e:
        raise e


def test_runner_run():
    try:
        runner.main("tests/fld_test_program.txt", True)
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
