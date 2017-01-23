import pygame
import random
from pygame.locals import *

class Cell:
    def __init__(self, i, j, size, alive=False):
        self.i = i
        self.j = j
        self.size = size
        self.alive = alive

    def is_alive(self):
        return self.alive

    def set_alive(self, alive):
        self.alive = alive

    def draw(self, screen):
        pygame.draw.rect(screen, pygame.Color('green' if self.alive else 'white'),
                         Rect(self.j * self.size, self.i * self.size, self.size, self.size))


class CellList:
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size

        self.cells = []
        for i in range(0, height):
            line = []
            for j in range(0, width):
                line.append(Cell(i, j, cell_size, random.random() > 0.5))

            self.cells.append(line)

    def draw(self, screen):
        for line in self.cells:
            [cell.draw(screen) for cell in line]

    def update(self):
        new_cells = []
        for i in range(0, self.height):
            line = []
            for j in range(0, self.width):
                alive_count = 0
                for n in self.get_neighbours(self.cells[i][j]):
                    alive_count += 1 if n.is_alive() else 0

                if alive_count < 2 or alive_count > 3:
                    line.append(Cell(i, j, self.cell_size, False))

                elif alive_count == 3:
                    line.append(Cell(i, j, self.cell_size, True))

                else:
                    line.append(Cell(i, j, self.cell_size, self.cells[i][j].is_alive()))

            new_cells.append(line)

        self.cells = new_cells

    def get_neighbours(self, cell):
        """
        Вернуть список соседних клеток для клетки cell
        Соседними считаются клетки по горизонтали,
        вертикали и диагоналям, то есть во всех
        направлениях.
        """
        neighbours = []
        for i in range(cell.i - 1, cell.i + 2):
            for j in range(cell.j - 1, cell.j + 2):
                if i < 0 or j < 0 or i >= self.height or j >= self.width or (i == cell.i and j == cell.j):
                    continue

                neighbours.append(self.cells[i][j])

        return neighbours


class GameOfLife:
    def __init__(self, width=640, height=480, cell_size=10, speed=10):
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Скорость протекания игры
        self.speed = speed

        self.cells = CellList(width // cell_size, height // cell_size, cell_size)

    def draw_grid(self):
        # http://www.pygame.org/docs/ref/draw.html#pygame.draw.line
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), (0, y), (self.width, y))

    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.cells.update()
            self.cells.draw(self.screen)
            self.draw_grid()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

if __name__ == '__main__':
    game = GameOfLife(320, 240, 20)
    game.run()