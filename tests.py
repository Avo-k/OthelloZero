from game_logic import *
from search import Desdemone
import time


def test_a_game(print_board=False):
    b = Board()
    assert b.bb[0] | b.bb[1] == 103481868288, "wrong setup"

    if print_board:
        print(b)

    nb_of_piece = 4

    while not b.is_leaf:

        assert b.bb[0] & b.bb[1] == 0, "bb should be disjoint"

        b = b.make_random_move()

        if print_board:
            print(b)

        nb_of_piece += 1
        assert count_bits(b.bb[0] | b.bb[1]) == nb_of_piece, "too many pieces"

    assert b.bb[0] | b.bb[1] == UNIVERSE
