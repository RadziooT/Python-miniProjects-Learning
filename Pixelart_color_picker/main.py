import pygame
pygame.display.init()
import time

class Grid:

    def __init__(self,row,column,width,height,colors):
        self.row = row
        self.column = column
        self.width = width
        self.height = height
        self.position = None
        self.cubes = [[Cube(i, j, width, height,colors,self.row) for j in range(column)] for i in range(row)]
        self.fill = False

    def draw(self,screen):
        gap = self.width/self.row
        if(self.fill == True):
            self.fill_event()
        for i in range(self.row):
            for j in range(self.column):
                self.cubes[i][j].draw(screen)
                pygame.draw.line(screen, (0, 0, 0), (0, gap * j), (self.width, gap * j), 1)
                pygame.draw.line(screen, (0, 0, 0), (gap * i, 0), (gap * i, self.height), 1)
        self.fill = False

    def fill_event(self):
        for i in range(self.row):
            for j in range(self.column):
                self.cubes[i][j].fill(self.setcolor)

    def set_position(self,pos):
        self.position = pos

    def setfill(self,bool):
        self.fill = bool

    def cube_clicked(self,pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / self.row
            x = pos[0] // gap
            y = pos[1] // gap
            self.setcolor = self.cubes[int(x)][int(y)].get_color()
            self.cubes[int(x)][int(y)].next_color()

class Cube:

    def __init__(self,row,column,width,height,colors,n):
        self.n = n
        self.row = row
        self.column = column
        self.width = width
        self.height = height
        self.colors = colors
        self.color = self.colors[0]

    def get_color(self):
        return self.color

    def fill(self,color):
        self.color = color

    def draw(self,screen):
        gap = self.width / self.n
        x = gap * self.row
        y = gap * self.column
        pygame.draw.rect(screen,self.color,(x,y,gap,gap),0)

    def next_color(self):
        if (self.color == self.colors[-1]):
            self.color = self.colors[0]
        else:
            self.color = self.colors[self.colors.index(self.color)+1]

def redraw_window(screen, Grid):
    screen.fill((255,255,255))
    Grid.draw(screen)

def main():
    colors = ['yellow', 'red', 'blue', 'green', 'black', 'white']
    game = pygame.display.set_mode((540, 540))
    pygame.display.set_caption("Color picker")
    board = Grid(18, 18, 540, 540, colors)
    key = None
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    pos = pygame.mouse.get_pos()
                    board.setfill(True)
                    board.cube_clicked(pos)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                time.sleep(0.15)
                board.cube_clicked(pos)
        redraw_window(game, board)
        pygame.display.update()

main()
pygame.quit()
