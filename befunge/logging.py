import sys


def get_logger(name: str):
    return Logger(name)


LEVELS = {'CRITICAL': 50,
          'ERROR': 40,
          'WARNING': 30,
          'INFO': 20,
          'DEBUG': 10,
          'NOTSET': 0}


class Logger:
    def __init__(self, name: str):
        self.name = name
        self.level = 'INFO'
        self.output = sys.stdout

    def set_output(self, output):
        self.output = output

    def log(self, message: str, level: str):
        if LEVELS[level] >= LEVELS[self.level]:
            self.output.write(f"{self.level}:{self.name}:{message}\n")

    def set_level(self, level: str):
        self.level = level.upper()

    def critical(self, message):
        self.log(message, 'CRITICAL')

    def error(self, message):
        self.log(message, 'ERROR')

    def warning(self, message):
        self.log(message, 'WARNING')

    def info(self, message):
        self.log(message, 'INFO')

    def debug(self, message):
        self.log(message, 'DEBUG')
