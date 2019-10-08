import sys

from befunge.caret import Caret
from befunge.field import Field
from befunge.texts import filename_input_promt
from befunge.utils import Stack, Right, Vec, logger, set_log_level


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
    log_level_pos = sys.argv.index('--log-level')
    if log_level_pos >= 0:
        if log_level_pos + 1 <= len(sys.argv):
            log_level = sys.argv[log_level_pos + 1]
            set_log_level(log_level)
            sys.argv.pop(log_level_pos)  # remove --log-level
            sys.argv.pop(log_level_pos)  # remove level name
        else:
            print("Please, specify log level: {INFO(by default), DEBUG, ERROR, CRITICAL, FATAl}")
    main(sys.argv[1] if len(sys.argv) > 1 else "")
