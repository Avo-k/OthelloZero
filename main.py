from game_logic import *
from search import Desdemone
import sys
import time
from tests import test_a_game

test_a_game()

results = []

start = time.perf_counter()
i = 0
for i in range(10):
    b = Board()
    desde = Desdemone(print_info=True)
    while not b.is_leaf:
        if b.turn:
            b = b.make_random_move()
        else:
            move = desde.run(b, time_limit=.1).board.last_move
            b = b.make_move(move)
        # print(b)
    desde_score = count_bits(b.bb[0])
    print(f"{desde_score = }")
    # assert desde_score > 32
    results.append(desde_score > 32)
print("time", time.perf_counter() - start)
print(f"desde won {sum(results)} games out of {i+1}")




"""
def bitboard_to_array(bb: int) -> np.ndarray:
    s = 8 * np.arange(7, -1, -1, dtype=np.uint64)
    b = (bb >> s).astype(np.uint8)
    b = np.unpackbits(b, bitorder="little")
    return b.reshape(8, 8)
"""
