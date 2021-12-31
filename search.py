from game_logic import Board
from constants import *


def ucb1(parent, child, temp):
    exploitation = child.score / child.visit_count * (-1 if child.board.turn else 1)
    exploration = temp * math.sqrt(math.log(parent.visit_count / child.visit_count))
    return exploitation + exploration


class Node:
    def __init__(self, board, parent):
        self.board = board
        self.parent = parent

        self.value_sum = 0
        self.visit_count = 0
        self.score = 0
        self.children = {}

        self.is_fully_expanded = False

    def expanded(self):
        return not not self.children


class Desdemone:
    def __init__(self, print_info=False):
        self.root = Node(Board(), None)
        self.print_info = print_info

    def run(self, board, time_limit=1, n_iter=10000):

        if board.last_move != self.root.board.last_move:
            if self.root.is_fully_expanded:
                self.root = self.root.children[board.last_move]
            else:
                self.root = Node(board, None)

        s = time.perf_counter()
        i = 0

        for i in range(n_iter):
            node = self.select(self.root)
            score = self.simulate(node.board)
            self.backpropagate(node, score)
            if time.perf_counter() - s > time_limit:
                break

        if self.print_info:
            print(f"{i} iter - {i/(time.perf_counter() - s):.0f} n/s")

        self.root = self.get_best_move(self.root, 0)
        self.root.parent = None

        return self.root

    def select(self, node):
        while not node.board.is_leaf:
            if node.is_fully_expanded:
                node = self.get_best_move(node, 2)
            else:
                return self.expand(node)
        return node

    @staticmethod
    def expand(node):
        move_gen = node.board.gen_moves()

        for move in move_gen:
            if move not in node.children:
                new_node = Node(node.board.make_move(move), node)
                node.children[move] = new_node
                node.is_fully_expanded = next(move_gen, -1) == -1
                return new_node

        assert 0

    @staticmethod
    def simulate(board):
        while not board.is_leaf:
            board = board.make_random_move()
        return board.term

    @staticmethod
    def backpropagate(node, score):
        while node is not None:
            node.visit_count += 1
            node.score += score
            node = node.parent

    @staticmethod
    def get_best_move(node, temp):
        best_score = float('-inf')
        best_moves = []

        for child_node in node.children.values():
            move_score = ucb1(node, child_node, temp=temp)

            if move_score > best_score:
                best_score = move_score
                best_moves = [child_node]

            elif move_score == best_score:
                best_moves.append(child_node)

        return random.choice(best_moves)
