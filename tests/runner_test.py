import sys

from blessings import Terminal

import runner
from befunge.caret import Caret
from befunge.field import Field
from befunge.utils import Stack


def test_runner_run():
    try:
        sys.argv.append('-f')
        sys.argv.append("tests/fld_test_program.txt")
        runner.clean_up()
        runner.parse_args()
        runner.main(True)
    except Exception as e:
        raise e


def test_runner_implicit_program_run():
    try:
        sys.argv.append('-f')
        sys.argv.append("tests/fld_test_program.txt")
        runner.clean_up()
        runner.parse_args()
        runner.main()
    except Exception as e:
        raise e


def test_runner_explicit_input():
    with open("tests/fld_test_program.txt", 'rt') as f:
        sys.stdin = f
        try:
            runner.clean_up()
            assert not runner.parse_args()
            assert not runner.from_file
        except Exception as e:
            raise e


def test_runner_stream_input():
    with open("tests/fld_test_program.txt", 'rt') as f:
        sys.stdin = f
        try:
            sys.argv.append('-p')
            runner.clean_up()
            runner.parse_args()
            assert not runner.from_pipe
            assert not runner.from_file
            runner.main(False)
        except Exception as e:
            raise e


def test_debug():
    try:
        sys.argv.append('--debug')
        sys.argv.append('-f')
        sys.argv.append("tests/fld_test_program.txt")
        runner.clean_up()
        runner.parse_args()
        runner.main(False)
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


def test_to_int_with_num():
    assert runner.to_int(5) == 5


def test_to_int_with_str_num():
    assert runner.to_int('5') == 5


def test_to_int_none():
    assert runner.to_int(None) == 0
