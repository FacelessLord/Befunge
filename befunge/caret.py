from befunge.executor import Executor
from befunge.field import Field
from befunge.utils import Stack, Vec, logger


class Caret:
    def __init__(self, stack: Stack,
                 field: Field,
                 max_new_line_count=10,
                 debug=False):
        self.direction = Vec(0, 0)
        self.pos = Vec(0, 0)
        self.current_instruction = ' '
        self.executor = Executor()
        self.stack = stack
        self.field = field
        self.string_mode = False
        self.new_line_count = 0
        self.max_new_line_count = max_new_line_count
        self.diff = ''
        self.output = ''
        self.debug = debug
        self.debug_messages = []
        logger.debug("Caret init")

    def move(self, field):
        self.pos += self.direction
        if self.pos.x > field.width - 1:
            self.pos.x = 0
        if self.pos.y > field.height - 1:
            self.pos.y = 0

        if self.pos.x < 0:
            self.pos.x = field.width - 1
        if self.pos.y < 0:
            self.pos.y = field.height - 1
        logger.debug("Caret move")

    def read_instruction(self, field):
        self.current_instruction = field.get_symbol_at(self.pos.x, self.pos.y)
        logger.debug("Instruction read")

    def switch_string_mode(self):
        self.string_mode = not self.string_mode
        logger.debug("Mode toggled")

    def execute_instruction(self):
        self.diff = ''
        if self.current_instruction == '"':
            self.switch_string_mode()
            return
        if self.string_mode:
            self.stack.push(ord(self.current_instruction))
        else:
            if self.current_instruction != ' ' and \
                    self.current_instruction != '\n':
                self.executor[self.current_instruction](self)
                logger.debug("Instruction executed: '" + self.current_instruction + "'")

    def set_direction(self, new_direction):
        self.direction = new_direction
        logger.debug("Direction changed: " + str(new_direction))

    def write(self, message):
        self.debug_messages.append(message)
