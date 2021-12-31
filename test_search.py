from game_logic import Board
from search import Desdemone
from constants import *
import time

down_half_g = 9187201948296675328
up_half_g = 2139062143
both_half_g = 9187201950435737471


def test_1():

    b = Board()

white = 2139062143
black = 9187201948296675328

x = int(("01111111"*8), 2)

print_bb(x)
