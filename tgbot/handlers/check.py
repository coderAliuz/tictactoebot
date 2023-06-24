import random

# Function to check if the board is full
def is_board_full(board):
    if '-' in board:
        return False
    else:
        return True

# Function to check if a player has won
def is_winner(board, player):
    if (board[0] == player and board[1] == player and board[2] == player) or \
       (board[3] == player and board[4] == player and board[5] == player) or \
       (board[6] == player and board[7] == player and board[8] == player) or \
       (board[0] == player and board[3] == player and board[6] == player) or \
       (board[1] == player and board[4] == player and board[7] == player) or \
       (board[2] == player and board[5] == player and board[8] == player) or \
       (board[0] == player and board[4] == player and board[8] == player) or \
       (board[2] == player and board[4] == player and board[6] == player):
        return True
    else:
        return False

# Function to get the available moves
def get_available_moves(board):
    moves = []
    for i in range(len(board)):
        if board[i] == '-':
            moves.append(i)
    return moves

# Minimax algorithm
def minimax(board, depth, is_maximizing):
    if is_winner(board, 'X'):
        return -1
    elif is_winner(board, 'O'):
        return 1
    elif is_board_full(board):
        return 0

    if is_maximizing:
        best_score = -1000
        for move in get_available_moves(board):
            board[move] = 'O'
            score = minimax(board, depth+1, False)
            board[move] = '-'
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = 1000
        for move in get_available_moves(board):
            board[move] = 'X'
            score = minimax(board, depth+1, True)
            board[move] = '-'
            best_score = min(score, best_score)
        return best_score

# Function to get the best move for the AI
def get_best_move(board):
    best_move = -1
    best_score = -1000
    for move in get_available_moves(board):
        board[move] = 'O'
        score = minimax(board, 0, False)
        board[move] = '-'
        if score > best_score:
            best_score = score
            best_move = move
    return best_move

# print(get_best_move(board))
