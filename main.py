import chess
import random

board = chess.Board()

PIECE_VALUES = {
    chess.PAWN: 1.0,
    chess.KNIGHT: 3.0,
    chess.BISHOP: 3.0,
    chess.ROOK: 5.0,
    chess.QUEEN: 9.0
}

PAWN_PST = [
     0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,
     5.0,  5.0,  5.0, -5.0, -5.0,  5.0,  5.0,  5.0,
     1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0,  1.0,
     0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5,
     0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0,  0.0,
     0.5, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5,  0.5,
     0.5,  1.0,  1.0, -2.0, -2.0,  1.0,  1.0,  0.5,
     0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0
]

KNIGHT_PST = [
    -0.5, -0.4, -0.3, -0.3, -0.3, -0.3, -0.4, -0.5,
    -0.4, -0.2,  0.0,  0.0,  0.0,  0.0, -0.2, -0.4,
    -0.3,  0.0,  0.2,  0.2,  0.2,  0.2,  0.0, -0.3,
    -0.3,  0.0,  0.2,  0.3,  0.3,  0.2,  0.0, -0.3,
    -0.3,  0.0,  0.2,  0.3,  0.3,  0.2,  0.0, -0.3,
    -0.3,  0.0,  0.2,  0.2,  0.2,  0.2,  0.0, -0.3,
    -0.4, -0.2,  0.0,  0.0,  0.0,  0.0, -0.2, -0.4,
    -0.5, -0.4, -0.3, -0.3, -0.3, -0.3, -0.4, -0.5,
]

BISHOP_PST = [
   -2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0,
   -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0,
   -1.0,  0.0,  0.5,  1.0,  1.0,  0.5,  0.0, -1.0,
   -1.0,  0.5,  0.5,  1.0,  1.0,  0.5,  0.5, -1.0,
   -1.0,  0.0,  1.0,  1.0,  1.0,  1.0,  0.0, -1.0,
   -1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -1.0,
   -1.0,  0.5,  0.0,  0.0,  0.0,  0.0,  0.5, -1.0,
   -2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0
]

ROOK_PST = [
     0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,
     0.5,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  0.5,
    -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5,
    -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5,
    -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5,
    -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5,
    -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5,
     0.0,  0.0,  0.0,  0.5,  0.5,  0.0,  0.0,  0.0
]

QUEEN_PST = [
   -2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0,
   -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0,
   -1.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0,
   -0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5,
    0.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5,
   -1.0,  0.5,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0,
   -1.0,  0.0,  0.5,  0.0,  0.0,  0.0,  0.0, -1.0,
   -2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0
]

"""
def move_list_generator():
    legal_moves_list = [move.uci() for move in board.legal_moves]
    #print(legal_moves_list)
    return legal_moves_list

def choose_random_move(legal_moves_list):
    random_move = random.choice(legal_moves_list)
    #print(random_move)
    return random_move

def execute_move(move_uci):
    board.push_uci(move_uci)
"""

def material_score(board):
    score = 0.0
    
    for piece_type,value in PIECE_VALUES.items():
        score += value * (len(board.pieces(piece_type, chess.WHITE)) -
        len(board.pieces(piece_type, chess.BLACK)))

    return score

def piece_square_score(board,piece_type, pst):
    score = 0.0
    
    for square in board.pieces(piece_type, chess.WHITE):
        score += pst[square]

    for square in board.pieces(piece_type, chess.BLACK):
        score -= pst[chess.square_mirror(square)]

    return score

def mobility_score(board):
    score = 0.0
    
    score += 0.05 * board.legal_moves.count()

    return score

def evaluate_board(board):
    if board.is_checkmate():
        return -9999 if board.turn else 9999
    score = 0.0
    
    # 재료 점수
    score += material_score(board)
    # 위치 점수
    score += piece_square_score(board, chess.PAWN, PAWN_PST)
    score += piece_square_score(board, chess.KNIGHT, KNIGHT_PST)
    score += piece_square_score(board, chess.BISHOP, BISHOP_PST)
    score += piece_square_score(board, chess.ROOK, ROOK_PST)
    score += piece_square_score(board, chess.QUEEN, QUEEN_PST)
    # mobility 점수
    score += mobility_score(board)


    return score

def engine_move(board):
    best_score = -float("inf")
    best_moves_list = []
    
    for move in board.legal_moves:
        
        board.push(move)
        score = evaluate_board(board)
        board.pop()

        if score > best_score:
            best_score = score
            best_moves_list = [move]

        elif score == best_score:
            best_moves_list.append(move)

    chosen_best_move =random.choice(best_moves_list)
    board.push(chosen_best_move)
    print(board)
    print(f"엔진 수 : {chosen_best_move}")
    print("-" * 20)
    if board.is_game_over():
        print(f"게임 종료: {board.result()}")
        print(f"승자: {board.outcome().winner}")

def human_move(board):
    while True:
        print(board)
        move_input = input("너의 수를 입력 (예: e2e4): ")
        try:
            move = chess.Move.from_uci(move_input)
            if move in board.legal_moves:
                board.push(move)
                break
            else:
                print("합법적인 수가 아닙니다. 다시 입력하세요.")
        except:
            print("입력 형식이 잘못되었습니다. 다시 입력하세요.")

# 메인 루프
while not board.is_game_over():
    if board.turn:  # WHITE = 사람
        human_move(board)
    else:           # BLACK = AI
        engine_move(board)

print("게임 종료")
print("결과:", board.result())
"""
while not board.is_game_over():
    legal_moves_list = move_list_generator()

    if not legal_moves_list:
        break
    
    random_move = choose_random_move(legal_moves_list)
    execute_move(random_move)

    print(board)
    print(f"Move: {random_move}")
    print("-" * 20)
"""