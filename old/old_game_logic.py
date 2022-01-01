from constants import *


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


class Board:
    # right, left, down, up, down-right, up-left, down-left, up-right
    __look_around = (1, -1, 8, -8, 9, -9, 7, -7)

    def __init__(self, bb=None, turn=0):
        if bb is None:
            bb = [34628173824, 68853694464, 103481868288]
        self.bb = bb
        self.turn = turn
        self.is_leaf = False
        self.term = None

        self.last_move = -1

    @staticmethod
    def _gen_line(self, sq, direction):
        pass

    @staticmethod
    def _gen_neigh(sq, bb):
        bb &= masks_around[sq]
        while bb:
            neigh = get_ls1b_index(bb)
            yield neigh
            bb = pop_bit(bb, neigh)

    def is_legal_move(self, sq):
        """:return: True if the move is legal else None"""

        if get_bit(self.bb[2], sq): return False

        # for each opp piece neighbour
        for neigh in self._gen_neigh(sq, self.bb[self.turn ^ 1]):
            inc = neigh - sq
            while not out_of_line(inc, neigh):
                # if not piece
                if not get_bit(self.bb[2], neigh):
                    break
                # if player piece
                elif get_bit(self.bb[self.turn], neigh):
                    return True
                neigh += inc
        return False

    def _get_candidates(self):
        """:return: bitboard of pseudo legal moves"""
        candidates = 0
        bb = self.bb[self.turn ^ 1]
        while bb:
            sq = get_ls1b_index(bb)
            candidates |= masks_around[sq]
            bb = pop_bit(bb, sq)
        candidates ^= self.bb[2]
        return candidates

    def _get_random_candidates(self):
        """:return: randomized list of pseudo legal moves"""
        candidates = self._get_candidates()
        list_candidates = []
        while candidates:
            move = get_ls1b_index(candidates)
            list_candidates.append(move)
            candidates = pop_bit(candidates, move)
        random.shuffle(list_candidates)
        return list_candidates

    def gen_moves(self):
        """:yield: all legal moves"""
        candidates = self._get_candidates()
        while candidates:
            move = get_ls1b_index(candidates)
            if self.is_legal_move(move):
                yield move
            candidates = pop_bit(candidates, move)

    def _update_board(self, square):
        """play a move on the board and update bb accordingly
           calculate the next legal moves
           update leaf and term"""

        player = self.turn
        opp = player ^ 1
        self.bb[2] = set_bit(self.bb[2], square)
        self.bb[player] = set_bit(self.bb[player], square)
        flipped = 0

        for inc in self.__look_around:
            maybe_flip = 0
            sq = square + inc
            while not out_of_line(inc, sq):
                if get_bit(self.bb[opp], sq):
                    maybe_flip = set_bit(maybe_flip, sq)
                elif get_bit(self.bb[player], sq):
                    flipped |= maybe_flip
                    break
                else:
                    break
                sq += inc

        self.bb[player] ^= flipped
        self.bb[opp] ^= flipped

    def _get_term(self):
        score = self.bb[self.turn] - self.bb[self.turn ^ 1]
        return 1 if score > 0 else -1 if score < 0 else 0

    def get_score(self):
        return self.bb[self.turn] - self.bb[self.turn ^ 1]

    def make_move(self, move):
        """return a new board object with the move played"""

        new_board = Board(self.bb.copy(), self.turn)

        new_board._update_board(move)
        new_board.last_move = move
        new_board.turn ^= 1

        if next(new_board.gen_moves(), -1) == -1:
            new_board.turn ^= 1
            if next(new_board.gen_moves(), -1) == -1:
                new_board.turn ^= 1
                new_board.is_leaf = True
                new_board.term = new_board._get_term()

        return new_board

    def make_random_move(self):
        """return a new board object with a random move played"""
        for candidate in self._get_random_candidates():
            if self.is_legal_move(candidate):
                return self.make_move(candidate)

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
