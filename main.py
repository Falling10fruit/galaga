import math
import time
import curses
import pynput

stdscr = curses.initscr()

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

            if ((line_pos + index) < 0) or ((line_pos + index) >= curses.LINES):
                continue
            if column_pos < 0 or (column_pos + len(self.source_array[index])) >= curses.COLS:
                continue

            stdscr.addstr(line_pos + index, column_pos, self.source_array[index])

class vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"[{self.x}, {self.y}]"
    
    def add(self, other):
        if isinstance(other, vec2):
            self.x += other.x
            self.y += other.y
        else:
            self.x += other
            self.y += other
        
        return self

    def substr(self, other):
        if isinstance(other, vec2):
            self.x -= other.x
            self.y -= other.y
        else:
            self.x -= other
            self.y -= other
        
        return self

    def multiply(self, other):
        if isinstance(other, vec2):
            self.x *= other.x
            self.y *= other.y
        else:
            self.x *= other
            self.y *= other
    
        return self

    def divide(self, other):
        if isinstance(other, vec2):
            self.x /= other.x
            self.y /= other.y
        else:
            self.x /= other
            self.y /= other
        
        return self

    def calc_add(self, other):
        result = self
        return result.add(other)
        
    def calc_substr(self, other):
        result = self.__init__()
        return result.substr(other)
        
    def calc_multiply(self, other):
        result = self.__init__()
        return result.multiply(other)
    
    def calc_divide(self, other):
        result = self.__init__()
        return result.divide(other)

    def to_int(self):
        self.x = int(round(self.x))
        self.y = int(round(self.y))
        return self
    
    def calc_to_int(self):
        result = self
        return result.to_int()

render_buffer = []

class Entity:
    texture = ""
    texture_dimensions = vec2(0, 0)
    position = vec2(0, 0)
    state_tick = 0

    def __init__(self, x = 0, y = 0):
        self.position.x = x
        self.position.y = y
        self.layout = layout(self.texture)
        render_buffer.append(self)
    

#    ^
#  |/.\|
# |/_^_\|
class Starfighter(Entity):
    texture ="""   ^   
 |/.\| 
|/_^_\|"""
    texture_dimensions = vec2(7, 3)

#  _ _
# \ ^ /
#  /_\
class Minion(Entity):
    texture = """ _ _ 
\ ^ /
 /_\ """
    texture_dimensions = vec2(5, 3)

#  _  _
# { || }
# [_||_]
class Butterflu(Entity):
    texture = ""

#  _   _
# | |_| |
#  \ O /
#   | |
#   *^*
#     \_/
#    \___/
#   \_____/
#  \_______/
# \_________/

key_down = {
    "up": False,
    "down": False,
    "left": False,
    "right": False,
}
last_keydown = False

def handle_keydown(key, is_injected):
    global key_down
    global last_keydown

    last_keydown = key

    if (key == pynput.keyboard.Key.up):
        key_down['up'] = True 
    if (key == pynput.keyboard.Key.down):
        key_down['down'] = True 
    if (key == pynput.keyboard.Key.left):
        key_down['left'] = True 
    if (key == pynput.keyboard.Key.right):
        key_down['right'] = True 

def handle_keyup(key, is_rejected):
    if (key == pynput.keyboard.Key.up):
        key_down['up'] = False 
    if (key == pynput.keyboard.Key.down):
        key_down['down'] = False 
    if (key == pynput.keyboard.Key.left):
        key_down['left'] = False 
    if (key == pynput.keyboard.Key.right):
        key_down['right'] = False 

keystroke_handler = pynput.keyboard.Listener(
    on_press=handle_keydown,
    on_release=handle_keyup
)
keystroke_handler.start()

player = Starfighter(50, curses.LINES - 8)

def tick(stdscr):
    global player
    player_speed = vec2(1, 0.5)

    if key_down['up']:
        player.position.y -= player_speed.y
    if key_down['down']:
        player.position.y += player_speed.y
    if key_down['right']:
        player.position.x += player_speed.x
    if key_down['left']:
        player.position.x -= player_speed.x

def render(stdscr):
    global player

    stdscr.clear()

    for entity in render_buffer:
        top_left_x = entity.position.x - entity.texture_dimensions.x / 2
        top_left_y = entity.position.y - entity.texture_dimensions.y / 2
        
        entity.layout.draw_at(stdscr, round(top_left_y), round(top_left_x))


    stdscr.addstr(curses.LINES - 1, 0, f"player position: {player.position.__str__()} | last key pressed: {last_keydown}")

    stdscr.refresh()

def main(stdscr):
    stdscr.clear()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    stdscr.nodelay(True)
    
    while True:
        tick(stdscr)
        render(stdscr)
        time.sleep(0.016667)

curses.wrapper(main)