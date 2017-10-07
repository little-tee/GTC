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

##import pygame_sdl2
##pygame_sdl2.import_as_pygame()


from keras.models import Sequential
from keras.models import load_model
from keras.optimizers import SGD
from keras.layers import Dense, Conv2D, Conv1D, MaxPooling2D, MaxPooling1D
from keras.layers import Activation, Dropout, Flatten
from keras.layers import Convolution2D, Reshape, InputLayer
from keras.utils import np_utils
from keras.utils import plot_model
import keras


#Imports uncategorised modules.
from time import sleep
from time import time as systime
from math import *
import pickle
import random
from w_random import WeightedRandomizer
from multiprocessing import Process
from evdev import InputDevice, ecodes
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
FOREST = os.path.join('forest.tmx')

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

statslist = ["height",
            "weight",
            "strength",
            "speed",
            "skill"]

enemystats = {"height" : 100,
                "weight" : 100,
                "strength" : 100,
                "speed" : 100,
                "skill" : 100}

playerStats = {"height" : 100,
                "weight" : 100,
                "strength" : 100,
                "speed" : 100,
                "skill" : 100}

# Should really be improved
forward = os.path.join("data", "Tiles", "character", "walking_forward.png")
down = os.path.join("data", "Tiles", "character", "walking_down.png")
left = os.path.join("data", "Tiles", "character", "walking_left.png")
right = os.path.join("data", "Tiles", "character", "walking_right.png")

clock = pygame.time.Clock()

screenMode = pygame.RESIZABLE

# Store these in pickles later on
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
            screenMode = pygame.RESIZABLE
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
            self.aichar = Hero('Tiles/hero/characterai.png')
            aimapfile = get_map("ai/" +stats['map'])
            tmxai_data = load_pygame(aimapfile)
            mapai_data = pyscroll.data.TiledMapData(tmxai_data)
            # creates new 'camera'
            self.mapai_layer = pyscroll.BufferedRenderer(mapai_data, (480, 600))
            self.mapai_layer.zoom = 2
            self.aigroup = PyscrollGroup(map_layer=self.mapai_layer, default_layer=0)
            self.aigroup.add(self.aichar)


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

    def map_change(self, map): # Does what it says on the tin
            mapfile = get_map(map)
            tmx_data = load_pygame(mapfile)
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
            self.hero.position = self.map_layer.map_rect.center

            self.map = stats['map'][:-4].lower()
            self.map = self.map.lstrip("m") # Fix that stupid bug that changes "maze1" to "ze1"
            self.map = self.map.lstrip("aps/")



            
            aimapfile = get_map("ai/" +map )
            tmxai_data = load_pygame(aimapfile)
            mapai_data = pyscroll.data.TiledMapData(tmxai_data)
            
            # creates new 'camera'
            self.mapai_layer = pyscroll.BufferedRenderer(mapai_data, (480, 600))
            self.mapai_layer.zoom = 2
            self.aigroup = PyscrollGroup(map_layer=self.map_layer, default_layer=4)

            #creates a new Hero to go on our new camera
