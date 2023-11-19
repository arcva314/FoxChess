class Game():
    def __init__(self):
        self.board = [["bR","bN","bB","bQ","bK","bB","bN","bR"],
                      ["bp","bp","bp","bp","bp","bp","bp","bp"],
                      ["--","--","--","--","--","--","--","--"],
                      ["--","--","--","--","--","--","--","--"],
                      ["--","--","--","--","--","--","--","ff"],
                      ["--","--","--","--","--","--","--","--"],
                      ["wp","wp","wp","wp","wp","wp","wp","wp"],
                      ["wR","wN","wB","wQ","wK","wB","wN","wR"]]
        self.whiteToMove = True
        self.white_king_location = (7,4)
        self.black_king_location = (0,4)
        self.inCheck = False
        self.pins = []
        self.checks = []
        self.checkmate = False
        self.stalemate = False
    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece
        self.whiteToMove = not self.whiteToMove
        if move.piece == "wK":
            self.white_king_location = (move.end_row, move.end_col)
        elif move.piece == 'bK':
            self.black_king_location = (move.end_row, move.end_col)
        if move.is_pawn_promotion:
            self.board[move.end_row][move.end_col] = move.piece[0] + 'Q'
    def get_valid_moves(self):
        moves = []
        self.inCheck, self.pins, self.checks = self.find_pins_and_checks()
        if self.whiteToMove:
            king_row = self.white_king_location[0]
            king_col = self.white_king_location[1]
        else:
            king_row = self.black_king_location[0]
            king_col = self.black_king_location[1]
        if self.inCheck:
            if len(self.checks) == 1:
                moves = self.get_all_moves()
                check = self.checks[0]
                check_row = check[0]
                check_col = check[1]
                piece_giving_check = self.board[check_row][check_col]
                valid_squares = []
                if piece_giving_check[1] == 'N':
                    valid_squares = [(check_row, check_col)]
                else:
                    for i in range(1,8):
                        valid_square = (king_row + check[2] * i, king_col + check[3] * 1)
                        valid_squares.append(valid_square)
                        if valid_square[0] == check_row and valid_square[1] == check_col:
                            break
                print(valid_squares)
                for i in range(len(moves) - 1, -1, -1):
                    if moves[i].piece != 'K':
                        if not (moves[i].end_row, moves[i].end_col) in valid_squares:
                            moves.remove(moves[i])
            else:
                self.get_King_Moves(king_row, king_col, moves)
        else:
            moves = self.get_all_moves()
        #print(moves[0].start_row, moves[0].start_col, moves[0].end_row, moves[0].end_col, moves[0].piece)
        if len(moves) == 0:
            if self.inCheck == True:
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            for i in range(len(moves)):
                print(moves[i].start_row, moves[i].start_col, moves[i].end_row, moves[i].end_col, moves[i].piece)
                print(self.inCheck)
            self.checkmate = False
            self.stalemate = False
        return moves
    def find_pins_and_checks(self):
        pins = []
        checks = []
        inCheck = False
        if self.whiteToMove:
            enemy_color = 'b'
            ally_color = 'w'
            start_row = self.white_king_location[0]
            start_col = self.white_king_location[1]
        else:
            enemy_color = 'w'
            ally_color = 'b'
            start_row = self.black_king_location[0]
            start_col = self.black_king_location[1]
        directions = ((-1,0), (0,-1), (1,0), (0,1), (-1,-1),(-1,1),(1,-1), (1,1))
        for j in range(len(directions)):
            d = directions[j]
            possible_pin = ()
            for i in range(1,8):
                end_row = start_row + d[0] * i
                end_col = start_col + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] == ally_color and end_piece[1] != 'K':
                        if possible_pin == ():
                            possible_pin = (end_row, end_col, d[0], d[1])
                        else:
                            break
                    elif end_piece[0] == enemy_color:
                        piece_type = end_piece[1]
                        if (0 <= j <= 3 and piece_type == 'R') or \
                                (4 <= j <= 7 and piece_type == 'B') or \
                                (i == 1 and piece_type == 'p' and ((enemy_color == 'w' and 6 <= j <= 7) or (enemy_color == 'b' and 4 <= j <= 5))) or \
                                (piece_type == 'Q') or (i == 1 and piece_type == 'K'):
                            if possible_pin == ():
                                inCheck = True
                                checks.append((end_row, end_col, d[0], d[1]))
                                break
                            else:
                                pins.append(possible_pin)
                                break
                        else:
                            break
        knight_moves = ((-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1))
        for move in knight_moves:
            end_row = start_row + move[0]
            end_col = start_col + move[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] == enemy_color and end_piece[1] == 'N':
                    inCheck = True
                    checks.append((end_row, end_col, move[0], move[1]))
        return inCheck, pins, checks

    def get_all_moves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if ((turn == 'w' or turn == 'f') and self.whiteToMove) or ((turn == 'b' or turn == 'f') and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    if piece == 'p':
                        self.get_pawn_moves(r, c, moves)
                    elif piece == 'R':
                        self.get_Rook_Moves(r, c, moves)
                    elif piece == 'N':
                        self.get_Knight_Moves(r, c, moves)
                    elif piece == 'B':
                        self.get_Bishop_Moves(r, c, moves)
                    elif piece == 'Q':
                        self.get_Queen_Moves(r, c, moves)
                    elif piece == 'K':
                        self.get_King_Moves(r, c, moves)
                    elif piece == 'f':
                        self.get_fox_moves(r, c, moves)

        return moves


    def get_pawn_moves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.whiteToMove:
            if self.board[r - 1][c] == "--":
                if not piecePinned or pinDirection == (-1, 0):
                    moves.append(Move((r, c), (r - 1, c), self.board))
                    if r == 6 and self.board[r - 2][c] == "--":
                        moves.append(Move((r, c), (r - 2, c), self.board))
            if c - 1 >= 0:
                if self.board[r - 1][c - 1][0] == "b":
                    if not piecePinned or pinDirection == (-1, -1):
                        moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if c + 1 <= 7:
                if self.board[r - 1][c + 1][0] == "b":
                    if not piecePinned or pinDirection == (-1, 1):
                        moves.append(Move((r, c), (r - 1, c + 1), self.board))
        else:
            if self.board[r + 1][c] == "--":
                if not piecePinned or pinDirection == (-1, 0):
                    moves.append(Move((r, c), (r + 1, c), self.board))
                    if r == 1 and self.board[r + 2][c] == "--":
                        moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0:
                if self.board[r + 1][c - 1][0] == "w":
                    if not piecePinned or pinDirection == (1, -1):
                        moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c + 1 <= 7:
                if self.board[r + 1][c + 1][0] == "w":
                    if not piecePinned or pinDirection == (1, 1):
                        moves.append(Move((r, c), (r + 1, c + 1), self.board))

    def get_Rook_Moves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != "Q":
                    self.pins.remove(self.pins[i])
                break
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else:
                            break
                else:
                    break

    def get_Bishop_Moves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else:
                            break
                else:
                    break

    def get_Knight_Moves(self, r, c, moves):
        piecePinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break
        knight_Moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        ally_Color = "w" if self.whiteToMove else "b"
        for i in knight_Moves:
            endRow = r + i[0]
            endCol = c + i[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != ally_Color and endPiece != 'ff':
                        moves.append(Move((r, c), (endRow, endCol), self.board))

    def get_Queen_Moves(self, r, c, moves):
        self.get_Rook_Moves(r, c, moves)
        self.get_Bishop_Moves(r, c, moves)

    def get_King_Moves(self, r, c, moves):
        rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colMoves = (-1, 0, 1, -1, 1, -1, 0, 1)
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + rowMoves[i]
            endCol = c + colMoves[i]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece != 'ff':
                    if endPiece[0] != allyColor:
                        if allyColor == "w":
                            self.white_king_location = (endRow, endCol)
                        else:
                            self.black_king_location = (endRow, endCol)
                        inCheck, pins, checks = self.find_pins_and_checks()
                        if not inCheck:
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        if allyColor == "w":
                            self.white_king_location = (r, c)
                        else:
                            self.black_king_location = (r, c)
    def get_fox_moves(self, r, c, moves):
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == '--':
                    moves.append(Move((r,c), (i,j), self.board))
        #print("hello")

class Move:
    def __init__(self, start_square, end_square, board):
        self.start_row = start_square[0]
        self.start_col = start_square[1]
        self.end_row = end_square[0]
        self.end_col = end_square[1]
        self.piece = board[self.start_row][self.start_col]
        self.is_pawn_promotion = (self.piece == 'wp' and self.end_row == 0) or (
        self.piece == 'bp' and self.end_row == 7)
        self.moveID = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False