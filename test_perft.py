from game_logic import Board
from tests import test_a_game
import time


def perft(board, depth):
    if depth == 0 or board.is_leaf:
        return 1
    return sum(perft(board.make_move(move), depth - 1) for move in board.gen_moves())


def iterative_perft(max_iter=9):
    results = [1, 4, 12, 56, 244, 1396, 8200, 55092, 390216, 3005288, 24571284, 212258800, 1939886636]

    for depth, r in enumerate(results):

        if depth == max_iter:
            break

        board = Board()
        s = time.perf_counter()
        perft_count = perft(board, depth)
        print("depth     time         n/s")
        print(f"  {depth}       {time.perf_counter() - s:.3f}      {r / (time.perf_counter() - s):.2f}")
        print(f"depth {depth}: {r} - {perft_count}")
        print("-" * 30)

        assert r == perft_count, f"failed at {depth = }"


if __name__ == "__main__":
    # test_a_game()
    iterative_perft(10)
