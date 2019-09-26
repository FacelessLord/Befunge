from befunge.executor import Executor
from befunge.field import Field
from befunge.utils import Stack, Vec


class Caret:
    def __init__(self, stack: Stack, field: Field):
        self.direction = Vec(0, 0)
        self.pos = Vec(0, 0)
        self.current_instruction = ' '
        self.executor = Executor()
        self.stack = stack
        self.field = field
        self.string_mode = False

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
        # print(self.current_instruction)
        # print(self.stack)
        self.current_instruction = field.get_symbol_at(self.pos.x, self.pos.y)

    def switch_string_mode(self):
        self.string_mode = not self.string_mode

    def execute_instruction(self):
        if self.current_instruction == '"':
            self.switch_string_mode()
            return
        if self.string_mode:
            self.stack.push(ord(self.current_instruction))
        else:
            if self.current_instruction != ' ' and \
                    self.current_instruction != '\n':
                self.executor[self.current_instruction](self)

    def set_direction(self, new_direction):
        self.direction = new_direction
