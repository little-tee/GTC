"""Noise functions for procedural generation of content

Contains native code implementations of Perlin improved noise (with
fBm capabilities) and Perlin simplex noise. Also contains a fast
"fake noise" implementation in GLSL for execution in shaders.

Copyright (c) 2008, Casey Duncan (casey dot duncan at gmail dot com)
"""
 
import os.path as path
from sys import path as syspath

syspath1 = path.join(path.dirname(__file__), 'lib')
syspath2 = syspath1[:-17]
syspath.append(syspath2)

__version__ = "1.2.1"

from . import _perlin, _simplex

snoise2 = _simplex.noise2
snoise3 = _simplex.noise3
snoise4 = _simplex.noise4
pnoise1 = _perlin.noise1
pnoise2 = _perlin.noise2
pnoise3 = _perlin.noise3
