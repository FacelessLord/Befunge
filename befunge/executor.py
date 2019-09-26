from befunge.utils import Up, Right, Down, Left, next_direction


def load_instructions(instructions: dict):
    # directions
    instructions['^'] = lambda c: c.set_direction(Up)
    instructions['>'] = lambda c: c.set_direction(Right)
    instructions['V'] = lambda c: c.set_direction(Down)
    instructions['v'] = lambda c: c.set_direction(Down)
    instructions['<'] = lambda c: c.set_direction(Left)

    # if
    instructions['-'] = lambda c: c.set_direction(Right) if c.stack.peek() == 0 else c.set_direction(Left)
    instructions['|'] = lambda c: c.set_direction(Down) if c.stack.peek() == 0 else c.set_direction(Up)

    instructions['?'] = lambda c: c.set_direction(next_direction())
    instructions['#'] = lambda c: c.move()
    instructions['@'] = lambda c: exit()

    # stack
    instructions[':'] = lambda c: c.stack.dup()
    instructions['\\'] = lambda c: c.stack.swap()
    instructions['$'] = lambda c: c.stack.pop()

    instructions['p'] = exec_p
    instructions['g'] = exec_g

    # constants
    instructions[str(0)] = lambda c: c.stack.push(int(0))
    instructions[str(1)] = lambda c: c.stack.push(int(1))
    instructions[str(2)] = lambda c: c.stack.push(int(2))
    instructions[str(3)] = lambda c: c.stack.push(int(3))
    instructions[str(4)] = lambda c: c.stack.push(int(4))
    instructions[str(5)] = lambda c: c.stack.push(int(5))
    instructions[str(6)] = lambda c: c.stack.push(int(6))
    instructions[str(7)] = lambda c: c.stack.push(int(7))
    instructions[str(8)] = lambda c: c.stack.push(int(8))
    instructions[str(9)] = lambda c: c.stack.push(int(9))

    instructions['"'] = lambda c: c.switch_string_mode

    # operations
    instructions['*'] = lambda c: c.stack.push(c.stack.pop() * c.stack.pop())
    instructions['/'] = lambda c: exec_div
    instructions['+'] = lambda c: c.stack.push(c.stack.pop() + c.stack.pop())
    instructions['-'] = lambda c: c.stack.push(-c.stack.pop() + c.stack.pop())
    instructions['%'] = lambda c: c.stack.push(c.stack.pop() % c.stack.pop())
    # logic
    instructions['!'] = lambda c: c.stack.push(0 if c.stack.pop() != 0 else 1)
    instructions['`'] = lambda c: c.stack.push(1 if c.stack.pop() < c.stack.pop() else 0)

    instructions['&'] = lambda c: exec_num_input
    instructions['~'] = lambda c: exec_char_input
    instructions['.'] = lambda c: print(c.stack.pop())
    instructions[','] = lambda c: print(chr(c.stack.pop()), end="")
    # todo


def exec_num_input(c):
    v = input("Enter a number: ")
    c.stack.push(int(v))


def exec_char_input(c):
    v = input("Enter a character: ")
    c.stack.push(v[0])


def exec_div(c):
    c.stack.swap()
    c.stack.push(c.stack.pop() / c.stack.pop())


def exec_p(c):
    x = c.stack.pop()
    y = c.stack.pop()
    code = c.stack.pop()
    symb = chr(code)

    c.field.set_symbol_at(x, y, symb)


def exec_g(c):
    x = c.stack.pop()
    y = c.stack.pop()
    symb = c.field.get_symbol_at(x, y)
    code = ord(symb)

    c.stack.push(code)


class Executor:
    def __init__(self):
        self.instructions = {}
        load_instructions(self.instructions)

    def __getitem__(self, item):
        return self.instructions[item]
