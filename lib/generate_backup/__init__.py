import os.path as path
from sys import path as syspath

syspath1 = __file__[:-12]
syspath.append(syspath1)
syspath2 = __file__[:-22]
syspath.append(syspath2)

import sys, time, os, math
from noise import pnoise2, snoise2
import numpy as np
import tmxlib
from Terrain.CobbleSand import CobbleSand
#from Terrain.SandWater import SandWater
from Terrain.CobbleCracks import CobbleCracks
from Terrain.CracksGrass import CracksGrass

def setup(octaves, freq, x_offset, y_offset):
    array = []
    octaves = int(octaves)
    freq = int(freq) * octaves
        
    for y in range(256):
        temp_array = []
        for x in range(256):
##            temp_array.append(int(pnoise2((x*int(coord[0])) / freq,
##                                          (y*int(coords[1])) / freq,
##                                          octaves) * 196 + 128.0))
            x_pos = x + (x_offset * 256)
            y_pos = y + (y_offset * 256)
            #print(x_pos - x, y_pos - y)
            noise_level = pnoise2(x_pos / freq, y_pos / freq, octaves) * 196 + 128.0
            temp_array.append(noise_level)
        array.append(temp_array)

    total = 0
    for y in range(len(array)):
        for x in array[y]:
            total += x

    highest = 0
    for y in range(len(array)):
        for x in array[y]:
            if x > highest:
                highest = x
                
    #print("[INFO] Highest Mark: " + str(int(highest)))
    #print("[INFO] Average Mark Height: " + str(int(total / (len(array) * len(array[0])))))

    np_array = np.array(array)

    filename = os.path.join(__file__[:-12], 'key.tmx')
    key = tmxlib.Map.open(filename)
    string = open(os.path.join(__file__[:-12], 'maze.tmx'), 'rb').read()
    map = tmxlib.Map.load(string)

    layer = map.layers['Ground']
    key = key.layers['Ground']

    #print("[INFO] Maps Loaded")
    key_pieces = []


    key_pieces.append(42) # Make my helper image work right
    for i in range(0, 768): # 768 is arbitrarily large.
        try:                # We won't get this many tiles
            key_pieces.append(key[i, 0].gid)
        except IndexError:
            break
        
    return array, layer, key_pieces, map

class Terraform:
    def __init__(self, map_array, layer, key_pieces, map):
        self.map_array = map_array
        self.layer = layer
        self.key_pieces = key_pieces
        self.map = map
        
    def generate(self):
        for y in range(len(self.map_array)):
            for x in range(len(self.map_array[0])):
                self.layer = CobbleSand.edges(self, x, y)
                self.layer = CracksGrass.edges(self, x, y)
                self.layer = CobbleCracks.edges(self, x, y)
                pass
        #print("[INFO] Edges Terraformed")

        for y in range(len(self.map_array)):
            for x in range(len(self.map_array[0])):
                self.layer = CobbleSand.t(self, x, y)
                self.layer = CracksGrass.t(self, x, y)
                self.layer = CobbleCracks.t(self, x, y)
                pass
        #print("[INFO] Ts Removed") 

        for y in range(len(self.map_array)):
            for x in range(len(self.map_array[0])):
                self.layer = CobbleSand.corners(self, x, y)
                self.layer = CracksGrass.corners(self, x, y)
                self.layer = CobbleCracks.corners(self, x, y)
                pass
        #print("[INFO] Corners Added")

        for y in range(len(self.map_array)):
            for x in range(len(self.map_array[0])):
                self.layer = CobbleSand.steps(self, x, y)
                self.layer = CracksGrass.steps(self, x, y)
                self.layer = CobbleCracks.steps(self, x, y)
                pass
        #print("[INFO] Steps Smoothed")
                
        return self.shrink(self.layer)

    def shrink(self, layer):
        layer_dict = self.layer.to_dict()
        layer_dict['width'], layer_dict['height'] = 256, 256

        array = np.array(layer_dict['data'])

        old_dimensions = int(math.sqrt(array.size))

        array = array.reshape(old_dimensions, old_dimensions)
        list_array = np.array(array[:-2, :-2]).flatten().tolist()

        self.map.width, self.map.height = old_dimensions-2, old_dimensions-2
        layer_dict['data'] = list_array
        self.layer = layer.from_dict(layer_dict, map)

        #print("[INFO] Map Shrunk")
        return self.layer
    
##def generate_map(output, octaves, freq):
coords = [0, 0]
output = sys.argv[1]
octaves = int(sys.argv[2])
freq = float(sys.argv[3])
x, y = int(sys.argv[4]), int(sys.argv[5])
array, layer, key_pieces, map = setup(octaves, freq, x, y)
for y in range(len(array)):
    for x in range(len(array[0])):
        if array[y][x] < 129:
            layer[x, y] = key_pieces[32] # Grass
        elif array[y][x] < 156:
            layer[x, y] = key_pieces[14] # Cracks
        elif array[y][x] < 169:
            layer[x, y] = key_pieces[5] # Cobbles
        elif array[y][x] < 190:
            layer[x, y] = key_pieces[23] # Sand
        elif array[y][x] < 500:
            layer[x, y] = key_pieces[50] # Water
            
#print("[INFO] Map Created")
Terraform(array, layer, key_pieces, map).generate()

map.layers['Ground'] = layer
map.save(str(output))

print("[INFO] Map Saved")

