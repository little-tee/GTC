import pygame, time, sys
import sqlite3
from textbox import *


def run():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    KEY_REPEAT_SETTING = (150,50)
    pygame.init()
    pygame.font.init()
    font = pygame.font.Font('GameFont.ttf', 20)

    pygame.display.set_caption("SQL Editor")
    screen = pygame.display.set_mode((1024, 700), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    array = []
    default_text = "None"
    current_row = "None1"
    end_now = False

    field_name = []
    for name in c.execute("PRAGMA table_info(csv);"):
        field_name.append(name)

                    
    running = True
    draw_db()
    while running:
        event = pygame.event.wait ()
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif pygame.mouse.get_pressed()[0] == 1:
            default_text, mouse_handler(pygame.mouse.get_pos())
            input_box = edit_popup(default_text)

    c.close()
    pygame.quit()

class Control(object):
    def __init__(self, screen, dimensions, default_text):
        pygame.init()
        pygame.display.set_caption("Input Box")
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.fps = 60.0
        self.done = False
        self.dimensions = dimensions
        self.input = TextBox(dimensions,command=update_db,
                              clear_on_enter=True,inactive_on_enter=False,
                              buffer=list(default_text))
        self.color = (100,100,100)
        self.prompt = self.make_prompt()
        pygame.key.set_repeat(*KEY_REPEAT_SETTING)

    def make_prompt(self):
        font = pygame.font.SysFont("arial", 20)
        rend = font.render("", True, pygame.Color("white"))     
        return (rend, rend.get_rect(topleft=(0, 0)))

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.done = True
            if end_now:
                self.done = True
            self.input.get_event(event)
            
    def change_color(self,id,color):
        try:
            self.color = pygame.Color(str(color))
        except ValueError:
            print("Please input a valid color name.")

    def main_loop(self):
        while not self.done:
            self.event_loop()
            self.input.update()
            self.input.draw(self.screen)
            self.screen.blit(*self.prompt)
            pygame.display.update()
            self.clock.tick(self.fps)

def update_db(id, data):
    for col_name in field_name:
        print(col_name[1])
        for row_index, row in enumerate(c.execute('SELECT * FROM csv'.format(col_name[1]))):
            if row == current_row:
                print("Thunderbirds are kinda GO!")
                for item_index, item in enumerate(row):
                    if default_text in item:
                        print(col_name[1], data, col_name[1], default_text, field_name[1], current_row[1])
                        c.execute("UPDATE csv SET {0}='{1}' WHERE {0}='{3}' AND {4}='{5}'"
                                  .format(col_name[1], data, col_name[1], default_text, field_name[1][1], current_row[1]))
                        print("Thunderbirds are GO!")
                        conn.commit()
                        print(current_row, row)
                        
                

def draw_db():
    for col_name in c.execute("PRAGMA table_info(csv);"):
        print(col_name[1])
        for row_index, row in enumerate(c.execute('SELECT * FROM csv'.format(col_name[1]))):
            array.append(row)
            for item_index, item in enumerate(row):
                text = font.render(item, True, pygame.Color('White'))            
                screen.blit(text, (30+item_index*150, 30+row_index*23))
                pass
    pygame.display.update()

def edit_popup(default_text):
    x = (pygame.display.get_surface().get_size()[0]-200)/2
    y = (pygame.display.get_surface().get_size()[1]-40)/2
    
    app = Control(screen, (x, y, 200, 40), default_text)
    app.buffer = list(default_text)
    app.main_loop()
    screen.fill(pygame.Color('Black'))
    conn.commit()
    draw_db()

def mouse_handler(mouse_pos):
    global default_text
    global current_row
    mouse_x, mouse_y = mouse_pos[0], mouse_pos[1]
    for y, row in enumerate(array):
        for x, item in enumerate(array[y]):
            if mouse_x > 30+x*150 and mouse_x < 30+x*150+150:
                if mouse_y > 30+y*23 and mouse_y < 30+y*23+23:
                    default_text = array[y][x]
                    current_row = array[y]
                    return default_text, current_row
