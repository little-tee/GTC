'''
   GTC, written by Connor124: Connor124.github.io/gtc.html,
   Requires PyTmx and PyScroll by bitcraft: https://github.com/bitcraft
   both are provided and should work as is.

   Controls:
       WASD     - Sprint
       Arrows   - Walk
       Numpad 0 - Enter Room

'''

#Adds 'lib' to syspath.
import os
import os.path as path
from sys import path as syspath
import sys
syspath.append(path.join(path.dirname(__file__), 'lib'))

#Imports uncategorised modules.
from time import sleep
from time import time as systime
from math import *
import pickle
import random
from w_random import WeightedRandomizer
from multiprocessing import Process
from evdev import InputDevice, ecodes
import mss
import mss.tools
import numpy as np
import cv2

#Import pygame.
import pygame
from pygame.locals import *
from pygame import font, display, time, image, sprite, event, key
import pygame.surfarray as surfarray

#Imports pytmx.
from pytmx.util_pygame import load_pygame
import pytmx

#Import pyscroll.
import pyscroll
import pyscroll.data
from pyscroll.group import PyscrollGroup

# define configuration variables here.
RESOURCES_DIR = 'data'

TIME_PLAYING = 0

HERO_MOVE_SPEED = 150  # pixels per second.
HERO_SPRINT_SPEED = 2000
MAP_FILENAME = os.path.join('forest.tmx')
FOREST = os.path.join("forest.tmx")
clock = pygame.time.Clock()

screenMode = pygame.RESIZABLE

# simple wrapper to keep the screen resizeable.
def init_screen(width, height, mode):
    screen = pygame.display.set_mode((int(width), int(height)), mode)
    return screen


# make loading maps a little easier.
def get_map(filename):
    return os.path.join(RESOURCES_DIR, "maps", filename)

def get_resource(filename):
    return os.path.join(RESOURCES_DIR, filename)


# make loading images a little easier.
def load_image(filename):
    return pygame.image.load(os.path.join(RESOURCES_DIR, filename))

class Hero(pygame.sprite.Sprite):
    """ Our Hero

    The Hero has three collision rects, one for the whole sprite "rect" and
    "old_rect", and another to check collisions with walls, called "feet".

    The position list is used because pygame rects are inaccurate for
    positioning sprites; because the values they get are 'rounded down'
    as integers, the sprite would move faster moving left or up.

    Feet is 1/2 as wide as the normal rect, and 8 pixels tall.  This size size
    allows the top of the sprite to overlap walls.  The feet rect is used for
    collisions, while the 'rect' rect is used for drawing.

    There is also an old_rect that is used to reposition the sprite if it
    collides with level walls.
    """

    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image(image).convert_alpha()
        self.velocity = [0, 0]
        self._position = [0, 0]
        self._old_position = self.position
        self.rect = self.image.get_rect()
        self.feet = pygame.Rect(0, 0, self.rect.width * .5, 8)
        
    @property
    def position(self):
        return list(self._position)

    @position.setter
    def position(self, value):
        self._position = list(value)

    def update(self, dt):
        self._old_position = self._position[:]
        self._position[0] += self.velocity[0] * dt
        self._position[1] += self.velocity[1] * dt
        self.rect.topleft = self._position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self, dt):
        """ If called after an update, the sprite can move back
        """
        self._position = self._old_position
        self.rect.topleft = self._position
        self.feet.midbottom = self.rect.midbottom
