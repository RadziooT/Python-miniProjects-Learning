def print_board(board):
    n = range(len(board))
    for i in n:
        if (i % 3 == 0):
            print("- - - - - - - - - - - - - - ")
        for j in n:
            if(j == 0):
                print("| ", end="")

            print(str(board[i][j]) + " ", end="")

            if(j % 3 == 2 and j != 8):
                print(" | ", end="")
            elif(j == 8):
                print(" | ")
    print("- - - - - - - - - - - - - - ")

def find_empty(board):
    n = range(len(board))
    for i in n:
        for j in n:
            if(board[i][j] == 0):
                return (i, j) #returns row as i and column as j
    return None

def check_valid(board,number,position):
    n = range(len(board))
    #checking row
    for i in n:
            if (board[i][position[1]] == number and i != position[0]):
                return False
    # checking column
    for i in n:
            if (board[position[0]][i] == number and i != position[1]):
                return False
    #checking box
    #x and y are positions of one of the 9 boxes in sudoku
    x = position[0] // 3
    y = position[1] // 3
    for i in range(x*3,x*3+3):
        for j in range(y*3,y*3+3):
            if (board[i][j] == number and (i,j) != position):
                return False
    #returns True if all conditions are met
    return True

def solve_sudoku(board):
    position = find_empty(board)
    if (not position):
        return True
    for i in range(1,10):
        if check_valid(board,i,position):
            board[position[0]][position[1]] = i;

            if solve_sudoku(board):
                return True

            board[position[0]][position[1]] = 0;
            #backtracking element returning to last solution if the current one doesn't satisfy conditions
    return False