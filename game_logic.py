import random
import time
import math
import numpy as np
import numba as nb
from numba import njit


@njit(nb.b1(nb.uint64, nb.uint8), cache=True)
def get_bit(bb, sq):
    return bb & (1 << sq)


@njit(nb.uint64(nb.uint64, nb.uint8), cache=True)
def set_bit(bb, sq):
    return bb | (1 << sq)


@njit(nb.uint64(nb.uint64, nb.uint8), cache=True)
def pop_bit(bb, sq):
    return bb & ~(1 << sq)


@njit(nb.uint8(nb.uint64), cache=True)
def count_bits(bb):
    c = 0
    while bb:
        c += 1
        bb &= bb - np.uint64(1)
    return c


@njit(nb.uint8(nb.uint64), cache=True)
def get_ls1b_index(bb):
    return count_bits((bb & -bb) - 1)


def print_bb(bb):
    """for debugging purposes"""
    print("\n")
    for rank in range(8):
        r = ""
        for file in range(8):
            sq = rank * 8 + file
            r += f" {'1' if get_bit(bb, sq) else '·'} "
        print(rank + 1, r)
    print("   A  B  C  D  E  F  G  H")

    print("Bitboard:", bb)


(
    a1, b1, c1, d1, e1, f1, g1, h1,
    a2, b2, c2, d2, e2, f2, g2, h2,
    a3, b3, c3, d3, e3, f3, g3, h3,
    a4, b4, c4, d4, e4, f4, g4, h4,
    a5, b5, c5, d5, e5, f5, g5, h5,
    a6, b6, c6, d6, e6, f6, g6, h6,
    a7, b7, c7, d7, e7, f7, g7, h7,
    a8, b8, c8, d8, e8, f8, g8, h8,
    no_sq,
) = range(65)

squares = range(64)

square_to_coordinates = (
    "a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1",
    "a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2",
    "a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3",
    "a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4",
    "a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5",
    "a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6",
    "a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7",
    "a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8",
    "-",
)
UNIVERSE = 0xffffffffffffffff
EMPTY = 0


@njit(nb.uint64(nb.uint64, nb.uint8), cache=True)
def shift(bb, direction):
    """:return: a bb with bits shifted in a given direction the non-adjacent ones erased"""
    _masks = np.array(
        (0x7F7F7F7F7F7F7F7F,  # Right
         0x007F7F7F7F7F7F7F,  # Down-right
         0xFFFFFFFFFFFFFFFF,  # Down
         0x00FEFEFEFEFEFEFE,  # Down-left
         0xFEFEFEFEFEFEFEFE,  # Left
         0xFEFEFEFEFEFEFE00,  # Up-left
         0xFFFFFFFFFFFFFFFF,  # Up
         0x7F7F7F7F7F7F7F00,  # Up-right
         ), dtype=np.uint64)
    _left_shift = (0, 0, 0, 0, 1, 9, 8, 7)
    _right_shift = (1, 9, 8, 7, 0, 0, 0, 0)

    if direction < 4:
        return (bb >> _right_shift[direction]) & _masks[direction]
    else:
        return (bb << _left_shift[direction]) & _masks[direction]


@njit(nb.uint64(nb.uint64, nb.uint64), cache=True)
def get_legal_moves(player, opp):
    """:return: a bb of legal moves for a player"""

    empty_cells = ~(player | opp)
    legal_moves = 0

    for i in range(8):
        x = shift(player, i) & opp
        x |= shift(x, i) & opp
        x |= shift(x, i) & opp
        x |= shift(x, i) & opp
        x |= shift(x, i) & opp
        x |= shift(x, i) & opp
        legal_moves |= shift(x, i) & empty_cells

    return legal_moves


@njit(nb.uint8(nb.uint64, nb.uint64), cache=True)
def get_random_move(player, opp):
    """:return: a random legal move"""

    legal_moves = get_legal_moves(player, opp)
    move_list = []

    while legal_moves:
        move = get_ls1b_index(legal_moves)
        move_list.append(move)
        legal_moves = pop_bit(legal_moves, move)

    return np.random.choice(np.array(move_list))


