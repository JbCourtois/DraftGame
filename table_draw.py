# -*- coding: utf-8 -*-
class TableDraw(object):
    JOINERS_OLD = {
        (True, True, True, True): '┼',
        (True, True, True, False): '┤',
        (True, True, False, True): '├',
        (True, True, False, False): '│',
        (True, False, True, True): '┴',
        (True, False, True, False): '┘',
        (True, False, False, True): '└',
        (False, True, True, True): '┬',
        (False, True, True, False): '┐',
        (False, True, False, True): '┌',
        (False, False, True, True): '─',
    }
    JOINERS = {
        (True, True, True, True): '╬',
        (True, True, True, False): '╣',
        (True, True, False, True): '╠',
        (True, True, False, False): '║',
        (True, False, True, True): '╩',
        (True, False, True, False): '╝',
        (True, False, False, True): '╚',
        (False, True, True, True): '╦',
        (False, True, True, False): '╗',
        (False, True, False, True): '╔',
        (False, False, True, True): '═',
    }

    HORIZONTAL = JOINERS[(False, False, True, True)]
    VERTICAL = JOINERS[(True, True, False, False)]

    def fill_joiner_char(self, up=True, down=True, left=True, right=True):
        return self.JOINERS[(up, down, left, right)]


class CollectionDraw(TableDraw):
    """Tool to pretty-print a CardCollection."""
    CARD_WIDTH = 8
    BORDER = TableDraw.HORIZONTAL * CARD_WIDTH

    def __init__(self, collection, active_red=True):
        table = collection.sorted(active_red=active_red)
        self.rows = [[idcard.text for idcard in row] for row in table]
        self.max_index = len(self.rows)

    def adjust_spaces(self, text):
        """Add spaces to fit exactly desired card width."""
        return text + ' ' * (self.CARD_WIDTH - len(text))

    def get_row_width(self, index):
        """Get length in columns of the index row."""
        if index < 0:
            return -1

        try:
            return len(self.rows[index])
        except IndexError:
            return -1

    def get_ruler_width(self, index):
        return max(self.get_row_width(row_index) for row_index in (index, index - 1))

    def get_joiner(self, row, col):
        """Compute the separator character for the row-th ruler for col-th column."""
        up = (col <= self.get_row_width(row - 1))
        down = (col <= self.get_row_width(row))
        left = (col > 0)
        right = (col < self.get_ruler_width(row))

        return self.fill_joiner_char(up=up, down=down, left=left, right=right)

    def format_ruler(self, row):
        result = []
        row_width = self.get_ruler_width(row)

        for col in range(row_width):
            result.append(self.get_joiner(row, col))
            result.append(self.BORDER)
        result.append(self.get_joiner(row, row_width))

        return ''.join(result)

    def _format_fragment_row(self, line):
        """Format just a text-line of a row of cards."""
        result = ['']
        result.extend(self.adjust_spaces(text) for text in line)
        result.append('')

        return self.VERTICAL.join(result)

    def format_row(self, r_index):
        row = self.rows[r_index]
        lines = zip(*row)

        return '\n'.join(self._format_fragment_row(line) for line in lines)

    def format(self):
        result = []
        max_index = self.max_index

        for r_index in range(max_index):
            result.append(self.format_ruler(r_index))
            result.append(self.format_row(r_index))
        result.append(self.format_ruler(max_index))

        return '\n'.join(result)
