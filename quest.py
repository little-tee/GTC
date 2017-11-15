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
import textwrap
import subprocess
from multiprocessing import Process
import screeninfo
import db_interface
import sqlite3

#Import pygame.
import pygame
from pygame.locals import *
from pygame import font, display, time, image, sprite, event, key

#Imports pytmx.
from pytmx.util_pygame import load_pygame
import pytmx

#Import pyscroll.
import pyscroll
import pyscroll.data
from pyscroll.group import PyscrollGroup

# Define configuration variables here.
RESOURCES_DIR = 'data'

TIME_PLAYING = 0

HERO_MOVE_SPEED = 150  # pixels per second.
HERO_SPRINT_SPEED = 2000
MAP_FILENAME = os.path.join('forest.tmx')
FOREST = os.path.join('forest.tmx')

randint = random.randint
choice = random.choice

# All of the lists that must be appended to later on
objectX = []
objectY = []
targetPosX = []
targetPosY = []
targetMap = []
currentMap = []
animationDirection = []
targetMapFile = []
used = []
objectType = []
chest = []

# Should really be improved
forward = os.path.join("data", "Tiles", "character", "walking_forward.png")
down = os.path.join("data", "Tiles", "character", "walking_down.png")
left = os.path.join("data", "Tiles", "character", "walking_left.png")
right = os.path.join("data", "Tiles", "character", "walking_right.png")

clock = pygame.time.Clock()

screenMode = pygame.RESIZABLE

# Store these in pickles later on
attack_stats = {"level":0,
                "skill" : 0,
                "strength" : 0,
                "speed" : 0,
                "health" : 0,
                "blocking": 0,
                "attack" : None}
enemy_stats = {"level":0,
                "skill" : 0,
                "strength" : 0,
                "speed" : 0,
                "health" : 0,
                "blocking": 0,
                "attack" : None}
attack_stats_types = ['level', 'skill', 'strength', 'speed', 'health', 'blocking', 'attack']
attack_types = ["bow", "fist", "headbutt", "psycological", "magic", "sword"]

items = {"1": "sword",
         "2": "axe",
         "3": "bow",
         "4": "shovel",
         "5": "apple",
         "6": "boots",
         "7": "chestplate",
         "8": "chicken",
         "9": "helmet",
         "10": "steak",
         "11": "trousers"
         }

itemsProbability = {"1": 10, "2": 20, "3": 12, "4": 25, "5": 100, "6": 7,\
                    "7": 4, "8": 75, "9": 7, "10": 50, "11": 5}

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

def load_font(size, filename=os.path.join('data', 'GameFont.ttf')):
    font = pygame.font.Font(filename, size)
    return font

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



