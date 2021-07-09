from enum import Enum


class Colors(Enum):
    blank = 0
    white = 1
    black = 2

    def __str__(self):
        if self.value == 1:
            return 'w'
        elif self.value == 2:
            return 'b'
        else:
            return ''
