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
super_debug = False
from_file = False
from_pipe = False
filename = ''

help_string = "    ____       ____                       __\n" \
              "   / __ )___  / __/_  ______  ____ ____  / /\n" \
              "  / __  / _ \\/ /_/ / / / __ \\/ __ `/ _ \\/ / \n" \
              " / /_/ /  __/ __/ /_/ / / / / /_/ /  __/_/  \n" \
              "/_____/\\___/_/  \\__,_/_/ /_/\\__, /\\___(_)   \n" \
              "                           /____/           \n" \
              "  Faceless Befunge Interpreter:\n" \
              "     enables you to run Befunge programs on your computer.\n" \
              "\n" \
              " Examples: python3 runner.py [options]\n" \
              "            python3 runner.py [options] -f programfile.bfg\n" \
              "            <text stream> | python3 runner.py [options] -p\n" \
              "\n" \
              "  Options:\n" \
              "  --log-level - which messages will be printed." \
              " There are 5 levels:\n" \
              "                {INFO(by default), DEBUG, ERROR," \
              " CRITICAL, FATAl};\n" \
              "  --debug     - step-by-step interpretation of a" \
              " program (Can work bad on some consoles)\n"


def clean_up():
    global debug
    global super_debug
    global from_file
    global from_pipe
    global filename

    debug = False
    super_debug = False
    from_file = False
    from_pipe = False
    filename = ''


def main(execute=True):
    term = Terminal()
    if from_file:
        field = Field.load_file(filename)
    elif from_pipe:
        lines = sys.stdin.readlines()
        text = lines[0]
        for line in lines:
            text += line

        program = text
        field = Field.from_text(program)
    else:
        return

    stack = Stack()
    caret = Caret(stack,
                  field,
                  max(3, to_int(term.height) - field.height),
                  debug)
    if debug:
        logger.set_output(caret)
    caret.executor.execute = execute
    logger.debug("Objects created")

    # if super_debug:
    #     input("Continue?")
    if debug:
        try:
            char = readchar()
            if char == 'c':
                print('\nForced exit')
                return
        except Exception:
            print("You shouldn't use pipe without -p option")
            return
        # field height shouldn't change
        print_field(caret, field, term)

    caret.read_instruction(field)
    caret.execute_instruction()
    if caret.direction == Vec(0, 0):
        caret.direction = Right

    logger.debug("Starting loop")
    while caret.executor.execute:
        caret.move(field)
        caret.read_instruction(field)

        if debug or super_debug:
            print_field(caret, field, term)
        else:
            print(caret.diff, end='')
        caret.execute_instruction()

        if debug:
            char = readchar()
            if char == 'c':
                print('\nForced exit')
                return

        logger.debug("Move performed")
    print()


def to_int(obj):
    if obj is None:
        return 0
    return int(obj)


def print_field(caret, field, term: Terminal):
    clear_screen(term)
    with term.location(0, 0):
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

        # sys.stdout.write(' ' * to_int(term.width))
        sys.stdout.write('\r' + str(caret.stack) + '\n')
        print('-' * to_int(term.width))
        debug_len = min(to_int(term.height) - field.height - 3,
                        len(caret.debug_messages) - 3)
        for i in range(0, debug_len):
            sys.stdout.write(caret.debug_messages[i])
        caret.debug_messages = []
        if len(caret.debug_messages) - 3 > debug_len:
            print(str(len(caret.debug_messages) - debug_len) + " more...")
        sys.stdout.write(caret.output)
    sys.stdout.flush()


def clear_screen(term: Terminal):
    term.location(0, 0)
    for i in range(0, to_int(term.height)):
        sys.stdout.write(' ' * to_int(term.width))
    sys.stdout.flush()


def parse_args():
    global from_file
    global from_pipe
    global filename
    global debug
    global super_debug
    if '--log-level' in sys.argv:
        arg_pos = sys.argv.index('--log-level')
        if arg_pos + 1 < len(sys.argv) \
                and not sys.argv[arg_pos + 1].startswith('-'):
            log_level = sys.argv[arg_pos + 1]
            set_log_level(log_level)
            sys.argv.pop(arg_pos)  # remove --log-level
            sys.argv.pop(arg_pos)  # remove level name
        else:
            print("Please, specify log level: "
                  "{INFO(by default), DEBUG, ERROR, CRITICAL, FATAl}")

    if '-p' in sys.argv:
        from_pipe = True
        if '--debug' in sys.argv:
            print("Debug mode is available only with argument-defined program")
            return False

    if '-f' in sys.argv:
        from_file = True
        arg_pos = sys.argv.index('-f')
        if arg_pos + 1 < len(sys.argv) \
                and not sys.argv[arg_pos + 1].startswith('-'):
            filename = sys.argv[arg_pos + 1]
            sys.argv.pop(arg_pos)  # remove -f
            sys.argv.pop(arg_pos)  # remove filename
        else:
            print("Please, specify the file to read from")
            return False

    if '--debug' in sys.argv:
        debug = True
        sys.argv.pop(sys.argv.index('--debug'))  # remove --debug

    if '--super-debug' in sys.argv:
        super_debug = True
        sys.argv.pop(sys.argv.index('--super-debug'))  # remove --super-debug

    if '-h' in sys.argv \
            or '--help' in sys.argv \
            or (not from_file and not from_pipe):
        print(help_string)
        return False

    return True


if __name__ == '__main__':
    clean_up()
    if parse_args():
        main()
