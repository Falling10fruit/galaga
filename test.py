
import curses

class layout:
    def __init__(self, text):
        self.source_text = text
        self.source_array = text.split("\n")
    
    def __str__(self):
        output_string = ""

        for line in self.source_array:
            output_string += line + "\n"

        return output_string

    def draw_at(self, stdscr, line_pos, column_pos):
        for index in range(len(self.source_array)):
            stdscr.addstr(line_pos + index, column_pos, self.source_array[index])

def main(stdscr):
    stdscr.clear()
    
    my_layout = layout("""abc
def
ghi""")
    
    my_layout.draw_at(stdscr, 10, 10)
    stdscr.refresh()
    stdscr.getkey()

curses.wrapper(main)