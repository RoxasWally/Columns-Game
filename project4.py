"""Yousef Wally ID# 32179033
    ICS 32A
     The Fall of the World's Own Optimist (Part 1)"""
import gameboard as game


def get_input(command, board) -> None:
    """Takes an input from the user"""
    if command == 'R':
        board.rotate()
    elif command == '<':
        board.move_hor(game.LEFT)
    elif command == '>':
        board.move_hor(game.RIGHT)
    elif command[0] == 'F':
        try:
            args = command.split(' ')
            columnNumber = int(args[1])
            faller = [args[4], args[3], args[2]]
            board.spawn(columnNumber, faller)
        except ValueError:
            return


def show(board) -> None:
    """Shows the statue of the board after each move"""
    for row in range(board.rows):
        rowString = "|"
        for col in range(board.cols):
            cellValue = board.boardRows[row][col]
            cellboard = board.pieces[row][col]
            if cellboard == game.EMPTY_CELL:
                rowString += '   '
            elif cellboard == game.OCCUPIED:
                rowString += (' ' + cellValue + ' ')
            elif cellboard == game.FALLER_MOVING_CELL:
                rowString += ('[' + cellValue + ']')
            elif cellboard == game.FALLER_STOPPED_CELL:
                rowString += ('|' + cellValue + '|')
            elif cellboard == game.MATCHED_CELL:
                rowString += ('*' + cellValue + '*')
        rowString += '|'
        print(rowString)
    finalLine = ' '
    for col in range(board.cols):
        finalLine += '---'
    finalLine += ' '
    print(finalLine)

if __name__ == '__main__':
    rows = int(input())
    cols = int(input())
    board = game.Board(rows, cols)

    line = input().strip()
    if line == 'CONTENTS':
        rowList = []
        for i in range(rows):
            row = []
            line = input()
            for index in range(cols):
                row.append(line[index])
            rowList.append(row)
        board.init_board(rowList)

    while True:
        show(board)
        line = input().strip()
        if line == 'Q':
            break
        if line == '':
            if board.time():
                show(board)
                break
        else:
            get_input(line, board)