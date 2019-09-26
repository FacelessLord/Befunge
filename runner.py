import time

from befunge.caret import Caret
from befunge.field import Field
from befunge.utils import Stack, Right
from befunge.texts import filename_input_promt


def main(filename="", execute=True):
    if filename == "":
        filename = input(filename_input_promt)

    field = Field.load_file(filename)
    stack = Stack()
    caret = Caret(stack, field)

    caret.move(field)
    caret.execute_instruction()
    caret.direction = Right
    while execute:
        caret.move(field)
        caret.execute_instruction()
        # time.sleep(1)
        # print(caret.current_instruction, end='')


if __name__ == '__main__':
    main()
