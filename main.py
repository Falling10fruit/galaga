import math
import time
import curses
import pynput
from enum import Enum
import random
import string

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
        result = self
        return result.substr(other)
        
    def calc_multiply(self, other):
        result = self
        return result.multiply(other)
    
    def calc_divide(self, other):
        result = self
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
    # avoid creating a shared mutable vec2 at class level
    # each Entity should have its own `position` instance
    position = None
    state_tick = 0
    bulletproof = True
    identification = ""
    render_buffer_index = 0

    def __init__(self, x = 0, y = 0):
        # create an instance-local position vector so instances don't share state
        self.position = vec2(x, y)
        self.layout = layout(self.texture)
        self.identification = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
        self.render_buffer_index = len(render_buffer)
        render_buffer.append(self)
    
#    ^
#  |/.\|
# |/_^_\|
class Starfighter(Entity):
    texture ="""   ^   
 |/.\| 
|/_^_\|"""
    texture_dimensions = vec2(7, 3)
    bulletproof = False
    health = 10

class Bullet(Entity):
    texture = """|""" 
    texture_dimensions = vec2(1, 1)
    pointing_up = False # false for pointing down, aka the enemy

#  _ _
# \ ^ /
#  /_\
class Minion(Entity):
    texture = """ _ _ 
\ ^ /
 /_\ """
    texture_dimensions = vec2(5, 3)
    bulletproof = False
    health = 2

#  _  _
# { || }
# [_||_]
class Butterflu(Entity):
    texture = """ _  _ 
{ || }
[_||_]"""
    texture_dimensions = vec2(6, 3)
    bulletproof = False
    health = 3

#  _   _
# | |_| |
#  \ O /
#   | |
#   *^*
class Mothership(Entity):
    texture = """ _   _
| |_| |
 \ O / 
  | |  
  *^*  """
    texture_dimensions = vec2(7, 5)
    bulletproof = False
    health = 5

#     \_/
#    \___/
#   \_____/
#  \_______/
# \_________/
class Motherbeam(Entity):
    texture = """    \_/    
   \___/   
  \_____/  
 \_______/ 
\_________/"""
    texture_dimensions = vec2(5, 11)
    penetration = 1

debug_message = ""

