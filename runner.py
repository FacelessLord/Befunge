import platform
import sys

from blessings import Terminal

from befunge.caret import Caret
from befunge.field import Field
from befunge.utils import Stack, Right, Vec, logger, set_log_level

if 'linux' in platform.system().lower() or 'osx' in platform.system().lower():
    from readchar.readchar_linux import readchar
else:
    from readchar.readchar_windows import readchar

debug = False
from_file = False
from_program = True
filename = ''


def main(execute=True):
    term = Terminal()
    if from_file:
        field = Field.load_file(filename)
    else:
        if from_program:
            program = '\\'
            print("Enter the program code: ")
            while program[-1] == '\\':
                program = program[:-1] + (
                    '\n' if program != '\\' else '')  # cutting the last character and inserting \n
                program += input()
            field = Field.from_text(program)
            print('-' * (field.width + 2))
        else:
            lines = sys.stdin.readlines()
            text = lines[0]
            for line in lines:
                text += '\n' + line
            program = text
            field = Field.from_text(program)

    stack = Stack()
    caret = Caret(stack, field, to_int(term.height) - field.height - 3, debug)
    caret.executor.execute = execute
    logger.debug("Objects created")

    if debug:
        try:
            char = readchar()
            if char == 'c':
                print('\nForced exit')
                exit()
        except Exception:
            print("You shouldn't use pipe without -p option")
            exit()
        sys.stdout.write('\n' * (field.height + 1))  # field height shouldn't change
        print_field(caret, field, term)

    caret.read_instruction(field)
    caret.execute_instruction()
    if caret.direction == Vec(0, 0):
        caret.direction = Right

    logger.debug("Starting loop")
    while caret.executor.execute:
        caret.move(field)
        caret.read_instruction(field)

        if debug:
            print_field(caret, field, term)
        else:
            print(caret.diff, end='')
        caret.execute_instruction()

        if debug:
            char = readchar()

        logger.debug("Move performed")
    print()


def to_int(obj):
    if obj is None:
        return 0
    return int(obj)


def print_field(caret, field, term):
    with term.location(0, max(0, to_int(term.height) - field.height - caret.new_line_count - 1)):
        for i in range(len(field.map)):
            if i != caret.pos.y:
                for j in range(0, field.width):
                    sys.stdout.write(field.map[i][j])
                sys.stdout.write('\n')
            else:
                for j in range(0, caret.pos.x):
                    sys.stdout.write(field.map[i][j])
                sys.stdout.write('\033[30;41m' + field.map[i][caret.pos.x])
                sys.stdout.write('\033[31;0m')
                for j in range(caret.pos.x + 1, field.width):
                    sys.stdout.write(field.map[i][j])
                sys.stdout.write('\n')

        sys.stdout.write(' ' * to_int(term.width))
        sys.stdout.write('\r' + str(caret.stack) + '\n')

        sys.stdout.write(caret.output)
    sys.stdout.flush()


if __name__ == '__main__':
    if '--log-level' in sys.argv:
        arg_pos = sys.argv.index('--log-level')
        if arg_pos + 1 < len(sys.argv):
            log_level = sys.argv[arg_pos + 1]
            set_log_level(log_level)
            sys.argv.pop(arg_pos)  # remove --log-level
            sys.argv.pop(arg_pos)  # remove level name
        else:
            print("Please, specify log level: {INFO(by default), DEBUG, ERROR, CRITICAL, FATAl}")

    if '-p' in sys.argv:
        from_program = False
        if '--debug' in sys.argv:
            print("Debug mode is available only with argument-defined program")
            exit()

    if '-f' in sys.argv:
        arg_pos = sys.argv.index('-f')
        from_file = True
        if arg_pos + 1 < len(sys.argv):
            filename = sys.argv[arg_pos + 1]
            sys.argv.pop(arg_pos)  # remove --log-level
            sys.argv.pop(arg_pos)  # remove level name
        else:
            print("Please, specify the file to read from")
            exit()

    if '--debug' in sys.argv:
        debug = True
        sys.argv.pop(sys.argv.index('--debug'))  # remove --debug

    main()
