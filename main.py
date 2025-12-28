import chess
import random

board = chess.Board()

# 기물 가치 설정
PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 280,
    chess.ROOK: 479,
    chess.QUEEN: 929,
    chess.KING: 60000
}

# --- Piece Square Tables (PST) ---
PAWN_PST = [
    0,   0,   0,   0,   0,   0,   0,   0,
    78,  83,  86,  73, 102,  82,  85,  90,
    7,  29,  21,  44,  40,  31,  44,   7,
    -17,  16,  -2,  15,  14,   0,  15, -13,
    -26,   3,  10,   9,   6,   1,   0, -23,
    -22,   9,   5, -11, -10,  -2,   3, -19,
    -31,   8,  -7, -37, -36, -14,   3, -31,
    0,   0,   0,   0,   0,   0,   0,   0
]

KNIGHT_PST = [
    -66, -53, -75, -75, -10, -55, -58, -70,
    -3,  -6, 100, -36,   4,  62,  -4, -14,
    -10,  67,   1,  74,  73,  27,  62,  -2,
    -24,  24,  45,  37,  33,  41,  25,  -17,
    -1,   5,  31,  21,  22,  35,   2,   0,
    -18,  10,  13,  22,  18,  15,  11, -14,
    -23, -15,   2,   0,   2,   0, -23, -20,
    -74, -23, -26, -24, -19, -35, -22, -69
]

BISHOP_PST = [
    -59, -78, -82, -76, -23,-107, -37, -50,
    -11,  20,  35, -42, -39,  31,   2, -22,
    -9,  39, -32,  41,  52, -10,  28, -14,
    25,  17,  20,  34,  26,  25,  15,  10,
    13,  10,  17,  23,  17,  16,   0,   7,
    14,  25,  24,  15,   8,  25,  20,  15,
    19,  20,  11,   6,   7,   6,  20,  16,
    -7,   2, -15, -12, -14, -15, -10, -10
]

ROOK_PST = [
    35,  29,  33,   4,  37,  33,  56,  50,
    55,  29,  56,  67,  55,  62,  34,  60,
    19,  35,  28,  33,  45,  27,  25,  15,
    0,   5,  16,  13,  18,  -4,  -9,  -6,
    -28, -35, -16, -21, -13, -29, -46, -30,
    -42, -28, -42, -25, -25, -35, -26, -46,
    -53, -38, -31, -26, -29, -43, -44, -53,
    -30, -24, -18,   5,  -2, -18, -31, -32
]

QUEEN_PST = [
    6,   1,  -8,-104,  69,  24,  88,  26,
    14,  32,  60, -10,  20,  76,  57,  24,
    -2,  43,  32,  60,  72,  63,  43,   2,
    1, -16,  22,  17,  25,  20, -13,  -6,
    -14, -15,  -2,  -5,  -1, -10, -20, -22,
    -30,  -6, -13, -11, -16, -11, -16, -27,
    -36, -18,   0, -19, -15, -15, -21, -38,
    -39, -30, -31, -13, -31, -36, -34, -42
]

# --- Evaluation Functions ---

def evaluate_board(board):
    if board.is_checkmate():
        # 현재 턴인 사람이 체크메이트 상태라면 최악의 점수 반환
        return -9999
    
    if board.is_stalemate() or board.can_claim_threefold_repetition() or board.is_insufficient_material() or board.can_claim_draw or board.can_claim_fifty_moves or board.is_seventyfive_moves:
        return 0

    score = 0.0
    
    # 기물 점수 계산
    for piece_type, value in PIECE_VALUES.items():
        score += value * (len(board.pieces(piece_type, chess.WHITE)) -
                          len(board.pieces(piece_type, chess.BLACK)))

    # 위치 점수 계산 (가중치 0.5 적용)
    score += piece_square_score(board, chess.PAWN, PAWN_PST)
    score += piece_square_score(board, chess.KNIGHT, KNIGHT_PST)
    score += piece_square_score(board, chess.BISHOP, BISHOP_PST)
    score += piece_square_score(board, chess.ROOK, ROOK_PST)
    score += piece_square_score(board, chess.QUEEN, QUEEN_PST)
    
    # 기동성 점수
    score += 0.05 * board.legal_moves.count()

    # Negamax: 현재 턴인 플레이어 관점으로 부호 반전
    return score if board.turn == chess.WHITE else -score