key_down = {
    "up": False,
    "down": False,
    "left": False,
    "right": False,
}
key_just_down = {
    "space": False
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

    if (key == pynput.keyboard.Key.space):
        key_just_down['space'] = True 

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

bullets_buffer = []

player = Starfighter(curses.COLS // 2 - 1, curses.LINES - 8)
player.identification = "ws0k3"

monster = Minion(curses.COLS // 2 - 1, 10)
monster.identification = "m0n3r"

class Scene(Enum):
    START = "start scene"
    PLAY = "play scene"
current_scene = Scene.START

def release_key_just_down():
    for key in key_just_down.keys():
        key_just_down[key] = False

def control_player():
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
        
    if key_just_down["space"]:
        x_pos = player.position.x + 0.5
        y_pos = round(player.position.y - 1)
        new_bullet = Bullet(x_pos, y_pos)
        new_bullet.pointing_up = True
        new_bullet.identification = "b214"
        bullets_buffer.append(new_bullet)

def simulate_bullets():
    global render_buffer
    global bullets_buffer
    global debug_message

    offset = 0
    for index in range(len(bullets_buffer)):
        bullet = bullets_buffer[index - offset]

        hit = False
        for enemy in render_buffer:
            if enemy.identification == "ws0k3" and bullet.identification == "b214":
                continue
            if enemy.identification != "ws0k3" and bullet.identification != "b214":
                continue
            if enemy.identification == bullet.identification: # we can't use pointing up because it's not guaranteed to be a property
                continue

            x_min_distance = enemy.texture_dimensions.x/2 + 0.5
            y_min_distance = enemy.texture_dimensions.y/2 + 0.5
            x_distance = enemy.position.x - bullet.position.x
            y_distance = enemy.position.y - bullet.position.y

            if x_min_distance >= abs(x_distance) and y_min_distance >= abs(y_distance):
                hit = True
                
                # debug_message = f"bullet {bullet.identification} hit enemy {enemy.identification}"
                # debug_message = f"{enemy.identification == "ws0k3" and bullet.identification == "b124"}"
                
        bullet.render_buffer_index -= offset
        if bullet.position.y < 0 or bullet.position.y > curses.LINES or hit:
            bullets_buffer = bullets_buffer[0:index] + bullets_buffer[index + 1:len(bullets_buffer)]
            offset += 1
            render_buffer = render_buffer[0:bullet.render_buffer_index] + render_buffer[bullet.render_buffer_index + 1:len(render_buffer)]


        if bullet.pointing_up:
            bullet.position.y -= 1
        else:
            bullet.position.y += 1

def tick(stdscr):
    global current_scene

    if current_scene == Scene.PLAY:
        control_player()
        simulate_bullets()

    if current_scene == Scene.START:
        if key_just_down["space"]:
            current_scene = Scene.PLAY
    
    release_key_just_down()

def draw_start_scene(stdscr):
    title = ["     ___           ___           ___       ___           ___           ___      ",
             "    /\  \         /\  \         /\__\     /\  \         /\  \         /\  \     ",
             "   /::\  \       /::\  \       /:/  /    /::\  \       /::\  \       /::\  \    ",
             "  /:/\:\  \     /:/\:\  \     /:/  /    /:/\:\  \     /:/\:\  \     /:/\:\  \   ",
             " /:/  \:\  \   /::\~\:\  \   /:/  /    /::\~\:\  \   /:/  \:\  \   /::\~\:\  \  ",
             "/:/__/_\:\__\ /:/\:\ \:\__\ /:/__/    /:/\:\ \:\__\ /:/__/_\:\__\ /:/\:\ \:\__\ ",
             "\:\  /\ \/__/ \/__\:\/:/  / \:\  \    \/__\:\/:/  / \:\  /\ \/__/ \/__\:\/:/  / ",
             " \:\ \:\__\        \::/  /   \:\  \        \::/  /   \:\ \:\__\        \::/  /  ",
             "  \:\/:/  /        /:/  /     \:\  \       /:/  /     \:\/:/  /        /:/  /   ",
             "   \::/  /        /:/  /       \:\__\     /:/  /       \::/  /        /:/  /    ",
             "    \/__/         \/__/         \/__/     \/__/         \/__/         \/__/     "]
    dimensions = vec2(80, 11)
    top_left = vec2(curses.COLS, curses.LINES).substr(dimensions).calc_divide(2).calc_to_int()

    for index in range(dimensions.y):
        stdscr.addstr(top_left.y + index, top_left.x, title[index])

    if (time.time()*1000)%1000 < 500:
        stdscr.addstr(top_left.y + dimensions.y, top_left.x + dimensions.x//2 - 10, "Press SPACE To Start")
    

def draw_entities_from_buffer(stdscr):
    for entity in render_buffer:
        top_left_x = entity.position.x - entity.texture_dimensions.x / 2
        top_left_y = entity.position.y - entity.texture_dimensions.y / 2
        
        entity.layout.draw_at(stdscr, round(top_left_y), round(top_left_x))

def render(stdscr):
    stdscr.clear()

    global current_scene
    if current_scene == Scene.START:
        draw_start_scene(stdscr)

    draw_entities_from_buffer(stdscr)

    global player
    global bullets_buffer
    # bullet_id = ""
    # if len(bullets_buffer) > 0:
    #     bullet_id = f"bullet identification: {bullets_buffer[0].identification}"
    # else:
    #     bullet_id = "no bullets yet"
    
    stdscr.addstr(curses.LINES - 1, 0, f"debug: {debug_message} | buffer size: {len(render_buffer)} | bullet count {len(bullets_buffer)}")

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