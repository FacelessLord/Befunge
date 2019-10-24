from befunge.caret import Caret
from befunge.executor import Executor, exec_g, exec_p
from befunge.field import Field
from befunge.utils import Stack


def test_executor_init():
    try:
        excr = Executor()
    except Exception as e:
        raise e
    else:
        assert excr is not None
        assert excr.instructions is not None


def test_executor_g():
    lines = [['>', 'v'], ['<', '^']]
    fld = Field(2, 2, lines)
    stk = Stack()
    crt = Caret(stk, fld)
    stk.push(1)
    stk.push(0)
    exec_g(crt)
    assert stk.peek() == ord('v')


def test_executor_p():
    lines = [['>', 'v'], ['<', '^']]
    fld = Field(2, 2, lines)
    stk = Stack()
    crt = Caret(stk, fld)
    stk.push(ord('@'))
    stk.push(1)
    stk.push(0)
    exec_p(crt)
    assert fld.get_symbol_at(1, 0) == '@'
