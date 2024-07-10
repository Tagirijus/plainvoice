"""
I have to be really honest here: ChatGPT was my friend for this
class and methods ...
"""

from prompt_toolkit import Application, HTML
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.styles import Style

import os
import sys


def create_items_grid(items, max_item_length, num_cols):
    lines = []
    for i in range(0, len(items), num_cols):
        line = items[i:i+num_cols]
        lines.append(line)
    return lines


class ListChooser:
    def __init__(self, items, padding=2):
        self.items = items
        self.padding = padding
        self.selected_item = (0, 0)
        self.result = None

        terminal_width = os.get_terminal_size().columns
        self.max_item_length = max(len(item) for item in items)
        self.col_width = self.max_item_length + padding
        self.num_cols = terminal_width // self.col_width
        self.grid = create_items_grid(
           items,
           self.max_item_length,
           self.num_cols
        )

        self.control = FormattedTextControl(focusable=True)
        self.update_display()

    def update_display(self):
        lines = []
        for row_idx, row in enumerate(self.grid):
            line = ""
            for col_idx, item in enumerate(row):
                if (row_idx, col_idx) == self.selected_item:
                    item_str = "<reverse>"
                    item_str += f"{item:<{self.max_item_length}}"
                    item_str += "</reverse>"
                else:
                    item_str = f"{item:<{self.max_item_length}}"
                line += f"{item_str} {' ' * self.padding}"
            lines.append(line)
        self.control.text = HTML("\n".join(lines))

    def move_cursor(self, direction):
        row, col = self.selected_item
        if direction == 'up':
            if row > 0:
                row -= 1
        elif direction == 'down':
            if row < len(self.grid) - 1:
                row += 1
        elif direction == 'left':
            if col > 0:
                col -= 1
        elif direction == 'right':
            if col < len(self.grid[row]) - 1:
                col += 1
        self.selected_item = (row, col)
        self.update_display()

    def get_selected_item(self):
        row, col = self.selected_item
        return self.grid[row][col]

    def prompt(self):
        bindings = KeyBindings()

        @bindings.add('up')
        def up(event):
            self.move_cursor('up')

        @bindings.add('down')
        def down(event):
            self.move_cursor('down')

        @bindings.add('left')
        def left(event):
            self.move_cursor('left')

        @bindings.add('right')
        def right(event):
            self.move_cursor('right')

        @bindings.add('enter')
        def enter(event):
            self.result = self.get_selected_item()
            self.control.text = None
            event.app.exit()
            sys.stdout.write('\033[F\033[K')

        layout = Layout(Window(content=self.control, always_hide_cursor=True))
        style = Style.from_dict({'reverse': 'reverse'})

        application = Application(
           layout=layout,
           key_bindings=bindings,
           full_screen=False,
           style=style
        )
        application.run()
        return self.result


# Example usage in another program
if __name__ == "__main__":
    items = [
        "apple", "banana", "cherry", "date", "elderberry",
        "fig", "grape", "honeydew", "kiwi", "lemon",
        "mango", "nectarine", "orange", "papaya", "quince",
        "raspberry", "strawberry", "tangerine", "ugli fruit", "victoria plum",
        "watermelon", "xigua", "yellow passion fruit", "zucchini"
    ]

    list_chooser = ListChooser(items)
    selected_item = list_chooser.prompt()
    print(f"Selected item: {selected_item}")
