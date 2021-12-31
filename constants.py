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
        bb &= bb - 1
    return c


@njit(nb.uint8(nb.uint64), cache=True)
def get_ls1b_index(bb):
    return count_bits((bb & -bb) - 1)


def print_bb(bb):
    print("\n")
    for rank in range(8):
        r = ""
        for file in range(8):
            sq = rank * 8 + file
            r += f" {'1' if get_bit(bb, sq) else '·'} "
        print(rank + 1, r)
    print("   A  B  C  D  E  F  G  H")

    print("Bitboard:", bb)


def print_board(board):
    print("\n")
    for rank in range(8):
        r = ""
        for file in range(8):
            sq = rank * 8 + file
            r += f" {'B' if get_bit(board.bb[0], sq) else 'W' if get_bit(board.bb[1], sq) else '.'} "
        print(rank + 1, r)
    print("   A  B  C  D  E  F  G  H")


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

around_sq = (1, -1, 8, -8, 9, -9, 7, -7)


def out_of_line(inc, sq):
    if not 0 <= sq <= 63:
        return True
    if abs(inc) == 8:
        return False
    if inc in (1, -7, 9):
        return not sq % 8
    if inc in (-1, 7, -9):
        return not (sq + 1) % 8
    assert 0


def _sq_around(sq):
    for inc in around_sq:
        neigh = sq + inc
        if not out_of_line(inc, neigh):
            yield neigh


def _init_mask_around():
    masks = []
    for sq in squares:
        bb = 0
        for s in _sq_around(sq):
            bb = set_bit(bb, s)
        masks.append(bb)
    return masks


masks_around = _init_mask_around()