class QuestGame(object):
    """ This class is a basic game.

    This class will load data, create a pyscroll group, a hero object.
    It also reads input and moves the Hero around the map.
    Finally, it uses a pyscroll group to render the map and Hero.
    """
    filename = get_map(MAP_FILENAME)

    counter = 1
    counter2 = 1

    def __init__(self, state): 
        if state == False:
            screenMode = pygame.RESIZABLE
            # true while running.
            self.running = False
            self.clock = pygame.time.Clock()
            # create all the directio variables
            self.direction = "still"
            self.fps = 1000

            self.bypass = False

            entityPos1, heroPos1 = False, False
                     
            # load data from pytmx
            tmx_data = load_pygame(self.filename)

            mapPlay = load_pygame(get_map(FOREST))
            # create new data source for pyscroll
            map_data = pyscroll.data.TiledMapData(mapPlay)
            # setup level geometry with simple pygame rects, loaded from pytmx.
            self.walls = list()
            for object in mapPlay.objects:
                self.walls.append(pygame.Rect(
                    object.x, object.y,
                    object.width, object.height))
            
            # create new renderer (camera)
            self.map_layer = pyscroll.BufferedRenderer(map_data, screen.get_size())
            self.map_layer.zoom = 2

            self.group = PyscrollGroup(map_layer=self.map_layer, default_layer=4)
            self.hero = Hero('Tiles/hero/character_still.png')
            self.hero.position = [1949, 1903]
            # add our hero to the group
            self.group.add(self.hero)
            #self.group.add(self.entity)
            
            self.entVel = (0, 0)
            self.aichar = Hero('Tiles/hero/characterai.png')
            aimapfile = get_map("ai/" +FOREST)
            tmxai_data = load_pygame(aimapfile)
            mapai_data = pyscroll.data.TiledMapData(tmxai_data)
            # creates new 'camera'
            self.mapai_layer = pyscroll.BufferedRenderer(mapai_data, (480, 600))
            self.mapai_layer.zoom = 2
            self.aigroup = PyscrollGroup(map_layer=self.mapai_layer, default_layer=0)
            self.aigroup.add(self.aichar)

    def draw(self, surface, ai_surf):
        self.group.center(self.hero.rect.center)
        self.aigroup.center(self.hero.rect.center)
        # draw the map and all sprites
        self.group.draw(surface)
        self.aigroup.draw(ai_surf)

    def handle_input(self, keyset):
        """ Handle pygame input events
        """
        keyset = "game"
        poll = pygame.event.poll
        
        event = poll()
        while event:
            #print("Event")
            if event.type == QUIT:
                self.running = False
                pygame.quit()
                break
            
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pickle.dump(stats, open(os.path.join("data", "saves", "save.dat"), "wb"))
                    pickle.dump(inventory, open(os.path.join("data", "saves", "inventory.dat"), "wb"))
                    self.running = False
                    pygame.quit()
                    print(" ")
                    sleep(0.5)
                    print("Shutdown... Complete")
                    sys.exit()
                    break

                elif event.key == K_KP2:
                    self.map_change(FOREST)
                    self.map = "forest"
            event = poll()
        # using get_pressed is slightly less accurate than testing for events
        # but is much easier to use.
        if keyset == "game":
            pressed = pygame.key.get_pressed()
            if pressed[K_UP]:
                self.hero.velocity[1] = -HERO_MOVE_SPEED
                self.direction = "up"
                self.direction2 = "up"
            elif pressed[K_DOWN]:
                self.hero.velocity[1] = HERO_MOVE_SPEED
                self.direction = "down"
                self.direction2 = "down"
            elif pressed[K_w]:
                self.hero.velocity[1] = -HERO_SPRINT_SPEED
                self.direction = "up"
                self.direction2 = "up"
            elif pressed[K_s]:
                self.hero.velocity[1] = HERO_SPRINT_SPEED
                self.direction = "down"
                self.direction2 = "down"
            else:
                self.hero.velocity[1] = 0
                self.direction2 = "still"
            if pressed[K_LEFT]:
                self.hero.velocity[0] = -HERO_MOVE_SPEED
                self.direction = "left"
                self.direction1 = "left"
            elif pressed[K_RIGHT]:
                self.hero.velocity[0] = HERO_MOVE_SPEED
                self.direction = "right"
                self.direction1 = "right"
            elif pressed[K_a]:
                self.hero.velocity[0] = -HERO_SPRINT_SPEED
                self.direction = "left"
                self.direction1 = "left"
            elif pressed[K_d]:
                self.hero.velocity[0] = HERO_SPRINT_SPEED
                self.direction = "right"
                self.direction1 = "right"
            else:
                self.hero.velocity[0] = 0
                self.direction1 = "still"

            if self.direction1 == "still" and self.direction2 == "still":
                self.direction = "still"

    def update(self, dt):
        """ Tasks that occur over time should be handled here
        """
        self.group.update(dt)

        # check if the sprite's feet are colliding with wall
        # sprite must have a rect called feet, and move_back method,
        # otherwise this will fail
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back(dt)

    def save_screenshot(self, surface, dev):
        try:
            pressed = dev.active_keys()
            key = ecodes.KEY[pressed[0]]
            key = key.lstrip("KEY_")
            print(key)
            with mss.mss() as sct:
                # The screen part to capture
                monitor = {'top': 30, 'left': 5, 'width': 480, 'height': 560}
                output = 'training_data/{}.{}.jpg'.format(key, self.counter)

                # Grab the data
                sct_img = sct.grab(monitor)

                # Save to the picture file
                mss.tools.to_png(sct_img.rgb, sct_img.size, output)
                #print(output)

            self.counter += 1
        except IndexError:
            key = "None"
                    
    def run(self):
        start = 0
        screenMode = pygame.RESIZABLE

        clock = pygame.time.Clock()
        self.running = True
        
        self.index_counter = 12501
        self.dev = InputDevice('/dev/input/event4')

        debug = False
        dispWidth, dispHeight = 1024, 768
        self.menu = "game"
        game_time = pygame.time.get_ticks()
        playTime = font.render("Timer: ", False, pygame.Color('white'))        
        minutes = 0

        self.map = "maps/forest.tmx"
        self.map = self.map.lstrip("m") # Fix that stupid bug that changes "maze1" to "ze1"
        self.map = self.map.lstrip("aps/")

        try:
            while self.running:
                dt = (clock.tick() / 500)
                clock.tick(self.fps)

                if self.counter2 % 7 == 0:
                    pass
                else:
                    self.counter += 1
                    guiX = (dispWidth / 2) - 175
                    guiY = (dispHeight / 2) - 165
                    self.group.remove(self.hero)
                    #self.group.remove(self.entity)
                    self.group.empty()
                    self.group.add(self.hero)
                    #self.group.add(self.entity)

                pygame.display.update()
                self.handle_input(self.menu)
                self.update(dt)
                self.draw(screen, ai_surf)
                ai_surf.blit(load_image(os.path.join("Tiles", "hero", "characterai32.png")),( 100, 150)) #200, 300
                self.draw(ai_surf, screen)
                screen.blit(ai_surf, (0, 0))
                Process(target = self.save_screenshot(ai_surf, self.dev)).start()
                start = systime()
                

        except KeyboardInterrupt:
            self.running = False
            pygame.quit()


if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    screen = init_screen(240, 300, pygame.RESIZABLE) # 1024, 700
    ai_surf = pygame.surface.Surface((240, 300))
    pygame.display.set_caption('Quest - An epic journey.')
    font = pygame.font.Font(os.path.join('data', 'GameFont.ttf'), 20)
    done = False
    gameStart = systime()
             
    try:
        game = QuestGame(False)
        #import cProfile
        #cProfile.run('game.run()')
        game.run()
    except:
        pygame.quit()
        raise
