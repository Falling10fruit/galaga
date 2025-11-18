
import curses

class layout:
    def generate_output_array(self):
        output_array = [[]]
        line = 0

        for char in self.source_text:
            if char == "\n":
                output_array.push([])
                line += 1
            else:
                output_array[line].push(char)

        return output_array

    def __init__(self, text):
        self.source_text = text
        self.source_array = self.generate_output_array(self)
    
    def __str__(self):
        for line in self.source_array:
            line_print = ""

            for char in line:
                line_print += char + " "
            
            print(line_print)
        print("layout_printed")

def main(stdscr):
    my_layout = layout("""abc
def
ghi
""")
    print(my_layout)