def piece_square_score(board, piece_type, pst):
    score = 0.0
    for square in board.pieces(piece_type, chess.WHITE):
        score += pst[square] * 0.4
    for square in board.pieces(piece_type, chess.BLACK):
        score -= pst[chess.square_mirror(square)] * 0.4
    return score

# --- Search Algorithms ---

def quiescence_search(board, alpha, beta):
    """안정적인 상태가 될 때까지 잡는 수만 탐색 (지평선 효과 방지)"""
    stand_pat = evaluate_board(board)
    
    if stand_pat >= beta:
        return beta
    if alpha < stand_pat:
        alpha = stand_pat

    for move in board.legal_moves:
        if board.is_capture(move):
            board.push(move)
            score = -quiescence_search(board, -beta, -alpha)
            board.pop()

            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
    return alpha

def score_move(board, move):
    """가지치기 효율을 높이기 위한 수 정렬용 점수 계산"""
    score = 0
    from_sq = move.from_square
    to_sq = move.to_square
    piece = board.piece_at(from_sq)
    if not piece: return 0
    piece_type = piece.piece_type

    # 1. MVV-LVA (가치 높은 기물을 낮은 기물로 잡기)
    if board.is_capture(move):
        captured_piece = board.piece_at(to_sq)
        if captured_piece:
            score += 10 * PIECE_VALUES[captured_piece.piece_type] - PIECE_VALUES[piece_type]
            score += 10000 
    
    # 2. 체크 가산점 (과도하지 않게 설정)
    if board.gives_check(move):
        score += 100 

    # 3. 위험 지역 이동 감점 (Hanging Piece 방지)
    if board.is_attacked_by(not board.turn, to_sq):
        if not board.is_attacked_by(board.turn, to_sq):
            score -= PIECE_VALUES[piece_type] * 2
        else:
            score -= 10

    return score

def negamax(board, depth, alpha, beta):
    if board.is_game_over():
        return evaluate_board(board)

    if depth == 0:
        return quiescence_search(board, alpha, beta)

    best_score = -float("inf")
    
    # 수 정렬
    moves = list(board.legal_moves)
    moves.sort(key=lambda m: score_move(board, m), reverse=True)

    for move in moves:
        board.push(move)
        score = -negamax(board, depth - 1, -beta, -alpha)
        board.pop()

        if score > best_score:
            best_score = score
        
        alpha = max(alpha, score)
        if alpha >= beta:
            break
            
    return best_score

# --- Main Game Loop Functions ---

def engine_move(board):
    best_move = None
    best_score = -float("inf")
    depth = 4 

    # 최상위 노드에서도 수 정렬 적용 (가지치기 극대화)
    moves = list(board.legal_moves)
    moves.sort(key=lambda m: score_move(board, m), reverse=True)
    
    for move in moves:
        board.push(move)
        score = -negamax(board, depth - 1, -float("inf"), float("inf"))
        board.pop()

        if score > best_score:
            best_score = score
            best_move = move

    if best_move:
        board.push(best_move)
        print("\n" + "="*20)
        print(board)
        print(f"엔진의 수: {best_move} (점수: {best_score})")
        print("="*20 + "\n")
    else:
        print("엔진이 더 이상 둘 수 있는 수가 없습니다.")

def human_move(board):
    while True:
        print("\n" + str(board))
        move_input = input("\n당신의 수를 입력하세요 (예: e2e4): ")
        try:
            move = chess.Move.from_uci(move_input)
            if move in board.legal_moves:
                board.push(move)
                break
            else:
                print("⚠️  합법적인 수가 아닙니다. 다시 입력하세요.")
        except:
            print("⚠️  입력 형식이 잘못되었습니다 (UCI 방식: e2e4).")

# 메인 실행부
if __name__ == "__main__":
    print("체스 엔진을 시작합니다. 당신은 백(WHITE)입니다.")
    while not board.is_game_over():
        if board.turn:  # WHITE
            human_move(board)
        else:           # BLACK (AI)
            print("엔진이 수 계산 중...")
            engine_move(board)

    print("\n게임 종료")
    print("결과:", board.result())
    outcome = board.outcome()
    if outcome and outcome.winner is not None:
        winner = "백" if outcome.winner == chess.WHITE else "흑"
        print(f"승자: {winner}")
    else:
        print("무승부입니다.")