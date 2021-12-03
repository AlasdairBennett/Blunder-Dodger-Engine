import chess


class NegMaxx:
    # constants needed for evaluation function
    #   piece values expressed in centipawns and piece-square tables taken from Tomasz Michniewski via
    #   https://www.chessprogramming.org/Simplified_Evaluation_Function
    P = 100  # Pawn
    N = 320  # Knight TODO consider tweaking
    B = 330  # Bishop TODO consider tweaking
    R = 500  # Rook
    Q = 900  # Queen
    K = 20000  # King

    PAWN_TABLE = [0, 0, 0, 0, 0, 0, 0, 0,
                  50, 50, 50, 50, 50, 50, 50, 50,
                  10, 10, 20, 30, 30, 20, 10, 10,
                  5, 5, 10, 25, 25, 10, 5, 5,
                  0, 0, 0, 20, 20, 0, 0, 0,
                  5, -5, -10, 0, 0, -10, -5, 5,
                  5, 10, 10, -20, -20, 10, 10, 5,
                  0, 0, 0, 0, 0, 0, 0, 0]

    KNIGHT_TABLE = [-50, -40, -30, -30, -30, -30, -40, -50,
                    -40, -20, 0, 0, 0, 0, -20, -40,
                    -30, 0, 10, 15, 15, 10, 0, -30,
                    -30, 5, 15, 20, 20, 15, 5, -30,
                    -30, 0, 15, 20, 20, 15, 0, -30,
                    -30, 5, 10, 15, 15, 10, 5, -30,
                    -40, -20, 0, 5, 5, 0, -20, -40,
                    -50, -40, -30, -30, -30, -30, -40, -50]

    BISHOP_TABLE = [-20, -10, -10, -10, -10, -10, -10, -20,
                    -10, 0, 0, 0, 0, 0, 0, -10,
                    -10, 0, 5, 10, 10, 5, 0, -10,
                    -10, 5, 5, 10, 10, 5, 5, -10,
                    -10, 0, 10, 10, 10, 10, 0, -10,
                    -10, 10, 10, 10, 10, 10, 10, -10,
                    -10, 5, 0, 0, 0, 0, 5, -10,
                    -20, -10, -10, -10, -10, -10, -10, -20]

    ROOK_TABLE = [0, 0, 0, 0, 0, 0, 0, 0,
                  5, 10, 10, 10, 10, 10, 10, 5,
                  -5, 0, 0, 0, 0, 0, 0, -5,
                  -5, 0, 0, 0, 0, 0, 0, -5,
                  -5, 0, 0, 0, 0, 0, 0, -5,
                  -5, 0, 0, 0, 0, 0, 0, -5,
                  -5, 0, 0, 0, 0, 0, 0, -5,
                  0, 0, 0, 5, 5, 0, 0, 0]

    QUEEN_TABLE = [-20, -10, -10, -5, -5, -10, -10, -20,
                   -10, 0, 0, 0, 0, 0, 0, -10,
                   -10, 0, 5, 5, 5, 5, 0, -10,
                   -5, 0, 5, 5, 5, 5, 0, -5,
                   0, 0, 5, 5, 5, 5, 0, -5,
                   -10, 5, 5, 5, 5, 5, 0, -10,
                   -10, 0, 5, 0, 0, 0, 0, -10,
                   -20, -10, -10, -5, -5, -10, -10, -20]

    KING_MID_TABLE = [-30, -40, -40, -50, -50, -40, -40, -30,
                      -30, -40, -40, -50, -50, -40, -40, -30,
                      -30, -40, -40, -50, -50, -40, -40, -30,
                      -30, -40, -40, -50, -50, -40, -40, -30,
                      -20, -30, -30, -40, -40, -30, -30, -20,
                      -10, -20, -20, -20, -20, -20, -20, -10,
                      20, 20, 0, 0, 0, 0, 20, 20,
                      20, 30, 10, 0, 0, 10, 30, 20]

    KING_END_TABLE = [-50, -40, -30, -20, -20, -30, -40, -50,
                      -30, -20, -10, 0, 0, -10, -20, -30,
                      -30, -10, 20, 30, 30, 20, -10, -30,
                      -30, -10, 30, 40, 40, 30, -10, -30,
                      -30, -10, 30, 40, 40, 30, -10, -30,
                      -30, -10, 20, 30, 30, 20, -10, -30,
                      -30, -30, 0, 0, 0, 0, -30, -30,
                      -50, -30, -30, -30, -30, -30, -30, -50]

    # we create a board variable outside function scope to improve performance
    board = chess.Board()

    # TODO defines the default search depth
    DEFAULT_SEARCH_DEPTH = 4

    def __init__(self, fen):
        self.board = chess.Board(fen)

    # core evaluation method to give a score to a position
    #   takes a fen of a board position (Forsyth-Edwards Notation) and returns a score for it.
    #   Based on Simplified Evaluation Function here: https://www.chessprogramming.org/Simplified_Evaluation_Function
    #   Also borrows from https://andreasstckl.medium.com/writing-a-chess-program-in-one-day-30daff4610ec
    def evaluate(self):

        # Return the evaluation score for games which are completed
        if self.board.is_game_over():
            oc = self.board.outcome()
            if oc.winner == "white":
                if self.board.turn:
                    return float('inf')
                else:
                    return float('-inf')
            else:
                return 0

        # Find the number of each piece remaining for each player
        wp = len(self.board.pieces(chess.PAWN, chess.WHITE))
        wn = len(self.board.pieces(chess.KNIGHT, chess.WHITE))
        wb = len(self.board.pieces(chess.BISHOP, chess.WHITE))
        wr = len(self.board.pieces(chess.ROOK, chess.WHITE))
        wq = len(self.board.pieces(chess.QUEEN, chess.WHITE))

        bp = len(self.board.pieces(chess.PAWN, chess.BLACK))
        bn = len(self.board.pieces(chess.KNIGHT, chess.BLACK))
        bb = len(self.board.pieces(chess.BISHOP, chess.BLACK))
        br = len(self.board.pieces(chess.ROOK, chess.BLACK))
        bq = len(self.board.pieces(chess.QUEEN, chess.BLACK))

        score = ((self.P * (wp - bp)) +  # Material score for pawns
                 (self.N * (wn - bn)) +  # knights
                 (self.B * (wb - bb)) +  # bishops
                 (self.R * (wr - br)) +  # rooks
                 (self.Q * (wq - bq)))  # queens

        # add the piece-square table calculations to get a score for piece positions

        # pawns
        score += sum([self.PAWN_TABLE[i] for i in self.board.pieces(chess.PAWN, chess.WHITE)])
        score += sum([-self.PAWN_TABLE[chess.square_mirror(i)] for i in self.board.pieces(chess.PAWN, chess.BLACK)])

        # knights
        score += sum([self.KNIGHT_TABLE[i] for i in self.board.pieces(chess.KNIGHT, chess.WHITE)])
        score += sum([-self.KNIGHT_TABLE[chess.square_mirror(i)] for i in self.board.pieces(chess.KNIGHT, chess.BLACK)])

        # bishops
        score += sum([self.BISHOP_TABLE[i] for i in self.board.pieces(chess.BISHOP, chess.WHITE)])
        score += sum([-self.BISHOP_TABLE[chess.square_mirror(i)] for i in self.board.pieces(chess.BISHOP, chess.BLACK)])

        # rooks
        score += sum([self.ROOK_TABLE[i] for i in self.board.pieces(chess.ROOK, chess.WHITE)])
        score += sum([-self.ROOK_TABLE[chess.square_mirror(i)] for i in self.board.pieces(chess.ROOK, chess.BLACK)])

        # queens
        score += sum([self.QUEEN_TABLE[i] for i in self.board.pieces(chess.QUEEN, chess.WHITE)])
        score += sum([-self.QUEEN_TABLE[chess.square_mirror(i)] for i in self.board.pieces(chess.QUEEN, chess.BLACK)])

        # kings TODO implement end game table
        score += sum([self.KING_MID_TABLE[i] for i in self.board.pieces(chess.KING, chess.WHITE)])
        score += sum([-self.KING_MID_TABLE[chess.square_mirror(i)] for i in self.board.pieces(chess.KING, chess.BLACK)])

        # the final returned score is expressed always as a positive value relative to the color whose turn it is
        if self.board.turn:
            return score
        else:
            return -score

        # the final returned score is expressed as negative for a black advantage and positive for a white advantage
        # return score

    # quiescence is a helper which extends the negamax search, evaluating a position until it is "quiet"
    #   https://www.chessprogramming.org/Quiescence_Search
    #   TODO add delta pruning https://www.chessprogramming.org/Delta_Pruning
    def quiescence(self, alpha, beta):
        stand = self.evaluate()
        if stand >= beta:
            return beta
        if stand > alpha:
            alpha = stand

        for move in self.board.legal_moves:
            if self.board.is_capture(move):
                self.board.push(move)
                score = -self.quiescence(-beta, -alpha)
                self.board.pop()

                if score >= beta:
                    return beta
                if score > alpha:
                    alpha = score

        return alpha

    # negamax is a recursive algorithm implemented to find the best available move given a depth parameter
    #   takes a search depth, a fen representing the current game position,
    #   also uses alphabeta pruning as a part of the function to vastly increase the performance.
    def negamax(self, depth, alpha, beta):

        if depth == 0:              # base case
            return self.evaluate()
            # return self.quiescence(alpha, beta)  TODO make quiescence performant enough to use

        max_score = float('-inf')
        for move in self.board.legal_moves:
            self.board.push(move)
            score = -self.negamax(depth - 1, beta, alpha)  # recursive call
            self.board.pop()

            if score >= beta:
                return score
            if score > max_score:
                max_score = score
            if score > alpha:
                alpha = score

        return max_score

    # nega_wrapper is a wrapper function used to call the recursive function negamax
    #   it takes no parameters and returns the best move available according to the search
    def nega_wrapper(self):

        max_score = float('-inf')
        best_move = chess.Move.null()  # This value should never be returned
        alpha = float('-inf')  # minimum score for maximizing player
        beta = float('inf')  # maximum score for minimizing player
        for move in self.board.legal_moves:
            self.board.push(move)
            score = -self.negamax(self.DEFAULT_SEARCH_DEPTH, -beta, -alpha)
            self.board.pop()

            if score > max_score:
                max_score = score
                best_move = move
            if score > alpha:
                alpha = score

        return best_move
