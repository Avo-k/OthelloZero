from game import Board
from search import Desdemone
from constants import *
import time


def test_1():

    b = Board()

white = 2139062143
black = 9187201948296675328

x = int(("01111111"*4)+("0"*32), 2)

print_bb(x)