##            self.hero = Hero('Tiles/hero/character_still.png')
##            self.hero.position = self.map_layer.map_rect.center
##
##            self.map = stats['map'][:-4].lower()
##            self.map = self.map.lstrip("m") # Fix that stupid bug that changes "maze1" to "ze1"
##            self.map = self.map.lstrip("aps/")


            
    def switcher(self): # Bunch of IF statements to decide if we're at a door or not, the changes the map
        if len(objectX) == len(objectY) == len(targetPosX) == len(targetPosY) == len(currentMap) == \
           len(targetMap) == len(animationDirection) == len(targetMapFile) == len(objectType):
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
                                break
                            elif objectType[i] == "chest":
                                keyset, self.menu = "chest", "chest"                  
                                if used[i] == False:
                                    if chestContents[i] == None and used[i] == False:
                                        used[i] = True
                                        pickle.dump(used, open(os.path.join("data", "saves", "used.dat"), "wb"))
                                        chestContents[i] = self.genchests()
                                        pickle.dump(chestContents, open(os.path.join("data", "saves", "chestContents.dat"), "wb"))
                                else:
                                    pass
                                self.chestNo = i
                    else: # There used to be code here
                        pass
                        
                else:
                    pass
        else:
            print("Error: Invalid number of object entries.")


    def draw(self, surface, ai_surf):
        self.group.center(self.hero.rect.center)
        self.aigroup.center(self.hero.rect.center)
        # draw the map and all sprites
        self.group.draw(surface)
        self.aigroup.draw(ai_surf)

    def handle_input(self, keyset, move_direction):
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

                    elif event.key == K_KP0:
                        self.switcher()
                        pass

                    elif event.key == K_e:
                        self.menu = "inventory"
                        pass

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


                if keyset == "inventory":
                    if event.key == K_ESCAPE:
                        self.menu = "game"
                        pass

                    if event.key == K_r:
                        self.genchests()
                    

                if keyset == "chest" or keyset == "attack":
                    if event.key == K_ESCAPE:
                        self.menu = "game"
                        pass

                    if event.key == K_r:
                        chestContents[self.chestNo] = self.genchests()

                    if event.key == K_t:
                        if taken[self.chestNo] != True:
                            self.takeChest()
                            taken[self.chestNo] = True
                            pickle.dump(taken, open(os.path.join("data", "saves", "taken.dat"), "wb"))
                            

                #Basically just debug keys
                elif event.key == K_KP1:
                    self.menu = "game"
                    #print("Game")
                    pass

                elif event.key == K_KP2:
                    self.map_change(FOREST)
                    self.map = "forest"

                elif event.key == K_KP3:
                    self.menu = "inventory"
                    #print("Inventory")
                    pass

                elif event.key == K_KP4:
                    self.genEnemies()                   
                    pass

                elif event.key == K_KP5:
                    self.genEnemies()
                    self.menu = "attack"
                    pass

                elif event.key == K_KP6:
                    print("X :" +str(self.hero.position[0]) +", Y: " +str(self.hero.position[1]) +", Map: "+ self.map)
                    pass

                elif event.key == K_KP7:
                    print(str(pygame.mouse.get_pos()))
                    pass
                
                elif event.key == K_KP8:
                    sleep(0.5)

                elif event.key == K_KP9:
                    pass

                elif event.key == K_F11:
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
            if pressed[K_UP] or move_direction == "UP":
                self.hero.velocity[1] = -HERO_MOVE_SPEED
                self.direction = "up"
                self.direction2 = "up"
            elif pressed[K_DOWN] or move_direction == "DOWN":
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
            if pressed[K_LEFT] or move_direction == "LEFT":
                self.hero.velocity[0] = -HERO_MOVE_SPEED
                self.direction = "left"
                self.direction1 = "left"
            elif pressed[K_RIGHT] or move_direction == "RIGHT":
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

        #print(wr.random())
        
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
                #print(item)
            chest.append(item)

        return chest

    def genEnemies(self):
        for i in range(len(stats)):
            #enemystats[statslist[i]] = random.randint(playerStats[statslist[i]] - 10, \
                                          #playerStats[statslist[i]] + 10)
            enemystats[statslist[i]] = random.randint(100 - 10, \
                                          100 + 20)
        print(enemystats)
        print(playerStats)
        print(self.attack())


    def attack(self):
        wins, losses = 0, 0
        for i in range(len(enemystats)):
            if enemystats[statslist[i]] > playerStats[statslist[i]]:
                losses += 1
            else:
                wins += 1
        if wins > losses:
            return True
        else:
            return False
            
        
    def blit_inventory(self, screenMode):
        xCounter, counter, OverCounter = 0, 0, 0
        if screenMode != "game":
            dt = (clock.tick() / 500)
            clock.tick(self.fps)
            dispWidth, dispHeight = pygame.display.get_surface().get_size()
            guiX = (dispWidth / 2) - 175
            guiY = (dispHeight / 2) - 165
            screen.blit(load_image(os.path.join("images", "gui", "transparent.png")),( 0, 0))
            screen.blit(load_image(os.path.join("images", "gui", screenMode +".png")),(guiX, guiY))
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

        if screenMode == "attack":
            picture = load_image(os.path.join("Tiles", "hero", "walking_down", "walking_down1.png"))
            picture = pygame.transform.scale(picture, (100, 100))
            rect = picture.get_rect()
            rect = rect.move((guiX + 50, guiY + 28))
            screen.blit(picture, rect)
            for i in range(len(stats)):
                text = font.render(statslist[i] + " : " + str(enemystats[statslist[i]]), True, pygame.Color('black'))
                screen.blit(text, (guiX + 172, guiY + 45 + i + 20*i))
            
            pass
                
    def takeChest(self):
        #print(len(chestContents[self.chestNo]))
        if len(inventory) < 27:  
            if chestContents[self.chestNo] != None:
                for i in range(0, (len(chestContents[self.chestNo]))):
                    #print(i)
                    inventory.append(chestContents[self.chestNo][i])
                chestContents[self.chestNo][:] = []
            pickle.dump(chestContents, open(os.path.join("data", "saves", "chestContents.dat"), "wb"))
            

    def save_screenshot(self, surface, model):
        try:
            if self.total == "total":
                pass
        except AttributeError:
            self.total = 0
            self.counter42 = 0
            self.ai_direction = None
            print("RESET")
            self.recent_actions = [0]
            for i in range(0, 25):
                self.recent_actions.append(0)
                print("loooooooop")
                if len(self.recent_actions) >= 25:
                    break
            self.ai_movement = 0
            self.new_counter = "Null"
        rgbarray = surfarray.array3d(ai_surf)
        rgbarray = cv2.resize(rgbarray, (32, 32)).flatten()
        #print("rgbarray done")
        prediction = model.predict(rgbarray.reshape((1, 3072)), batch_size=1)/1
        prediction = prediction.argmax(axis=1)
        #print(prediction)
        random_num = random.randint(0, 50)
        if random_num == 2 and self.counter42 == 0:
            self.random42 = random_num
            self.counter42 = random.randint(0, 50)
            self.total = self.counter42
            print("42\n")
        elif self.total == self.counter42:
            self.ai_direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
            print("Direction Chosen: {}".format(self.ai_direction))
            self.counter42 = self.counter42 - 1
            print(self.counter42)
        elif self.counter42 > 0:
            print("Counter > 0")
            self.counter42 =- 1
        elif self.counter42 == 0:
            self.random42 = 0
            print("Done")
