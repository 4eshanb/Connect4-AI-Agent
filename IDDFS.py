import numpy as np

def IDDFS(board, depth, player_num):
    for i in range(depth):
        for j in board[i]:
            found = DLS(board,j, i)
            if found != None:
                print(found)
                return found

                
def DLS( board, node, depth, ):
    if depth == 0:
        if node == max(board[depth]):
            return node
    elif depth > 0:
        if node == max(board[depth]):
            return node


if __name__=='__main__':
    board = np.zeros([6,7])
    for i in range(len(board)):
        for j in range(len(board[i])):
            board[i][j] = i + j
    print(board)
    player_num = 1
    IDDFS(board, 5, player_num)
