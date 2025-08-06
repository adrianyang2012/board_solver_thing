pieces= [[2,4],[3,4],[2,2],[1,4],[2,5],[3,3],[2,3],[1,5]]
board = [[0 for x in range(8)] for y in range(8)]
board[1][0] = 1
board[1][1] = 1
board[1][2] = 1
board[1][3] = 1
board[1][4] = 1
board[4][4] = 1

def floodfill(board,piece):
    global pieces
    if piece==8:
        return board
        #print(board)
    for i in range(len(board)):
        for j in range(len(board[0])):
            stop = 0
            new_board = [x[:] for x in board]
            for x in range(i,i+pieces[piece][0]):
                for y in range(j,j+pieces[piece][1]):
                    if x>=len(board) or y>=len(board[0]):
                        stop = 1
                        break
                    elif board[x][y]:
                        stop = 1
                        break
                    else:
                        new_board[x][y] = piece+2

                if stop:
                    break
            if not stop:

                a = floodfill(new_board,piece+1)
                if a:
                    return a
    for i in range(len(board)):
        for j in range(len(board[0])):
            stop = 0
            new_board = [x[:] for x in board]
            for x in range(i,i+pieces[piece][1]):
                for y in range(j,j+pieces[piece][0]):
                    if x>=len(board) or y>=len(board[0]):
                        stop = 1
                        break
                    elif board[x][y]:
                        stop = 1
                        break
                    else:
                        new_board[x][y] = piece+2

                if stop:
                    break
            if not stop:

                a = floodfill(new_board,piece+1)
                if a:
                    return a
    return False
floodfill(board,0)
