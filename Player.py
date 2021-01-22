import numpy as np

ROW_COUNT = 6
COLUMN_COUNT = 7

WINDOW_LENGTH = 4
EMPTY = 0 

## Approach
# https://www.youtube.com/watch?v=MMLtza3CZFM
#board = np.flip(board, 0)
def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

def is_terminal_node(board, player_num, opp_num):
    return game_completed(board, player_num) or game_completed(board, opp_num) or len(get_valid_locations(board)) == 0

### taken from Connect4.py
def game_completed( board, player_num):
        player_win_str = '{0}{0}{0}{0}'.format(player_num)
        to_str = lambda a: ''.join(a.astype(str))

        def check_horizontal(b):
            for row in b:
                if player_win_str in to_str(row):
                    return True
            return False

        def check_verticle(b):
            return check_horizontal(b.T)

        def check_diagonal(b):
            for op in [None, np.fliplr]:
                op_board = op(b) if op else b
                
                root_diag = np.diagonal(op_board, offset=0).astype(np.int)
                if player_win_str in to_str(root_diag):
                    return True

                for i in range(1, b.shape[1]-3):
                    for offset in [i, -i]:
                        diag = np.diagonal(op_board, offset=offset)
                        diag = to_str(diag.astype(np.int))
                        if player_win_str in diag:
                            return True

            return False

        return (check_horizontal(board) or
                check_verticle(board) or
                check_diagonal(board))

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)

    def get_expectimax_move(self, board):
        """
        Given the current state of the board, return the next move based on
        the alpha-beta pruning algorithm

        This will play against either itself or a human player

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """

        player_num = self.player_number

        opp_num = 1
        if player_num == 1:
            opp_num = 2
        elif player_num == 2:
            opp_num = 1

        def value(board, depth, max_player):
            valid_locations = get_valid_locations(board)
            is_terminal = is_terminal_node(board, player_num, opp_num)
            if depth == 0 or is_terminal:
                if is_terminal:
                    if game_completed(board, player_num):
                        return (None, 10000000)
                    elif game_completed(board, opp_num):
                        return (None, -10000000)
                    else:
                        return (None,0 )
                else:
                    return (None, self.evaluation_function(board))
            
            if max_player:
                return max_value(board, depth, valid_locations)
            else:
                return exp_value(board, depth, valid_locations)


        def max_value(board, depth, valid_locations):
            val = float("-inf")
            column = np.random.choice(valid_locations)
            for col in valid_locations:
                b_copy = board.copy()
                val = max(val, value(b_copy, depth - 1, False)[1])
            return column, val
    
        def exp_value(board, depth, valid_locations):
            v = 0
            column = np.random.choice(valid_locations)
            for col in valid_locations:
                p = col/len(board[0])
                b_copy = board.copy()
                v += p* value(b_copy, depth - 1, True)[1]
            return column, v

        col, score = value(board, 2, True)
        return col
       
        #raise NotImplementedError('Whoops I don\'t know what to do')
    


    def get_alpha_beta_move(self, board):
        """
        Given the current state of the board, return the next move based on
        the expectimax algorithm.

        This will play against the random player, who chooses any valid move
        with equal probability

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        player_num = self.player_number

        opp_num = 1
        if player_num == 1:
            opp_num = 2
        elif player_num == 2:
            opp_num = 1
        beta = float("inf")
        alpha = float("-inf")
        def max_value(board, alpha, beta, depth, player_num, opp_num):
            valid_locations = get_valid_locations(board)
            is_terminal = is_terminal_node(board, player_num, opp_num)
            #column = np.random.choice(valid_locations)
            if depth == 0 or is_terminal:
                if is_terminal:
                    if game_completed(board, player_num):
                        return (None, 1000)
                    elif game_completed(board, opp_num):
                        return (None, -1000)
                    else:
                        return (None,0 )
                else:
                    return (None, self.evaluation_function(board))
            v = float("-inf")
            for col in valid_locations:
                b_copy = board.copy()
                v = max(v, min_value(b_copy, alpha, beta, depth -1, player_num, opp_num)[1])
                if v >= beta:
                    column = col
                    return col, v
                alpha = max(alpha, v)
                column = col
            return column, v

        def min_value(board, alpha, beta, depth, player_num, opp_num):
            valid_locations = get_valid_locations(board)
            is_terminal = is_terminal_node(board, player_num, opp_num)
            #column = np.random.choice(valid_locations)
            if depth == 0 or is_terminal:
                if is_terminal:
                    if game_completed(board, player_num):
                        return (None, 1000)
                    elif game_completed(board, opp_num):
                        return (None, -1000)
                    else:
                        return (None,0 )
                else:
                    return (None, self.evaluation_function(board))
            v = float("inf")
            for col in valid_locations:
                b_copy = board.copy()
                v = min(v, max_value(b_copy, alpha, beta, depth -1, player_num, opp_num)[1])
                if v <= alpha:
                    column = col
                    return col, v
                beta = min(beta, v)
                column = col
            return column, v
        

        col, score = max_value(board,  alpha, beta, 3, player_num ,opp_num)
        return col

        raise NotImplementedError('Whoops I don\'t know what to do')




    def evaluation_function(self, board):
        """
        Given the current stat of the board, return the scalar value that 
        represents the evaluation function for the current player
       
        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The utility value for the current board
        """
        player_num = self.player_number
        opp_num = 1
        if player_num == 1:
            opp_num = 2
        elif player_num == 2:
            opp_num = 1

        def evaluate_window(window, player_num, opp_num):
            score = 0
            if window.count(player_num) == 4:
                score += 100
            if window.count(player_num) == 3 and window.count(0) == 1:
                score += 5 
            if window.count(player_num) == 2 and window.count(0) == 2:
                score += 2 
            if window.count(opp_num) == 3 and window.count(0) == 1:
                score -= -4 
            return score
        score = 0 

        # SCORE CENTER COLUMN
        center_array = [int(i) for i in list(board[:, len(board[0])//2])]
        center_count = center_array.count(player_num)
        score += center_count * 6 
        # HORIZONTAL
        for r in reversed(range(0, ROW_COUNT )):
            row_array = [int(i) for i in list(board[r,:])]
            for c in range(COLUMN_COUNT -3):
                window = row_array[c: c + 4]
                score += evaluate_window(window, player_num, opp_num)

        #VERTICAL
        for c in range(COLUMN_COUNT):
            column_array = [int(i) for i in list(board[:, c])]
            for r in reversed(range(0,ROW_COUNT - 3)):
                window = column_array[r: r + 4]
                score += evaluate_window(window, player_num, opp_num)
        #POSITIVE SLOPED DIAGONAL
        for r in reversed(range(0,ROW_COUNT- 3)):
            for c in range(COLUMN_COUNT - 3):
                window = [board[r + i][c  +i ] for i in range(4)]
                score += evaluate_window(window, player_num, opp_num)

        #NEGATIVE SLOPED DIAGONAL
        for r in reversed(range(0,ROW_COUNT- 3)):
            for c in range(COLUMN_COUNT - 3):
                window = [board[r + 3 - i][c + i ] for i in range(4)]
                score += evaluate_window(window, player_num, opp_num)

        return score


class RandomPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'random'
        self.player_string = 'Player {}:random'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state select a random column from the available
        valid moves.

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)

        return np.random.choice(valid_cols)


class HumanPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'human'
        self.player_string = 'Player {}:human'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state returns the human input for next move

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """

        valid_cols = []
        for i, col in enumerate(board.T):
            if 0 in col:
                valid_cols.append(i)

        move = int(input('Enter your move: '))
        #added 
        #move = self.next_move

        while move not in valid_cols:
            print('Column full, choose from:{}'.format(valid_cols))
            move = int(input('Enter your move: '))

        return move

