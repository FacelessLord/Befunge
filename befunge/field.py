from befunge.utils import logger


class Field:
    def __init__(self, width, height, text: list):
        self.width = width
        self.height = height
        self.map = []
        for i in range(0, height):
            string_list = []
            for j in range(0, width):
                string_list.append(text[i][j])
            self.map.append(string_list)
        logger.debug('Field initialized width:'
                     ' %i, height: %i' % (width, height))

    def get_symbol_at(self, x, y):
        return self.map[y][x]

    def set_symbol_at(self, x, y, char):
        self.map[y][x] = char
        logger.debug('symbol set at %i,%i' % (x, y))

    @classmethod
    def load_file(cls, filename: str):
        with open(filename, 'r') as f:
            lines = f.readlines()
            logger.debug('file %s loaded' % filename)

        # cutting \n
        for i in range(0, len(lines)):
            if i != len(lines) - 1:
                lines[i] = lines[i][0:-1]

        height = len(lines)
        width = len(lines[0])

        for line in lines:
            if len(line) > width:
                width = len(line)

        for i in range(0, len(lines)):
            lines[i] += ' ' * (width - len(lines[i]))

        return Field(width, height, lines)

    @classmethod
    def from_text(cls, text: str):
        lines = text.split('\n')
        height = len(lines)
        width = len(lines[0])

        for line in lines:
            if len(line) > width:
                width = len(line)

        for i in range(0, len(lines)):
            lines[i] += ' ' * (width - len(lines[i]))

        # cutting \n

        return Field(width, height, lines)
