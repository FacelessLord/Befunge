from random import randint

from befunge.logging import get_logger

logger = get_logger("befunge")


def set_log_level(log_level: str):
    lower = log_level.lower()
    if lower == 'debug':
        logger.set_level(log_level)
        logger.debug("log-level=" + log_level)
    if lower == 'info':
        logger.set_level(log_level)
        logger.info("log-level=" + log_level)
    if lower == 'warning':
        logger.set_level(log_level)
        logger.warning("log-level=" + log_level)
    if lower == 'error':
        logger.set_level(log_level)
        logger.error("log-level=" + log_level)
    if lower == 'critical':
        logger.set_level(log_level)
        logger.critical("log-level=" + log_level)


class Stack:
    def __init__(self):
        self.size = 1
        self.ptr = None
        logger.debug("Stack initialized")

    def __len__(self):
        return self.size

    def push(self, item):
        entry = (item, self.ptr)
        self.ptr = entry
        logger.debug("stack push")

    def pop(self):
        if self.ptr is None:
            return 0
        entry = self.ptr
        self.ptr = self.ptr[1]
        logger.debug("stack pop")
        return entry[0]

    def peek(self):
        if self.ptr is None:
            logger.debug("stack empty")
            return 0
        logger.debug("stack peek")
        return self.ptr[0]

    def dup(self):
        self.push(self.peek())
        logger.debug("stack dup")

    def swap(self):
        a = self.pop()
        b = self.pop()
        self.push(a)
        self.push(b)
        logger.debug("stack swap")

    def __str__(self):
        s = "["
        last = self.ptr
        if last is None:
            return '[ ]'
        while last is not None:
            obj_str = str(last[0])
            if len(obj_str) == 1:
                if ord(obj_str) < 32:
                    obj_str = '\\' + str(ord(obj_str))
            s += obj_str + ", "
            last = last[1]
        s = s[:-2]
        s += "]"
        logger.debug("stack stringified")
        return s


class Vec:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        return Vec(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"


Left = Vec(-1, 0)
Right = Vec(1, 0)
Up = Vec(0, -1)
Down = Vec(0, 1)


def next_direction():
    dir_num = randint(0, 4)
    # print("dir: " + str(dir_num))
    if dir_num == 0:
        return Up
    elif dir_num == 1:
        return Left
    elif dir_num == 2:
        return Down
    else:
        return Right
