from befunge.caret import Caret
from befunge.field import Field
from befunge.utils import Stack, Right, Down, Left, Up, Vec


def test_change_direction():
    lines = [['>', 'v'], ['^', '<']]
    fld = Field(2, 2, lines)
    stk = Stack()
    crt = Caret(stk, fld)

    crt.move(fld)
    crt.read_instruction(fld)
    crt.execute_instruction()
    assert crt.direction == Right
    crt.move(fld)
    crt.read_instruction(fld)
    crt.execute_instruction()
    assert crt.direction == Down
    crt.move(fld)
    crt.read_instruction(fld)
    crt.execute_instruction()
    assert crt.direction == Left
    crt.move(fld)
    crt.read_instruction(fld)
    crt.execute_instruction()
    assert crt.direction == Up
    crt.move(fld)
    assert crt.pos == Vec(0, 0)


def test_horizontal_if():
    lines = [['_']]
    fld = Field(1, 1, lines)
    stk = Stack()
    crt = Caret(stk, fld)

    stk.push(174)
    crt.read_instruction(fld)
    crt.execute_instruction()
    assert crt.direction == Left
    stk.push(0)
    crt.read_instruction(fld)
    crt.execute_instruction()
    assert crt.direction == Right


def test_vertical_if():
    lines = [['|']]
    fld = Field(1, 1, lines)
    stk = Stack()
    crt = Caret(stk, fld)

    stk.push(174)
    crt.read_instruction(fld)
    crt.execute_instruction()
    assert crt.direction == Up
    stk.push(0)
    crt.read_instruction(fld)
    crt.execute_instruction()
    assert crt.direction == Down


def test_trampoline():
    lines = [['>', '#', '1', '.']]
    fld = Field(4, 1, lines)
    stk = Stack()
    crt = Caret(stk, fld)

    crt.read_instruction(fld)
    crt.execute_instruction()
    assert crt.direction == Right
    crt.move(fld)
    crt.read_instruction(fld)
    assert crt.current_instruction == '#'
    crt.execute_instruction()
    crt.move(fld)
    crt.read_instruction(fld)
    assert crt.current_instruction == '.'
