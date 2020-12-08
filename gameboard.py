EMPTY_CELL = 'EMPTY'
FALLER_MOVING_CELL = 'FALLER_MOVING'
FALLER_STOPPED_CELL = 'FALLER_STOPPED STATE'
OCCUPIED = 'OCCUPIED STATE'
MATCHED_CELL = 'MATCHED STATE'

LEFT = -1
RIGHT = 1
DOWN = 0
DOWN_LEFT = 2

NONE = 'NONE'
EMPTY = ' '
S = 'S'
T = 'T'
V = 'V'
W = 'W'
X = 'X'
Y = 'Y'
Z = 'Z'


class Board:
    def __init__(self, r, c):
        """
        Standard constructor for a GameBoard that initializes all the variables
        :param r:  the number of rows
        :param c:  the number of cols
        """
        self.lastfallerposition = None
        self.rows = r
        self.cols = c
        self.boardRows = []
        self.pieces = []
        self.faller = Faller()
        for i in range(r):
            row = []
            row_pieces = []
            for j in range(c):
                row.append(EMPTY)
                row_pieces.append(EMPTY_CELL)
            self.boardRows.append(row)
            self.pieces.append(row_pieces)

    def init_board(self, contents) -> None:
        """Initiates the board by taking the user's input"""
        for row in range(self.rows):
            for col in range(self.cols):
                value = contents[row][col]
                if value is EMPTY:
                    self.set_cell(row, col, EMPTY, EMPTY_CELL)
                else:
                    self.set_cell(row, col, value, OCCUPIED)

        self.time_grav()
        self.matching()

    def time(self) -> bool:
        """Ticks one time unit on the game."""
        if self.faller.active:
            if self.faller.is_moving:
                self.check_faller()
            if not self.faller.is_moving:
                value = False
                if self.faller.row - 2 < 0:
                    value = True
                for i in range(3):
                    self.set_cell(self.faller.row - i, self.faller.col, self.faller.contents[i], OCCUPIED)
                self.faller.active = False
                self.matching()
                return value

            self.fall_down()
            self.check_faller()
        self.matching()
        return False

    def spawn(self, column, faller) -> None:
        """Spawns a faller in the given column"""
        if self.faller.active:
            return

        self.faller.active = True
        self.faller.contents = faller
        self.faller.row = 0
        self.faller.col = (column - 1)
        self.set_cell(0, self.faller.col, self.faller.contents[0], FALLER_MOVING_CELL)
        self.lastfallerposition = (self.faller.row, self.faller.col)
        self.check_faller()

    def rotate(self) -> None:
        """Rotates the faller"""
        if not self.faller.active:
            return

        one = self.faller.contents[0]
        two = self.faller.contents[1]
        three = self.faller.contents[2]

        self.faller.contents = [two, three, one]
        for i in range(3):
            self.set_cell_contents(self.faller.row - i, self.faller.col, self.faller.contents[i])
        self.check_faller()

    def move_hor(self, direction) -> None:
        """Moves the faller horizontally, if > to the right, if < to the left"""
        if not self.faller.active:
            return

        if not direction == RIGHT and not direction == LEFT:
            return

        if (direction == LEFT and self.faller.col == 0) or (
                direction == RIGHT and self.faller.col == self.cols - 1):
            return

        targetColumn = self.faller.col + direction
        for i in range(3):
            if self.faller.row - i < 0:
                break

            if self.pieces[self.faller.row - i][targetColumn] == OCCUPIED:
                return

        for i in range(3):
            if self.faller.row - i < 0:
                break
            self.move(self.faller.row - i, self.faller.col, direction)

        self.faller.col = targetColumn
        self.check_faller()
        self.removelastfaller()
        self.lastfallerposition = (self.faller.row, self.faller.col)

    def set_cell(self, row, col, contents, state) -> None:
        """Sets the content and state of the cell identified by the given row and column"""
        if row < 0:
            return
        self.set_cell_contents(row, col, contents)
        self.set_cell_state(row, col, state)

    def set_cell_contents(self, row, col, contents) -> None:
        """Sets the content of the cell identified by the given row and column"""
        if row < 0:
            return
        self.boardRows[row][col] = contents
    def set_cell_state(self, row, col, state) -> None:
        """Sets the state of the cell identified by the given row and column"""
        if row < 0:
            return
        self.pieces[row][col] = state

    def time_grav(self):
        """Applies gem gravity to all frozen cells, and moves them until the the cell below them is solid"""
        for col in range(self.cols):
            for row in range(self.rows - 1, -1, -1):
                state = self.pieces[row][col]
                # Ignore the crawler when propagating gravity
                if state == FALLER_MOVING_CELL or state == FALLER_STOPPED_CELL:
                    continue
                if state == OCCUPIED:
                    i = 1
                    while not ((row + i) >= self.rows or self.pieces[row + i][col] == OCCUPIED):
                        self.move(row + i - 1, col, DOWN)
                        i += 1

    def matching(self):
        """Ticks the matching state on all cell."""

        for row in range(self.rows):
            for col in range(self.cols):
                if self.pieces[row][col] == MATCHED_CELL:
                    self.set_cell(row, col, EMPTY, EMPTY_CELL)
        self.time_grav()
        self.check_ver_ax()
        self.check_hor_ax()
        self.check_diag()

    def check_ver_ax(self) -> None:
        """ Attempts matching for all cells on the vertical axis"""
        for currentRow in range(self.rows - 1, -1, -1):
            matches = 0
            gem = NONE
            for col in range(0, self.cols):
                contents = self.boardRows[currentRow][col]
                state = self.pieces[currentRow][col]
                cellMatches = (contents == gem and (state == OCCUPIED or state == MATCHED_CELL))
                if cellMatches:
                    matches += 1
                if col == self.cols - 1:
                    if matches >= 3:
                        if cellMatches:
                            self.match_pieces(currentRow, col, LEFT, matches)
                        else:
                            self.match_pieces(currentRow, col - 1, LEFT, matches)
                elif not cellMatches:
                    if matches >= 3:
                        self.match_pieces(currentRow, col - 1, LEFT, matches)

                    if state == OCCUPIED or state == MATCHED_CELL:
                        gem = contents
                        matches = 1
                    else:
                        gem = NONE
                        matches = 1

    def check_hor_ax(self) -> None:
        """ Attempts matching for all cells on the horizontal axis"""
        for currentCol in range(0, self.cols):
            matches = 0
            gem = NONE
            for row in range(self.rows - 1, -1, -1):
                contents = self.boardRows[row][currentCol]
                state = self.pieces[row][currentCol]
                cellMatches = (contents == gem and (state == OCCUPIED or state == MATCHED_CELL))
                if cellMatches:
                    matches += 1

                if row == 0:
                    if matches >= 3:
                        if cellMatches:
                            self.match_pieces(row, currentCol, DOWN, matches)
                        else:
                            self.match_pieces(row + 1, currentCol, DOWN, matches)
                elif not cellMatches:
                    if matches >= 3:
                        self.match_pieces(row + 1, currentCol, DOWN, matches)

                    if state == OCCUPIED or state == MATCHED_CELL:
                        gem = contents
                        matches = 1
                    else:
                        gem = NONE
                        matches = 1

    def check_diag(self) -> None:
        """ Attempts matching for all cells on the diagonal axis"""
        for currentRow in range(self.rows - 1, -1, -1):
            for currentCol in range(0, self.cols):
                matches = 0
                gem = NONE
                rowCounter = 0
                colCounter = 0
                while True:
                    row = currentRow - rowCounter
                    col = currentCol + colCounter

                    contents = self.boardRows[row][col]
                    state = self.pieces[row][col]
                    cellMatches = (contents == gem and (state == OCCUPIED or state == MATCHED_CELL))
                    # This cell matches our current sequence
                    if cellMatches:
                        matches += 1

                    if col == self.cols - 1 or row == 0:
                        if matches >= 3:
                            if cellMatches:
                                self.match_pieces(row, col, DOWN_LEFT, matches)
                            else:
                                self.match_pieces(row + 1, col - 1, DOWN_LEFT, matches)
                    elif not cellMatches:
                        if matches >= 3:
                            self.match_pieces(row + 1, col - 1, DOWN_LEFT, matches)

                        if state == OCCUPIED or state == MATCHED_CELL:
                            gem = contents
                            matches = 1
                        else:
                            gem = NONE
                            matches = 1

                    rowCounter += 1
                    colCounter += 1

                    if currentRow - rowCounter < 0 or currentCol + colCounter >= self.cols:
                        break

    def match_pieces(self, row, col, direction, amount) -> None:
        """Matches the given number of cells in the given direction as matching cells"""
        if direction == LEFT:
            for targetCol in range(col, col - amount, -1):
                self.set_cell_state(row, targetCol, MATCHED_CELL)
        elif direction == DOWN:
            for targetRow in range(row, row + amount):
                self.set_cell_state(targetRow, col, MATCHED_CELL)
        elif direction == DOWN_LEFT:
            for i in range(amount):
                self.set_cell_state(row + i, col - i, MATCHED_CELL)

    def check_faller(self) -> None:
        """Checks for the faller"""
        targetRow = self.faller.row + 1
        if targetRow >= self.rows or self.pieces[targetRow][self.faller.col] == OCCUPIED:
            state = FALLER_STOPPED_CELL
            self.faller.is_moving = False
        else:
            state = FALLER_MOVING_CELL
            self.faller.is_moving = True

        for i in range(3):
            row = self.faller.row - i
            if row < 0:
                return
            self.set_cell(row, self.faller.col, self.faller.contents[i], state)

    def fall_down(self) -> None:
        """Moves the faller down"""
        if self.faller.row + 1 >= self.rows or self.pieces[self.faller.row + 1][self.faller.col] == OCCUPIED:
            return

        self.move(self.faller.row, self.faller.col, DOWN)
        if self.faller.row - 1 >= 0:
            self.move(self.faller.row - 1, self.faller.col, DOWN)
            if self.faller.row - 2 >= 0:
                self.move(self.faller.row - 2, self.faller.col, DOWN)
            else:
                self.set_cell(self.faller.row - 1, self.faller.col, self.faller.contents[2],
                              FALLER_MOVING_CELL)
        else:
            self.set_cell(self.faller.row, self.faller.col, self.faller.contents[1], FALLER_MOVING_CELL)
        self.faller.row = self.faller.row + 1
        self.removelastfaller()
        self.lastfallerposition = (self.faller.row, self.faller.col)

    def move(self, row, col, direction) -> None:
        """Moves the given cell in the given direction"""
        old_val = self.boardRows[row][col]
        old_status = self.pieces[row][col]

        self.boardRows[row][col] = EMPTY
        self.pieces[row][col] = EMPTY_CELL

        if direction == DOWN:
            targetRow = row + 1
            self.boardRows[targetRow][col] = old_val
            self.pieces[targetRow][col] = old_status
        else:
            targetCol = col + direction
            self.boardRows[row][targetCol] = old_val
            self.pieces[row][targetCol] = old_status

    def removelastfaller(self) -> None:
        row, col = self.lastfallerposition
        self.resetcell(row,col)
        if row > 0:
            self.resetcell(row-1, col)
        if row > 1:
            self.resetcell(row-2,col)


    def resetcell(self,row,col) -> None:
        self.set_cell(row, col, ' ', EMPTY_CELL)

class Faller:
    def __init__(self):
        """
        Creates a Faller Object
        """
        self.active = False
        self.row = 0
        self.col = 0
        self.contents = [EMPTY, EMPTY, EMPTY]
        self.is_moving = True
