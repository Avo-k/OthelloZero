from game import *
from search import Desdemone
import sys


for i in range(10):

    b = Board()
    desde = Desdemone(print_info=False)
    # print_board(b)
    x = 4

    while not b.is_leaf:
        # print(f"{'White' if b.turn else 'Black'} to play")
        # print("moves dispo:", [square_to_coordinates[m] for m in b.next_move_stack], sep="\n")

        if b.turn:
            # b = b.make_move(eval(input("ur move: ")))
            b = b.make_random_move()

        else:
            b = desde.run(b, .14).board

        # print_board(b)
        # print(f"{'Randy' if b.turn else 'Desdemone'} played {square_to_coordinates[b.last_move]}")
        x += 1

        assert count_bits(b.bb[2]) == x, "there is an error somewhere"

    print_board(b)
    Desdemone_score = count_bits(b.bb[1])
    Randy_score = count_bits(b.bb[0])

    assert Desdemone_score + Randy_score == 64

    print(f"Desdemone wins with {Desdemone_score}")
    assert Desdemone_score > 32
