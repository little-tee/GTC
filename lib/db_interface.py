import pygame, time, sys
import sqlite3
from textbox import *

class Editor(object):
    def __init__(self):
        global field_name
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.Font('data/GameFont.ttf', 16)

        pygame.display.set_caption("SQL Editor")
        self.screen = pygame.display.set_mode((1024, 700), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()

        self.conn = sqlite3.connect('data/saves/data.db')
        self.c = self.conn.cursor()

        self.array = []
        self.default_text = "None"
        self.current_row = "None1"

        self.field_name = []
        for name in self.c.execute("PRAGMA table_info(csv);"):
            self.field_name.append(name)

        self.running = True
        self.draw_db()
        while self.running:
            event = pygame.event.wait ()
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            elif pygame.mouse.get_pressed()[0] == 1:
                self.default_text, self.mouse_handler(pygame.mouse.get_pos())
                self.input_box = self.edit_popup(self.default_text)
        self.c.close()

    def update_db(self, id, data, current_row, default_text):
        conn = sqlite3.connect('data/saves/data.db')
        c = conn.cursor()
        field_name = []
        for name in c.execute("PRAGMA table_info(csv);"):
            field_name.append(name)

        for col_name in field_name:
            for row_index, row in enumerate(c.execute('SELECT * FROM csv'.format(col_name[1]))):
                if row == current_row:
                    for item_index, item in enumerate(row):
                        if default_text in item:
                            c.execute("UPDATE csv SET {0}='{1}' WHERE {0}='{3}' AND {4}='{5}'"
                                           .format(col_name[1], data, col_name[1], default_text,
                                                   field_name[1][1], current_row[1]))
                            conn.commit()
                            
    def draw_db(self):
        for col_name in self.c.execute("PRAGMA table_info(csv);"):
            for name_index, name in enumerate(self.field_name):
                text = self.font.render(name[1], True, pygame.Color('White'))            
                self.screen.blit(text, (30+name_index*120, 30+0*20))
                pass
            for row_index, row in enumerate(self.c.execute('SELECT * FROM csv'.format(col_name[1]))):
                self.array.append(row)
                for item_index, item in enumerate(row):
                    text = self.font.render(item, True, pygame.Color('White'))            
                    self.screen.blit(text, (30+item_index*120, 30+(row_index+1)*20))
                    pass
        pygame.display.update()

    def edit_popup(self, default_text):
        x = (pygame.display.get_surface().get_size()[0]-200)/2
        y = (pygame.display.get_surface().get_size()[1]-40)/2
        
        self.app = Control(self.screen, (x, y, 200, 40), self.__class__, self.current_row, self.default_text)
        self.app.main_loop()
        self.screen.fill(pygame.Color('Black'))
        self.conn.commit()
        self.draw_db()

    def mouse_handler(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos[0], mouse_pos[1]
        for y, row in enumerate(self.array):
            for x, item in enumerate(self.array[y]):
                if mouse_x > 30+(x*150) and mouse_x < 30+(x*150)+150:
                    if mouse_y > 30+((y+1)*23) and mouse_y < 30+((y+1)*23)+23:
                        self.default_text = self.array[y][x]
                        self.current_row = self.array[y]
                        

class Control(object):
    def __init__(self, screen, dimensions, parent, current_row, default_text):
        KEY_REPEAT_SETTING = (150,50)
        pygame.init()
        pygame.display.set_caption("Input Box")
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.fps = 60.0
        self.done = False
        self.dimensions = dimensions
        self.input = TextBox(dimensions,parent=parent,current_row=current_row,command=Editor.update_db,
                              clear_on_enter=True,inactive_on_enter=False,
                              buffer=list(default_text), default_text=default_text)
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
            self.input.get_event(event)

    def main_loop(self):
        while not self.done:
            self.event_loop()
            self.input.update()
            self.input.draw(self.screen)
            self.screen.blit(*self.prompt)
            pygame.display.update()
            self.clock.tick(self.fps)
