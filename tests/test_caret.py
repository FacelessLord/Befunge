from befunge.caret import Caret
from befunge.field import Field
from befunge.utils import Stack, Vec, Right, Left, Up, Down


def test_caret_init():
    lines = [['>', 'v'], ['<', '^']]
    fld = Field(2, 2, lines)
    stk = Stack()
    try:
        crt = Caret(stk, fld)
    except Exception as e:
        raise e
    else:
        assert crt is not None
        assert crt.pos is not None
        assert crt.string_mode is False
        assert crt.field is fld
        assert crt.direction == Vec(0, 0)


def test_caret_move_first():
    lines = [['>', 'v'], ['<', '^']]
    fld = Field(2, 2, lines)
    stk = Stack()
    crt = Caret(stk, fld)
    crt.move(fld)
    crt.read_instruction(fld)
    assert crt.direction == Vec(0, 0)
    assert crt.current_instruction == '>'


def test_caret_move():
    lines = [['>', 'v'], ['<', '^']]
    fld = Field(2, 2, lines)
    stk = Stack()
    crt = Caret(stk, fld)
    crt.set_direction(Right)
    crt.move(fld)
    crt.read_instruction(fld)
    assert crt.direction == Right
    assert crt.current_instruction == 'v'


def test_caret_move_behind_left_border():
    lines = [['>', 'v'], ['<', '^']]
    fld = Field(2, 2, lines)
    stk = Stack()
    crt = Caret(stk, fld)
    crt.set_direction(Left)
    crt.move(fld)
    assert crt.direction == Left
    assert crt.pos == Vec(1, 0)


def test_caret_move_behind_right_border():
    lines = [['>', 'v'], ['<', '^']]
    fld = Field(2, 2, lines)
    stk = Stack()
    crt = Caret(stk, fld)
    crt.set_direction(Right)
    crt.move(fld)
    crt.move(fld)
    assert crt.direction == Right
    assert crt.pos == Vec(0, 0)


def test_caret_move_behind_top_border():
    lines = [['>', 'v'], ['<', '^']]
    fld = Field(2, 2, lines)
    stk = Stack()
    crt = Caret(stk, fld)
    crt.set_direction(Up)
    crt.move(fld)
    assert crt.direction == Up
    assert crt.pos == Vec(0, 1)


def test_caret_changes_direction():
    lines = [['>', 'v'], ['<', '^']]
    fld = Field(2, 2, lines)
    stk = Stack()
    crt = Caret(stk, fld)
    crt.set_direction(Down)
    assert crt.direction == Down
    crt.set_direction(Left)
    assert crt.direction == Left
    crt.set_direction(Right)
    assert crt.direction == Right
    crt.set_direction(Up)
    assert crt.direction == Up


def test_caret_move_behind_down_border():
    lines = [['>', 'v'], ['<', '^']]
    fld = Field(2, 2, lines)
    stk = Stack()
    crt = Caret(stk, fld)
    crt.set_direction(Down)
    crt.move(fld)
    crt.move(fld)
    assert crt.direction == Down
    assert crt.pos == Vec(0, 0)


def test_caret_switch_string_mode():
    lines = [['>', 'v'], ['<', '^']]
    fld = Field(2, 2, lines)
    stk = Stack()
    crt = Caret(stk, fld)
    assert not crt.string_mode
    crt.switch_string_mode()
    assert crt.string_mode
    crt.switch_string_mode()
    assert not crt.string_mode
