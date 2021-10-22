def solver(sudoku, sudoku_original):

    # Input
    #sudoku = [[3,4,1,0],[0,2,0,0],[0,0,2,0],[0,1,4,3]]

    # Keeping a copy of the original
    original = [x[:] for x in sudoku]


    # Box names for box_check. Used for checking which "box" the number belongs to.
    box_name = [['a','a','b','b'],['a','a','b','b'],['c','c','d','d'],['c','c','d','d']]


    # dict for box_check
    box_dict = {'a':[],'b':[],'c':[],'d':[]}


    # fill dictionary for box_check
    for i in range(4):
        for k in range(4):
            box_dict[box_name[i][k]].append(sudoku[i][k])

    # find first cell with 0, for catching unsolvable sudokus:
    for i in range(4):
        for k in range(4):
            if sudoku[i][k] == 0:
                print("the first zero is at %i %i" % (i, k))
                row_0 = i
                col_0 = k
                break
        else:
            continue
        break


    # function for printing the sudoku
    def print_sudoku(sudoku):
        for i in range(4):
            for j in range(4):
                print(sudoku[i][j], end='')
                print('  ', end='')
            print('')


    # row check
    def check_row(row,num):
        if num in sudoku[row]:
            return 0
        else:
            return 1


    # col check
    def check_col(row, col, num):
        if row == 4:
            return 1
        elif sudoku[row][col] == num:
            return 0
        else:
            return check_col(row + 1, col, num)


    # box check
    def check_box(row, col, num):
        if num in box_dict[box_name[row][col]]:
            return 0
        else:
            return 1


    # solve function checking if conditions are met.
    def solve(row, col, num):
        if (check_col(0,col,num) == 1
            and check_row(row,num) == 1
            and check_box(row,col,num) == 1):
                return 1
        else:
            return 0

    # run solve recursively
    def solve_rec(row,col,num):
        print("entered solve rec")
        print("row: %i col: %i num: %i" % (row, col, num))
        if num > 4:
            sudoku[row][col] = 0
            return 0
        elif solve(row,col,num) == 1:
            sudoku[row][col] = num
            return 1
        else:
            return solve_rec(row,col,num+1)

    # set counters
    i = 0
    k = 0
    # set backtrack switch value
    backtrack = 0

    # row counter
    while 0 <= i < 4:
        # column counter
        while 0 <= k < 4:
            # check if number should be filled ie. is it 0 in the original
            if original[i][k] == 0:
                # check if we are backtracking, and set initial number
                if backtrack == 0:
                    num = sudoku[i][k]
                else:
                    num = sudoku[i][k] + 1
                # run number validation, go ahead if ok, or backtrack
                if solve_rec(i, k, num) == 1:
                    backtrack = 0
                    k += 1
                else:
                    # set to backtrack
                    backtrack = 1
                    # break if backtracking is called on the first cell
                    if i == row_0 and k == col_0:
                        result = [sudoku_original, 0]
                        return result
                    # decrease counter and begin backtracking
                    k -= 1
            # what to do if number if filled already
            # adding column counter increments based on backtrack
            else:
                # go ahead
                if backtrack == 0 or (i == k == 0):
                    backtrack = 0
                    k += 1
                # backtrack
                else:
                    backtrack = 1
                    k -= 1
        # adding row counter increments based on backtrack
        if backtrack == 1:
            k = 3
            i -= 1
        else:
            k = 0
            i += 1

    result = [sudoku, 1]
    return result
