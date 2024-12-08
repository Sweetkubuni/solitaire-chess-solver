from collections import deque
from abc import ABC, abstractmethod
from copy import copy


# Abstract ChessPiece class
class ChessPiece(ABC):
    def __init__(self, piece_id, col, row):
        self.piece_id = piece_id
        self.col = str(col)  # Columns are letters ('a' to 'h')
        self.row = int(row)  # Rows are numbers (8 to 1)

    def __copy__(self):
        return type(self)(self.piece_id, self.col, self.row)

    @abstractmethod
    def available_movement(self, chessboard):
        """Returns a set of moves that can capture other pieces."""
        pass

    def captures(self, other_piece, chessboard):
        """Check if this piece can capture the given piece."""
        print(f'{self.piece_id} == {other_piece.piece_id}')
        if self.piece_id == other_piece.piece_id:
            return None
        return other_piece.piece_id in self.available_movement(chessboard)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.piece_id}, '{self.col}', {self.row})"


def position_to_coordinates(col, row):
    """Convert position (e.g., 'a', 8) to chessboard coordinates."""
    return ord(col) - ord('a'), 8 - row


def coordinates_to_position(coord):
    """Convert coordinates (e.g., (0, 7)) to position (e.g., 'a', 8)."""
    col = chr(coord[0] + ord('a'))
    row = 8 - coord[1]
    return col, row


# Concrete ChessPiece implementations
class Knight(ChessPiece):
    def available_movement(self, chessboard):
        # Knight moves in L-shape
        col_idx, row_idx = position_to_coordinates(self.col, self.row)
        moves = [
            (col_idx + 2, row_idx + 1), (col_idx + 2, row_idx - 1),
            (col_idx - 2, row_idx + 1), (col_idx - 2, row_idx - 1),
            (col_idx + 1, row_idx + 2), (col_idx - 1, row_idx + 2),
            (col_idx + 1, row_idx - 2), (col_idx - 1, row_idx - 2)
        ]
        valid_moves = {coordinates_to_position(move) for move in moves if 0 <= move[0] < 8 and 0 <= move[1] < 8}
        return {piece.piece_id for piece in chessboard if (piece.col, piece.row) in valid_moves}


class Rook(ChessPiece):
    def available_movement(self, chessboard):
        moves = set()
        for piece in chessboard:
            if piece.col == self.col or piece.row == self.row:
                moves.add(piece.piece_id)
        return moves


class Bishop(ChessPiece):
    def available_movement(self, chessboard):
        moves = set()
        col_idx, row_idx = position_to_coordinates(self.col, self.row)
        for piece in chessboard:
            p_col_idx, p_row_idx = position_to_coordinates(piece.col, piece.row)
            if abs(p_col_idx - col_idx) == abs(p_row_idx - row_idx):
                moves.add(piece.piece_id)
        return moves


class Queen(ChessPiece):
    def available_movement(self, chessboard):
        rook_moves = Rook(self.piece_id, self.col, self.row).available_movement(chessboard)
        bishop_moves = Bishop(self.piece_id, self.col, self.row).available_movement(chessboard)
        return rook_moves | bishop_moves

class Pawn(ChessPiece):
    def available_movement(self, chessboard):
        moves = set()
        col_idx, row_idx = position_to_coordinates(self.col, self.row)

        # Pawn's diagonal capture moves (upward direction)
        potential_moves = [
            (col_idx - 1, row_idx - 1),  # Up-left
            (col_idx + 1, row_idx - 1)  # Up-right
        ]

        valid_moves = {coordinates_to_position(move) for move in potential_moves if 0 <= move[0] < 8 and 0 <= move[1] < 8}
        return {piece.piece_id for piece in chessboard if (piece.col, piece.row) in valid_moves}

    def __repr__(self):
        return f"Pawn({self.piece_id}, '{self.col}', {self.row})"


def SearchDFS(chess_pieces, record):
    for active_piece in chess_pieces:
        results = CheckMoves(active_piece, chess_pieces, record)
        print(results)
        if len(results) == (len(chess_pieces) - 1) + len(record):
            print('all pieces except 1 captured')
            return results
    print('returning default')
    return record

# DFS for solving solitaire chess
def CheckMoves(active_chess_piece, chess_pieces, record):
    # Copy Record
    new_record = record.copy()

    #copy new set of chess pieces
    new_chess_pieces = chess_pieces.copy()

    for piece in chess_pieces:
        if active_chess_piece.captures(piece, chess_pieces):
            print(f"active_chess_piece:{active_chess_piece}")
            print(f"captured chess_piece:{piece}")
            #remove captured and moved chess pieces
            new_chess_pieces = [p for p in new_chess_pieces if p.piece_id not in [piece.piece_id, active_chess_piece.piece_id]]
            print(f'filter chess_pieces: {new_chess_pieces}')

            cpy_active_piece = copy(active_chess_piece)

            #set moved chess piece to new location
            cpy_active_piece.col, cpy_active_piece.row = piece.col, piece.row

            #add the moved chess piece back into set
            new_chess_pieces.append(cpy_active_piece)

            #add to record chess pieced moved
            new_record.append(f"{active_chess_piece} to {piece}")

            if len(new_chess_pieces) > 1:
                print(f'searching further in set {new_chess_pieces} record: {new_record}')
                return SearchDFS(new_chess_pieces, new_record)
    print(f'returning record {new_record}')
    return new_record


# Main execution
if __name__ == "__main__":
    # Initial board setup
    chess_pieces = [
        Queen(1, 'h', 2),
        Queen(2, 'e', 1),
        Queen(3, 'd', 5),
        Bishop(4,'e', 5)
    ]
    initial_stack = deque(chess_pieces)
    solution = SearchDFS(chess_pieces, [])
    print("Solution:", solution)
