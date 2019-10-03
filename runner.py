import sys

from befunge.caret import Caret
from befunge.field import Field
from befunge.utils import Stack, Right, Vec
from befunge.texts import filename_input_promt

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def main(filename="", execute=True):
    if filename == "":
        logger.debug("File is not specified as an argument")
        filename = input(filename_input_promt)

    field = Field.load_file(filename)
    stack = Stack()
    caret = Caret(stack, field)
    logger.debug("Objects created")

    caret.move(field)
    caret.read_instruction(field)
    caret.execute_instruction()
    if caret.direction == Vec(0, 0):
        caret.direction = Right
    logger.debug("Starting loop")
    while execute:
        caret.move(field)
        caret.read_instruction(field)
        caret.execute_instruction()
        logger.debug("Move performed")


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else "")