##        else:
        if self.new_counter == "Null":
            print(self.new_counter)
            print(len(self.recent_actions), self.ai_movement)
            if self.ai_movement == 24:
                self.ai_movement = -1
            self.ai_movement += 1
            random_num = random.randint(0, 2)
            if str(prediction) == "[0]" and random_num == 0:
                self.ai_direction = "DOWN"
            elif str(prediction) == "[1]" and random_num == 0:
                self.ai_direction = "LEFT"
            elif str(prediction) == "[2]" and random_num == 0:
                self.ai_direction  = "RIGHT"
            elif str(prediction) == "[3]" and random_num == 0:
                self.ai_direction = "UP"
            print("AI: " +self.ai_direction)
            self.recent_actions[self.ai_movement] = self.ai_direction
        if all(x==self.recent_actions[0] for x in self.recent_actions):
            self.new_counter = 20
            if self.ai_direction == "LEFT":
                self.ai_direction == "RIGHT"
                print("GOING RIGHT")
            if self.ai_direction == "RIGHT":
                self.ai_direction == "LEFT"
                print("GOING LEFT")
            if self.ai_direction == "UP":
                self.ai_direction == "DOWN"
                print("GOING DOWN")
            if self.ai_direction == "DOWN":
                self.ai_direction == "UP"
                print("GOING UP")
            print(self.ai_direction)
            print(self.ai_movement)
            self.recent_actions[self.ai_movement] = self.ai_direction
            self.new_counter -= 1
            if self.new_counter <= 1:
                print("loooooooop")
                for i in range(0, 25):
                    self.recent_actions[i] = 0
                    #print(self.recent_actions)
                    self.new_counter = "Null"

            print(self.recent_actions)
            #self.ai_direction == "RIGHT"
        os.system("echo Direction: {}".format(self.ai_direction))
        self.move_direction = self.ai_direction
        pass
                
    def run(self):
        start = 0
        screenMode = pygame.RESIZABLE

        oldPlay = stats['playTime']
        clock = pygame.time.Clock()
        self.running = True

        self.move_direction = None
        model = load_model("DENSE 265 - 48.model")
        
        self.index_counter = 12501
        self.dev = InputDevice('/dev/input/event4')

        debug = False
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
                    location = font.render("Position: " + str(round(round(self.hero.position[0], -1) / 10)) + ", " + str(round(round(self.hero.position[1], -1) / 10)), False, pygame.Color('blue'))
                    mapdebug = font.render("Map Name: " + str(self.map), False, pygame.Color('blue'))
                    minutes = seconds // 60
                    secondsDisp = seconds % 60
                    if minutes < 1:
                        minutes = 0
                    if secondsDisp == 60:
                        secondsDisp = 0
                        minutes += 1
                    fps = font.render("FPS:" + str(int(clock.get_fps())), False, pygame.Color('blue'))
                    screen.blit(fps, (50, 50))
                    screen.blit(playTime, (50,100))
                    screen.blit(location, (50,75))
                    screen.blit(mapdebug, (50, 125))

                    playTime = font.render("Timer: " + str(floor(minutes)) + " : " + str(round(secondsDisp)), True, pygame.Color('blue'))
                    screen.blit(playTime, (50,100))    


                self.blit_inventory(str(self.menu))
                pygame.display.update()
                #ai_surf.blit(screen, (0, 0))
                #pygame,display.flip()
                self.handle_input(self.menu, self.move_direction)
                self.update(dt)
                self.draw(screen, ai_surf)
                ai_surf.blit(load_image(os.path.join("Tiles", "hero", "characterai32.png")),( 100, 150)) #200, 300
                #self.draw(ai_surf, screen)
                screen.blit(ai_surf, (0, 0))
                end = systime()
                #print("Loop took {} seconds".format(end-start))
                #Thread(target = self.save_screenshot(ai_surf)).start()
                Process(target = self.save_screenshot(ai_surf, model)).start()
                start = systime()
                #array_img = pygame.surfarray.array2d(ai_surf)
                
                

        except KeyboardInterrupt:
            self.running = False
            pygame.quit()