@njit(nb.b1(nb.uint64, nb.uint64), cache=True)
def has_legal_moves(player, opp):
    """:return: a bb of legal moves for a player"""

    empty_cells = ~(player | opp)
    legal_moves = 0

    for i in range(8):
        x = shift(player, i) & opp
        x |= shift(x, i) & opp
        x |= shift(x, i) & opp
        x |= shift(x, i) & opp
        x |= shift(x, i) & opp
        x |= shift(x, i) & opp
        legal_moves |= shift(x, i) & empty_cells
        if legal_moves:
            return True
    return False


@njit(nb.uint64[:](nb.uint64, nb.uint64, nb.uint8), cache=True)
def update_board(player, opp, move):

    # assert 0 <= move <= 63
    # assert player & opp == 0, "bb should be disjoint"
    # assert not get_bit(player | opp, move), "sq must be empty"

    move_bb = set_bit(0, move)
    player |= move_bb
    captured = 0

    for i in range(8):
        x = shift(move_bb, i) & opp
        x |= shift(x, i) & opp
        x |= shift(x, i) & opp
        x |= shift(x, i) & opp
        x |= shift(x, i) & opp
        x |= shift(x, i) & opp

        if shift(x, i) & player:
            captured |= x

    player ^= captured
    opp ^= captured

    return np.array((player, opp), np.uint64)


class Board:
    def __init__(self, bb=None, turn=0):
        if bb is None:
            bb = [0, 0]
            bb[0] = set_bit(bb[0], d5)
            bb[0] = set_bit(bb[0], e4)
            bb[1] = set_bit(bb[1], d4)
            bb[1] = set_bit(bb[1], e5)
        self.bb = bb
        self.turn = turn
        self.is_leaf = False
        self.term = None

        self.last_move = -1

    def _get_term(self):
        score = self.bb[self.turn] - 32
        return 1 if score > 0 else -1 if score < 0 else 0

    def get_score(self):
        return self.bb[self.turn] - 32

    def gen_moves(self):
        """yield legal moves"""
        moves = get_legal_moves(self.bb[self.turn], self.bb[self.turn ^ 1])
        while moves:
            move = get_ls1b_index(moves)
            yield move
            moves = pop_bit(moves, move)

    def make_move(self, move):
        """:return: a new board object with the move played"""

        new = Board(self.bb.copy(), self.turn)

        new.bb[new.turn], new.bb[new.turn ^ 1] = update_board(new.bb[new.turn], new.bb[new.turn ^ 1], move)
        new.last_move = move
        new.turn ^= 1

        if not has_legal_moves(new.bb[new.turn], new.bb[new.turn ^ 1]):
            new.turn ^= 1
            if not has_legal_moves(new.bb[new.turn], new.bb[new.turn ^ 1]):
                new.is_leaf = True
                new.term = new._get_term()
            # else:
            #     print(new.turn)
            #     print(new)
            #     assert 0

        return new

    def make_random_move(self):
        """:return: a new board object with a random move played"""
        move = get_random_move(self.bb[self.turn], self.bb[self.turn ^ 1])
        return self.make_move(move)

    def __str__(self):
        b = "\n"
        for rank in range(8):
            r = ""
            for file in range(8):
                sq = rank * 8 + file
                r += f" {'B' if get_bit(self.bb[0], sq) else 'W' if get_bit(self.bb[1], sq) else '.'} "
            b += f"{rank + 1} {r}\n"
        b += "   A  B  C  D  E  F  G  H"
        return b



# bb = [0, 0]
# bb[0] = set_bit(bb[0], d5)
# bb[0] = set_bit(bb[0], e4)
# bb[1] = set_bit(bb[1], d4)
# bb[1] = set_bit(bb[1], e5)
#
# print_bb(bb[0])
# print_bb(bb[1])
#
# print_bb(bb[0] | bb[1])

# bb = update_board(bb[0], bb[1], c4)
#
# print_bb(bb[0])
# print_bb(bb[1])
#
# print(square_to_coordinates[get_random_move(bb[1], bb[0])])

