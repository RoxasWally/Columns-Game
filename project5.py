import gameboard as game
import pygame
import random

JEWEL_COLOR = {"S": (255, 0, 0), "T": (0, 255, 0), "V": (0, 0, 255), "W": (255, 255, 0), "X": (255, 128, 0),
               "Y": (102, 0, 204), "Z": (51, 255, 255)}


class Runner:
    def __init__(self):
        self.sur = None
        self.board = game.Board(13, 6)
        self.ctr = 12
        self.is_run = True
        self.bg = pygame.Color(0, 0, 0)
        self.fg = pygame.Color(102, 51, 0)
        self.bufY = 0.004
        self.sz = (1.0 - self.bufY) / self.board.rows
        self.bufX = (1.0 - (self.sz * self.board.cols))

    def incr_time(self) -> None:
        self.is_run = not self.board.time()

        if not self.board.faller.active:
            contents = random.sample(JEWEL_COLOR.keys(), 3)
            column = random.randint(1, 6)
            self.board.spawn(column, contents)

    def draw_obj(self) -> None:
        top_x = int((self.bufX / 2) * self.sur.get_height())
        top_y = int((self.bufY / 2) * self.sur.get_height())

        width = int(((self.sz * self.board.cols) - 0.001) * self.sur.get_width())
        height = int((self.sz * self.board.rows) * self.sur.get_height())

        # Draw the outline box for the game
        pygame.Rect(top_x, top_y, width, height)

        # Draw each of the individual jewels
        for row in range(self.board.rows):
            for col in range(self.board.cols):
                self._draw_jewel(row, col)

    def _draw_jewel(self, row: int, col: int) -> None:
        jewel = self.board.boardRows[row][col]
        if jewel is game.EMPTY or jewel is game.EMPTY_CELL:
            color = pygame.Color(102, 51, 0)
            state = 'OCCUPIED STATE'
        else:
            state = self.board.pieces[row][col]
            if state == game.MATCHED_CELL:
                color_hex = (255, 255, 255)
                color = pygame.Color(color_hex[0], color_hex[1], color_hex[2])
            else:
                color_hex = JEWEL_COLOR.get(jewel)
                color = pygame.Color(color_hex[0], color_hex[1], color_hex[2])

        x_pos = (col * self.sz) + (self.bufX / 2.5)
        y_pos = (row * self.sz) + (self.bufY / 2.5)

        top_x = int(x_pos * self.sur.get_width())
        top_y = int(y_pos * self.sur.get_height())

        width = int(self.sz * self.sur.get_width())
        height = int(self.sz * self.sur.get_height())

        rect = pygame.Rect(top_x, top_y, width, height)

        pygame.draw.rect(self.sur, color, rect, 0)

        if state == game.FALLER_STOPPED_CELL:
            pygame.draw.rect(self.sur, pygame.Color(255, 255, 255), rect, 2)


if __name__ == '__main__':
    g = Runner()
    pygame.init()

    try:
        clock = pygame.time.Clock()

        g.sur = pygame.display.set_mode((600,600), pygame.RESIZABLE)

        while g.is_run:
            clock.tick(12)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    g.is_run = False
                elif event.type == pygame.VIDEORESIZE:
                    g.sur = pygame.display.set_mode(event.size, pygame.RESIZABLE)

            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT]:
                g.board.move_hor(game.LEFT)

            if keys[pygame.K_RIGHT]:
                g.board.move_hor(game.RIGHT)

            if keys[pygame.K_SPACE]:
                g.board.rotate()

            g.ctr -= 1

            if g.ctr == 0:
                g.incr_time()
                g.ctr = 12
            g.sur.fill(g.bg)
            g.draw_obj()
            pygame.display.flip()

    finally:
        pygame.quit()