if __name__ == "__main__":
    allVars = [objectX, objectY, targetPosY, targetPosX, targetMap, currentMap, animationDirection, targetMapFile]
    pygame.init()
    pygame.font.init()
    screen = init_screen(240, 300, pygame.RESIZABLE) # 1024, 700
    ai_surf = pygame.surface.Surface((240, 300))
    pygame.display.set_caption('Quest - An epic journey.')
    font = pygame.font.Font(os.path.join('data', 'GameFont.ttf'), 20)
    done = False
    gameStart = systime()
    inventory = pickle.load(open("data/saves/inventory.dat", "rb"))
    stats = pickle.load(open(os.path.join("data", "saves", "save.dat"), "rb"))
    used = pickle.load(open(os.path.join("data", "saves", "used.dat"), "rb"))
    chestContents = pickle.load(open(os.path.join("data", "saves", "chestContents.dat"), "rb"))
    taken = pickle.load(open(os.path.join("data", "saves", "chestContents.dat"), "rb"))
    vars = ["objectX", "objectY", "targetPosY", "targetPosX", "targetMap", "currentMap", "animationDirection", \
            "targetMapFile", "objectType"]



    for i in range(0, len(vars)):
        with open ("data/saves/" +vars[i], "r") as myfile:
            data = myfile.readlines()
            splitList = data[0].split(", ")
            #print(splitList)
            for j in range(0, len(splitList)):
                eval(vars[i]).append(splitList[j].rstrip())
                
    try:
        game = QuestGame(False)
        #import cProfile
        #cProfile.run('game.run()')
        game.run()
    except:
        pygame.quit()
        raise
