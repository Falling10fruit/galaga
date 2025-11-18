import math
import time
import curses

stdscr = curses.initscr()

print(f"There are {curses.LINES} lines")

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
    texture_pad = curses.newpad(0, 0)
    position = vec2(0, 0)
    state_tick = 0

    def __init__(self, x = 0, y = 0):
        self.position.x = x
        self.position.y = y
        self.load_pad()
        render_buffer.append(self)
    
    def load_pad(self):
        self.texture_pad = curses.newpad(self.texture_dimensions.x, self.texture_dimensions.y)

        for row in range(self.texture_dimensions.y):
            slice_indicies = vec2(0, self.texture_dimensions.x)
            slice_indicies.add(row * self.texture_dimensions.x)

            self.texture_pad.addstr(row, 0, self.texture[slice_indicies.x:slice_indicies.y])
    

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

#  _  _
# { || }
# [_||_]


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


def render(stdscr):
    stdscr.clear()

    render_buffer[0].texture_pad.refresh(0, 0, 0, 0, 7, 2)

    # for entity in render_buffer:
    #     top_left = entity.position
    #     entity_dimensions = entity.texture_dimensions
    #     offset = entity_dimensions.divide(2)
    #     top_left.substr(offset).to_int()

    #     entity_int_dimensions = entity_dimensions.calc_to_int()
    #     entity.texture_pad.refresh(0, 0, top_left.y, top_left.x, top_left.y + entity_int_dimensions.y, top_left.x + entity_int_dimensions.x)

def main(stdscr):
    stdscr.clear()
    curses.noecho()
    curses.cbreak()

    player = Starfighter(20, 20)

    print(render_buffer)
    
    while True:
        render(stdscr)
        time.sleep(0.016667)

curses.wrapper(main)