# -*- coding: utf-8 -*-

# Objekti, ki se uvozijo s from ... import *
__all__ = ['SlowMatrix', 'FastMatrix', 'CheapMatrix','FastMatrix2']

# Uvozimo naše razrede
from .slowmatrix import SlowMatrix
from .fastmatrix import FastMatrix as FastMatrix1
from .fastmatrix2 import FastMatrix2 as FastMatrix
from .cheapmatrix import CheapMatrix
