def done_or_not(board):  # board[i][j]
    done = True
    allowed = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for i in range(9):
        numbersused = []
        for j in range(9):
            if board[i][j] in numbersused or board[i][j] not in allowed:
                done = False
            else:
                numbersused.append(board[i][j])

    for j in range(9):
        numbersused = []
        for i in range(9):
            if board[i][j] in numbersused or board[i][j] not in allowed:
                done = False
            else:
                numbersused.append(board[i][j])
    if done:
        return 'Finished!'
    else:
        return 'Try again!'

    for bigi in range(3):
        for bigj in range(3):
            numbersused = []
            for reli in range(3):
                for relj in range(3):
                    i = bigi * 3 + reli
                    j = bigj * 3 + relj
                    print(i, j)
                    if board[i][j] in numbersused or board[i][j] not in allowed:
                        done = False
                    else:
                        numbersused.append(board[i][j])

                        # your solution here
                        # ..
                        # return 'Finished!'
                        # ..
                        # or return 'Try again!'