class Entity(pygame.sprite.Sprite):
    """ Our Entity

    The Entity has three collision rects, one for the whole sprite "rect" and
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
        QuestGame.bypass = True


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
            self.fullscreen = False
            # true while running.
            self.running = False
            self.clock = pygame.time.Clock()
            # create all the directio variables
            self.direction = "still"
            self.EntityDirection = "still"
            self.EntityDirection1, self.EntityDirection2 = "still", "still"  
            self.fps = 1000

            self.bypass = False

            entityPos1, heroPos1 = False, False
                     
            # load data from pytmx
            tmx_data = load_pygame(self.filename)
            self.tmx_data = tmx_data

            mapPlay = load_pygame(get_map(stats['map']))
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
            self.entity = Entity('Tiles/hero/character_still.png')
            self.hero.position = stats['pos']
            self.entity.position = stats['pos']
            # add our hero to the group
            self.group.add(self.hero)
            #self.group.add(self.entity)
            
            self.entVel = (0, 0)

    def deep_thought(self): # The 'AI' function, needs work
        if self.counter2 % 75 == 0 or self.bypass == True:
            self.bypass = False
            if random.randint(0, 1) == 1:
                self.entity.velocity[0], self.entity.velocity[1] = 0, 0
            movement = random.choice(["self.entity.velocity[0] = -45; self.EntityDirection = 'left'; self.EntityDirection2 = 'left'",
                                      "self.entity.velocity[0] = 45; self.EntityDirection = 'right'; self.EntityDirection2 = 'right'",
                                      "self.entity.velocity[1] = -45; self.EntityDirection = 'up'; self.EntityDirection1 = 'up'",
                                      "self.entity.velocity[1] = 45; self.EntityDirection = 'down'; self.EntityDirection1 = 'down'"])
            exec(movement)
            
    def EntityAnimation(self, direction, number, character="hero"):
        self.entVel = self.entity.velocity
        
        self.counter += 1
        if self.EntityDirection1 == "still" and self.EntityDirection2 == "still":
            if self.EntityDirection == "left":
                self.entity = Entity('Tiles/' +character +'/walking_left/walking_left1.png')
            if self.EntityDirection == "right":
                self.entity = Entity('Tiles/' +character +'/walking_right/walking_right1.png')
            if self.EntityDirection == "up":
                self.entity = Entity('Tiles/' +character +'/walking_up/walking_up1.png')
            if self.EntityDirection == "down":
                self.entity = Entity('Tiles/' +character +'/walking_down/walking_down1.png')
        else:
            self.entity = Entity('Tiles/' +character +'/walking_' +direction +'/walking_' +direction +str(number) +'.png')
        self.entity.velocity = self.entVel

    def EntMoveBack(self):
        #self.deep_thought(self, True) # Comment this to disable the 'AI'
        pass

    def map_change(self, map, target=False): # Does what it says on the tin
            mapfile = get_map(map)
            tmx_data = load_pygame(mapfile)
            self.tmx_data = tmx_data
            map_data = pyscroll.data.TiledMapData(tmx_data)
            self.walls = list()
            for object in tmx_data.objects:
                self.walls.append(pygame.Rect(
                    object.x, object.y,
                    object.width, object.height))

            # creates new 'camera'
            self.map_layer = pyscroll.BufferedRenderer(map_data, screen.get_size())
            self.map_layer.zoom = 2
            self.group = PyscrollGroup(map_layer=self.map_layer, default_layer=4)

            #creates a new Hero to go on our new camera
            self.hero = Hero('Tiles/hero/character_still.png')
            try:
                self.hero.position = (target)
            except TypeError:
                self.hero.position = self.map_layer.map_rect.center
            self.map = stats['map'][:-4].lower()
            self.map = self.map.lstrip("m") # Fix that stupid bug that changes "maze1" to "ze1"
            self.map = self.map.lstrip("aps/")
            
    def switcher(self): # Bunch of IF statements to decide if we're at a door or not, then changes the map.
        if len(objectX) == len(objectY) == len(targetPosX) == len(targetPosY) == len(currentMap) == \
           len(targetMap) == len(animationDirection) == len(targetMapFile) == len(objectType):
            heroPos = [0, 0]
            heroPos[0], heroPos[1] = self.hero.position[0], self.hero.position[1]
            for i in range(len(objectX)):
                if self.map == currentMap[i]:
                    if self.hero.position[0] - 15 <= int(objectX[i]) <= self.hero.position[0] + 15:
                        if self.hero.position[1] - 15 <= int(objectY[i]) <= self.hero.position[1] + 15:
                            if objectType[i] == "door":
                                used[i] = True
                                self.map_change(targetMapFile[i])
                                self.map = targetMap[i]
                                stats['map'] = targetMapFile[i]
                                heroPos = (int(targetPosX[i]), int(targetPosY[i]))
                                self.animation(animationDirection[i], 1)
                                self.hero.position = heroPos
                                return False
                            elif objectType[i] == "chest":
                                keyset, self.menu = "chest", "chest"                  
                                if used[i] == False:
                                    if chestContents[i] == None and used[i] == False:
                                        used[i] = True
                                        pickle.dump(used, open(os.path.join("data", "saves", "used.dat"), "wb"))
                                        chestContents[i] = self.genchests()
                                        pickle.dump(chestContents, open(os.path.join("data", "saves", "chestContents.dat"), "wb"))
                                self.chestNo = i                    
                            return False
                        
    def generate_surrounding_maps(self):
        heroPos = [0, 0]
        heroPos = self.hero.position
        if int(self.hero.position[0]) in range((self.tmx_data.width*32)-64,
                                                 (self.tmx_data.width*32)):
            target = (32, heroPos[1])
            self.grid[0] = self.grid[0]+1
            try:
                self.map_change(str(self.grid[0]+1) +", "+ str(self.grid[1]) +".tmx",
                                target)
                self.map = str(self.grid).lstrip("[").rstrip("]")
                stats['map'] = self.map + ".tmx"
                self.animation("right", 1)
                target = (32, heroPos[1])
                #self.hero.position = target
            except FileNotFoundError:
                self.generate_new_map(4, 16, 2, self.grid, target)
        elif int(self.hero.position[1]) in range((self.tmx_data.height*32)-64,
                                                 self.tmx_data.width*32):
            target = (heroPos[0], 32)
            self.grid[1] = self.grid[1]+1
            try:
                self.map_change(str(self.grid[0]) +", "+ str(self.grid[1]+1) +".tmx",
                                target)
                self.map = str(self.grid).lstrip("[").rstrip("]")
                stats['map'] = self.map + ".tmx"
                heroPos[0], heroPos[1] = self.hero.position[0], self.hero.position[1]
                self.animation("up", 1)
                
            except FileNotFoundError:
                self.generate_new_map(4, 16, 2, self.grid, target)
        elif int(self.hero.position[0]) in range(0, 64):
            target = (self.tmx_data.width*32 - 32, heroPos[1])
            self.grid[0] = self.grid[0]-1
            try:
                self.map_change(str(self.grid[0]-1) +", "+ str(self.grid[1]) +".tmx",
                                target)
                self.map = str(self.grid).lstrip("[").rstrip("]")
                stats['map'] = self.map + ".tmx"
                heroPos[0], heroPos[1] = self.hero.position[0], self.hero.position[1]
                self.animation("left", 1)
                #self.hero.position = target
            except FileNotFoundError:
                self.generate_new_map(4, 16, 2, self.grid, target)
        elif int(self.hero.position[1]) in range(0, 64):
            target = (heroPos[0], self.tmx_data.height*32 - 32)
            self.grid[1] = self.grid[1]-1
            try:
                self.map_change(str(self.grid[0]) +", "+ str(self.grid[1]-1) +".tmx",
                                target)
                self.map = str(self.grid).lstrip("[").rstrip("]")
                stats['map'] = self.map + ".tmx"
                heroPos[0], heroPos[1] = self.hero.position[0], self.hero.position[1]
                self.animation("down", 1)
                #self.hero.position = target
            except FileNotFoundError:
                self.generate_new_map(4, 16, 2, self.grid, target)
        else:
            pass

    def generate_new_map(self, octaves, freq, area, target, position):
        command = "{}/lib/generate/__init__.py".format(os.getcwd())
        if sys.platform.startswith('win32'):
            executeable = ("Python35\python.exe")
            
        elif sys.platform.startswith('linux'):
            executeable = ("python3.5")

        for y in range(self.grid[1] + eval("-"+ str(area)),self.grid[1] +  area):
            for x in range(self.grid[0] + eval("-"+ str(area)),self.grid[0] +  area):
                if os.path.isfile("data/maps/"+str(x)+", "+str(y)+".tmx"):
                    pass
                else:
                    p = subprocess.Popen([executeable, command, ("data/maps/"+
                                                    str(x)+", "+str(y)+".tmx"),
                                      str(octaves), str(freq), str(x), str(y)],
                                         close_fds=True)
        try:
            if p is not None:
                disp_width, disp_height = pygame.display.get_surface().get_size()
                #self.blit_inventory("speach", "Generating Map... Please Wait...")
                self.speach(disp_width, disp_height,
                            "Generating Map... Please Wait...") 
                pygame.display.update()
                p.wait()
                self.map_change((str(target[0])+", "+str(target[1])+".tmx"), position)
                self.map = str(self.grid).lstrip("[").rstrip("]")
                stats['map'] = self.map + ".tmx"
        except UnboundLocalError:
            pass
                    
    def draw(self, surface):
        self.group.center(self.hero.rect.center)
        # draw the map and all sprites
        self.group.draw(surface)

    def speach(self, dispWidth, dispHeight, text):
##        text = "Laudem bonorum salutandi pri te, tollit melius delicata mel cu,\
##                eu mea ullum legimus. Probo debitis te vel. Labores vulputate \
##                argumentum sea id. Cibo vitae vocent eos no, ne odio molestiae\
##                duo."
        screen.blit(pygame.transform.scale(load_image(os.path.join(
            "images", "gui", "speach.png")), (dispWidth, 150)), (0, dispHeight-150))
        text = textwrap.wrap(text, width=95)
        for i, line in enumerate(text): 
            text_blit = pixel_font.render(line, False, pygame.Color('white'))
            screen.blit(text_blit, (60, dispHeight-110 + 25*i))

    def map_generate(self, output, octaves, freq, x, y):
        command = "{}/lib/generate/__init__.py".format(os.getcwd())
        
        if sys.platform.startswith('win32'):
            executeable = ("Python35\python.exe")
            
        elif sys.platform.startswith('linux'):
            executeable = ("python3.5")
            
        subprocess.Popen([executeable, command, output, str(octaves), str(freq),
                          str(x), str(y)],close_fds=True) 

    def handle_input(self, keyset):
        """ Handle pygame input events
        """
        
        poll = pygame.event.poll
        
        event = poll()
        while event:
            if event.type == QUIT:
                self.running = False
                pygame.quit()
                break

            elif event.type == KEYDOWN:
                

                if keyset == "game":
                    if event.key == K_EQUALS:
                        self.map_layer.zoom += .25

                    elif event.key == K_MINUS:
                        value = self.map_layer.zoom - .25
                        if value > 0:
                            self.map_layer.zoom = value
                        else:
                            self.map_layer.zoom = 0.1

                    elif event.key == K_KP0:
                        try:
                            if self.switcher() == True:
                                self.generate_surrounding_maps()
                        except FileNotFoundError:
                            print("Exception Caught")
                        pass

                    elif event.key == K_e:
                        self.menu = "inventory"
                        pass

                    if event.key == K_ESCAPE:
                        for i in attack_stats_types:
                            stats[i] = attack_stats[i]
                        pickle.dump(stats, open(os.path.join("data", "saves", "save.dat"), "wb"))
                        pickle.dump(inventory, open(os.path.join("data", "saves", "inventory.dat"), "wb"))
                        self.running = False
                        pygame.quit()
                        print(" ")
                        sleep(0.5)
                        print("Shutdown... Complete")
                        sys.exit()
                        break

                if keyset != "game":
                    if event.key == K_ESCAPE:
                        self.menu = "game"
                        pass

                if keyset == "inventory":
                    if event.key == K_r:
                        self.genchests()

                if keyset == "chest":
                    if event.key == K_r:
                        chestContents[self.chestNo] = self.genchests()

                    if event.key == K_t:
                        if taken[self.chestNo] != True:
                            self.takeChest()
                            taken[self.chestNo] = True
                            pickle.dump(taken, open(os.path.join("data", "saves", "taken.dat"), "wb"))

                if keyset == "attack":
                    pass

                #Basically just debug keys
                if event.key == K_KP1:
                    self.menu = "game"
                    pass

                elif event.key == K_KP2:
                    self.map_change(FOREST)
                    self.map = "forest"

                elif event.key == K_KP3:
                    self.generate_new_map(4, 16, 3)
                    pass

                elif event.key == K_KP4:
                    self.map_generate(str(self.grid[0]) +", "+ str(self.grid[1]) +".tmx", 4, 16.0, self.grid[0], self.grid[1])  
                    pass

                elif event.key == K_KP5:
                    self.enemy_stats = self.gen_enemy(attack_stats, enemy_stats)
                    self.menu = "attack"
                    pass

                elif event.key == K_KP6:
                    print("X :" +str(int(self.hero.position[0])) +
                          ", Y: " +str(int(self.hero.position[1])) +
                          ", Map: "+ self.map)
                    pass

                elif event.key == K_KP7:
                    print(str(pygame.mouse.get_pos()))
                    pass
                
                elif event.key == K_KP8:
                    sleep(0.5)

                elif event.key == K_KP9:
                    editor = db_interface.Editor()
                    conn = sqlite3.connect('data/saves/data.db')
                    c = conn.cursor()

                    for var in vars:
                        exec("del "+var+"[:]")
                        for data in c.execute("SELECT {} FROM csv".format(var)):
                            data = str(data[0])
                            exec("{}.append(\"{}\")".format(var, data))
                            pass

                elif event.key == K_F11:
                    for m in screeninfo.get_monitors():
                        displ = str(m)
                        w, h, mx, c = displ.split(", ")
                        
                    if self.fullscreen:
                        self.fullscreen = False
                        screen = init_screen(1024, 700, pygame.HWSURFACE | pygame.FULLSCREEN )
                    else:
                        self.fullscreen = True
                        screen = init_screen(w, h, pygame.HWSURFACE | pygame.RESIZABLE )

                    pygame.display.toggle_fullscreen()

            elif event.type == VIDEORESIZE:
                self.map_layer.set_size((event.w, event.h))
                dispHeight = event.h
                dispWidth = event.w
                

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

    def animation(self, direction, number):
        if self.direction1 == "still" and self.direction2 == "still":
            if self.direction == "left":
                self.hero = Hero('Tiles/hero/walking_left/walking_left1.png')
            if self.direction == "right":
                self.hero = Hero('Tiles/hero/walking_right/walking_right1.png')
            if self.direction == "up":
                self.hero = Hero('Tileshero/walking_up/walking_up1.png')
            if self.direction == "down":
                self.hero = Hero('Tiles/hero/walking_down/walking_down1.png')

        else:
            self.hero = Hero('Tiles/hero/walking_' +direction +'/walking_' +direction +str(number) +'.png')      

    def genchests(self):

        wr = WeightedRandomizer(itemsProbability)
        
        self.taken = False
        chest.clear()
        numItems = random.randint(1, random.randint(2, 4))
        if random.randint(0, 3) < 1:
            numItems += 1
        elif random.randint(0, 9) < 2:
            numItems += 2
        elif random.randint(0, 18) < 2:
            numItems += 5
        for i in range(0, numItems):
            item = wr.random()
            while item in chest: 
                item = wr.random()
            chest.append(item)

        return chest

    def gen_enemy(self, player_stats, enemy_stat):
        stats = attack_stats_types
        stat = player_stats
        for i in range(len(player_stats)):
            j = stats[i]
            try:
                enemy_stat[stats[i]] = int((stat[j]-(stat[j]*0.2)) + random.randint(0, int(stat[j]*0.4)))
            except TypeError:
                enemy_stat[j] = choice(attack_types)
        return enemy_stat
        pass

    def player_attack():
        type = None
        while type not in attack_types:
            type = input("[ QUESTION ] Enter attack type. ")
            if type not in attack_types:
                print("[ ERROR    ] Attack type {} not found. Must be {}".format(type, attack_types))
            else:
                break
        return type
        pass

    def attack(self, attacker_stats, defender_stats, player_attack_type):
        fraction = attacker_stats['strength'] / defender_stats['blocking']
        print("[ INFO     ] Defender attack type: {}".format(defender_stats['attack']))
        if player_attack_type != defender_stats['attack']:
            if fraction > (0.8 + (randint(0, 40)/100)):
                attacker_stats['health'] -= int(fraction*10)
                pass # Attacker Win
            else:
                defender_stats['health'] -= int(fraction*10)
                pass # Attacker Loss
        elif player_attack_type == attacker_stats['attack']: # Better odds here
            if fraction > (0.9 + (randint(0, 40)/100)):
                attacker_stats['health'] -= int(fraction*10)
                pass # Attacker Win
            else:
                defender_stats['health'] -= int(fraction*10)
                pass # Attacker Loss
        else:
            if fraction > (0.70 + (randint(0, 40)/100)): # Odds are worse here
                attacker_stats['health'] -= int(fraction*10)
                pass # Attacker Win
            else:
                defender_stats['health'] -= int(fraction*10)
                pass # Attacker Loss
        print("[ INFO     ] Attacker: {}  Defender: {}".format(attacker_stats['health'], defender_stats['health']))
        print("[ INFO     ] Health to be lost: {}".format(int(fraction*10)))
        return attacker_stats, defender_stats
        
    def blit_inventory(self, screenMode, speach=None):
        if screenMode != "game":
            xCounter, counter, OverCounter = 0, 0, 0
            dispWidth, dispHeight = pygame.display.get_surface().get_size()
            guiX = (dispWidth / 2) - 175
            guiY = (dispHeight / 2) - 165
            screen.blit(load_image(os.path.join("images", "gui", "transparent.png")),( 0, 0))
            screen.blit(load_image(os.path.join("images", "gui", screenMode +".png")),(guiX, guiY))
        if screenMode == "inventory" or screenMode == "chest":
            dt = (clock.tick() / 500)
            clock.tick(self.fps)

            if len(inventory) > 0:
                for i in range(0, len(inventory)):
                    OverCounter += 1
                    if xCounter >= 9:
                        counter += 1
                        xCounter = 0
                    screen.blit(load_image(os.path.join("images", "items",\
                    str(items[inventory[i]])+".png")), (guiX + 16 + 36*xCounter, guiY + 168 + 36*counter))
                    xCounter += 1
        if screenMode == "chest" and chestContents[self.chestNo] != None:
            itemNo = 0
            for i in range(0, len(chestContents[self.chestNo])):
                screen.blit(load_image(os.path.join("images", "items",\
                            items[str(chestContents[self.chestNo][i])]\
                            +".png")), (guiX + 123 + 36*itemNo,\
                            guiY + 34 + int(35 * (i/3)) - int(35 * (i/3)) % 35))

                if itemNo < 2:
                    itemNo += 1
                else:
                    itemNo = 0

        if screenMode == "speach":
            self.speach(dispWidth, dispHeight, speach)
        if screenMode == "attack":
            picture = load_image(os.path.join("Tiles", "hero", "walking_down", "walking_down1.png"))
            picture = pygame.transform.scale(picture, (100, 100))
            rect = picture.get_rect()
            rect = rect.move((guiX + 50, guiY + 28))
            screen.blit(picture, rect)
            text = font.render("Player : Enemy", True, pygame.Color('black'))
            screen.blit(text, (guiX + 172, guiY + 45))
            text = "Health: "+str(attack_stats['health'])+"    Skill: "+str(attack_stats['skill'])+"    Attack: "+str(attack_stats['attack'])
            text_render = pixel_font.render(text, False, pygame.Color('gray27'))
            screen.blit(text_render, (guiX+20, guiY+290))
            for i, attack in enumerate(attack_types):
                text = load_font(30, "data/PixelFont.ttf").render(attack, False, pygame.Color('black'))
                screen.blit(text, (guiX+172, guiY+25+28*(i+2)))
            #
            if pygame.mouse.get_pressed()[0] == 1:
                #print(pygame.mouse.get_pos())
                mouse_pos = pygame.mouse.get_pos()
                if guiX+160 < mouse_pos[0] and guiX+330 > mouse_pos[0]: 
                    for i, attack in enumerate(attack_types):
                        if guiY+25+28*(i+2) < mouse_pos[1] and (guiY+25+28*(i+2))+28 > mouse_pos[1]:
                            print(attack)
                            self.attack(attack_stats, enemy_stats, attack)
                        else:
                            pass

            pass
                
    def takeChest(self):
        if len(inventory) < 27:  
            if chestContents[self.chestNo] != None:
                for i in range(0, (len(chestContents[self.chestNo]))):
                    #print(i)
                    inventory.append(chestContents[self.chestNo][i])
                chestContents[self.chestNo][:] = []
            pickle.dump(chestContents, open(os.path.join("data", "saves", "chestContents.dat"), "wb"))
            
                
    def run(self):
        screenMode = pygame.RESIZABLE

        oldPlay = stats['playTime']
        clock = pygame.time.Clock()
        self.running = True

        self.grid = [0, 0]

        debug = True
        dispWidth, dispHeight = 1024, 768
        self.menu = "game"
        game_time = pygame.time.get_ticks()
        playTime = font.render("Timer: ", False, pygame.Color('white'))        
        minutes = 0

        self.map = stats['map'][:-4].lower()
        self.map = self.map.lstrip("m") # Fix that stupid bug that changes "maze1" to "ze1"
        self.map = self.map.lstrip("aps/")
        
        try:
            while self.running:
                dt = (clock.tick() / 500)
                clock.tick(self.fps)

                if self.menu == "game":
                    #self.deep_thought()
                    if self.counter2 % 7 == 0:
                        heroPos = self.hero.position
                        self.animation(self.direction, self.counter)
                        self.hero.position = heroPos
                        #entityPos = self.entity.position
                        #self.EntityAnimation(self.EntityDirection, self.counter, "princess")
                        #self.entity.position = entityPos
                        
                        self.counter += 1
                        guiX = (dispWidth / 2) - 175
                        guiY = (dispHeight / 2) - 165
                        
                        self.group.remove(self.hero)
                        #self.group.remove(self.entity)
                        self.group.empty()
                        self.group.add(self.hero)
                        #self.group.add(self.entity)

                self.counter2 += 1
                if self.counter > 8:
                    self.counter = 1

                stats['pos'] = self.hero.position
                currentTime = systime()
                seconds = currentTime - gameStart + oldPlay
                dispWidth, dispHeight = pygame.display.get_surface().get_size()
                stats['playTime'] = seconds

                

                if debug == True and self.counter2 % 1 == 0:
                    location = font.render("Position: " + str(round(round(self.hero.position[0], -1) / 10)) + ", " + str(round(round(self.hero.position[1], -1) / 10)), False, pygame.Color('white'))
                    mapdebug = font.render("Map Name: " + str(self.map), False, pygame.Color('white'))
                    minutes = seconds // 60
                    secondsDisp = seconds % 60
                    if minutes < 1:
                        minutes = 0
                    if secondsDisp == 60:
                        secondsDisp = 0
                        minutes += 1
                    fps = font.render("FPS:" + str(int(clock.get_fps())), False, pygame.Color('white'))
                    screen.blit(fps, (50, 50))
                    screen.blit(playTime, (50,100))
                    screen.blit(location, (50,75))
                    screen.blit(mapdebug, (50, 125))

                    playTime = font.render("Timer: " + str(floor(minutes)) + " : " + str(round(secondsDisp)), True, pygame.Color('white'))
                    screen.blit(playTime, (50,100))    


                self.blit_inventory(str(self.menu))
                      
                pygame.display.update()
                #pygame,display.flip()
                self.handle_input(self.menu)
                self.update(dt)
                self.draw(screen)

        except KeyboardInterrupt:
            self.running = False
            pygame.quit()


if __name__ == "__main__":
    allVars = [objectX, objectY, targetPosY, targetPosX, targetMap, currentMap, animationDirection, targetMapFile]
    pygame.init()
    pygame.font.init()
    screen = init_screen(1024, 700, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
    pygame.display.set_caption('Quest - An epic journey.')
    font = pygame.font.Font(os.path.join('data', 'GameFont.ttf'), 20)
    pixel_font = pygame.font.Font(os.path.join('data', 'PixelFont.ttf'), 24)
    done = False
    gameStart = systime()
    inventory = pickle.load(open("data/saves/inventory.dat", "rb"))
    stats = pickle.load(open(os.path.join("data", "saves", "save.dat"), "rb"))
    used = pickle.load(open(os.path.join("data", "saves", "used.dat"), "rb"))
    chestContents = pickle.load(open(os.path.join("data", "saves", "chestContents.dat"), "rb"))
    taken = pickle.load(open(os.path.join("data", "saves", "chestContents.dat"), "rb"))
    vars = ["objectX", "objectY", "targetPosY", "targetPosX", "targetMap", "currentMap", "animationDirection", \
            "targetMapFile", "objectType"]
    conn = sqlite3.connect('data/saves/data.db')
    c = conn.cursor()
    for i in attack_stats_types:
        attack_stats[i] = stats[i]
    
##    for i in range(0, len(vars)):
##        with open ("data/saves/" +vars[i], "r") as myfile:
##            data = myfile.readlines()
##            splitList = data[0].split(", ")
##            #print(splitList)
##            for j in range(0, len(splitList)):
##                eval(vars[i]).append(splitList[j].rstrip())

    for var in vars:
        for data in c.execute("SELECT {} FROM csv".format(var)):
            data = str(data[0])
            exec("{}.append(\"{}\")".format(var, data))

    for var in vars:
        eval("print({})".format(var))
                
    try:
        game = QuestGame(False)
        #import cProfile
        #cProfile.run('game.run()')
        game.run()
    except:
        pygame.quit()
        raise
