# -*- coding: utf-8 -*-

# Objekti, ki se uvozijo s from ... import *
__all__ = ['SlowMatrix', 'FastMatrix', 'CheapMatrix']

# Uvozimo naše razrede
from .slowmatrix import SlowMatrix
from .fastmatrix import FastMatrix
from .cheapmatrix import CheapMatrix
