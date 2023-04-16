import pygame
from solver import check_valid, solve_sudoku
pygame.font.init()
import time

class GameGrid:
    board = [
           [7, 8, 0, 4, 0, 0, 1, 2, 0],
           [6, 0, 0, 0, 7, 5, 0, 0, 9],
           [0, 0, 0, 6, 0, 1, 0, 7, 8],
           [0, 0, 7, 0, 4, 0, 2, 6, 0],
           [0, 0, 1, 0, 5, 0, 9, 3, 0],
           [9, 0, 4, 0, 6, 0, 0, 0, 5],
           [0, 7, 0, 3, 0, 0, 0, 1, 2],
           [1, 2, 0, 0, 0, 7, 4, 0, 0],
           [0, 4, 9, 2, 0, 6, 0, 0, 7]
       ]

    def __init__(self,rows,columns,width,height):
        self.rows = rows
        self.columns = columns
        self.width = width
        self.height = height
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(columns)] for i in range(rows)]
        self.selected_pos = None
        self.model = None
        self.selected = None

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.columns)] for i in range(self.rows)]

    def draw(self,game):
        gap = self.width / self.rows #space for each cube
        #writing lines of the sudoku grid
        for i in range(self.rows+1):
                if(i % 3 == 0):
                    thickness = 5
                else:
                    thickness = 1
                pygame.draw.line(game, (0, 0, 0), (0, gap * i), (self.width, gap * i), thickness)
                pygame.draw.line(game, (0, 0, 0), (gap * i, 0), (gap * i, self.height), thickness)
        #filling each cube with value from the cube class
        for i in range(self.rows):
            for j in range(self.columns):
                self.cubes[i][j].draw(game)

    def set_permanent_value(self,value):
        row, column = self.selected_pos
        if self.cubes[row][column].value == 0 and self.cubes[row][column].tmp != 0:
            self.cubes[row][column].set_value(value)
            self.update_model()
        if check_valid(self.model, value, (row, column)) and solve_sudoku(self.model):
            return True
        else:
            self.cubes[row][column].set_value(0)
            self.cubes[row][column].set_temp_number(0)
            self.clear_selected()
            self.update_model()
            return False

    def set_temp_value(self,value):
        row, column = self.selected_pos
        self.cubes[row][column].tmp = value

    def select_cube(self,position):
        #reset selection of other cubes
        if position[0] < self.width and position[1] < self.height:
            for i in range(self.rows):
                for j in range(self.columns):
                    self.cubes[i][j].selected = False
            #print border of the selected cube
            gap = self.width / 9
            x = int(position[1] // gap)
            y = int(position[0] // gap)
            self.cubes[x][y].selected = True
            self.selected_pos = (x, y)
            self.selected = True

    def clear_selected(self):
        row, column = self.selected_pos
        if self.cubes[row][column].value == 0:
            self.cubes[row][column].set_temp_number(0)

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True

class Cube:

    def __init__(self,value,row,column,width,height):
        self.value = value
        self.tmp = 0
        self.row = row
        self.column = column
        self.width = width
        self.height = height
        self.selected = False

    def draw(self,game):
        gap = self.width / 9
        x_coordinate = gap * self.column
        y_coordinate = gap * self.row
        #printing "pencil drawn" numbers
        if (self.tmp != 0 and self.value == 0):
            font = pygame.font.SysFont('Comic Sans MS', 30)
            text = font.render(str(self.tmp),True,'Grey')
            game.blit(text, (x_coordinate + 10, y_coordinate))
        elif self.value != 0 :
        #printing "set" numbers
            font = pygame.font.SysFont('Comic Sans MS', 30)
            text = font.render(str(self.value),True,'Black')
            game.blit(text, (x_coordinate + (gap / 2 - text.get_width() / 2), y_coordinate + (gap / 2 - text.get_height() / 2)))
        #printing border of the selected cube
        if self.selected:
            pygame.draw.rect(game,'Red',(x_coordinate, y_coordinate, gap, gap),5)

    def set_temp_number(self,value):
        self.tmp = value

    def set_value(self,value):
        self.value = value


#function constantly refreshing the board
def redraw_board(game,board,strikes,time):
    game.fill((255, 255, 255))
    board.draw(game)
    font = pygame.font.SysFont('Comic Sans MS', 60)
    #printing time
    text = font.render("Time: " + format_playtime(time),True,'Black')
    game.blit(text, (board.width-text.get_width(), board.height-10))
    #printing strikes
    text = font.render(str(strikes)+"X",True,'Red')
    game.blit(text, (20, board.height-10))

def lose_screen(game,board):
    game.fill((255, 255, 255))
    font = pygame.font.SysFont('Comic Sans MS', 60)
    text = font.render("YOU LOST", True, 'Red')
    game.blit(text, ((board.width - text.get_width()) / 2, (board.height - text.get_height()) / 2))
    tmp = text.get_height()
    text = font.render("Press enter", True, 'Red')
    game.blit(text, ((board.width - text.get_width()) / 2, (board.height - text.get_height()) / 2 + tmp))
    tmp = tmp + text.get_height()
    text = font.render("to continue", True, 'Red')
    game.blit(text, ((board.width - text.get_width()) / 2, (board.height - text.get_height()) / 2 + tmp))
    pygame.display.update()

def format_playtime(time):
    hours = int(time / 3600)
    minutes = int((time - hours * 3600)/60)
    seconds = time - hours * 3600 - minutes * 60
    text = str(hours)+ ":" + str(minutes) + ":" + str(seconds)
    return text

def main():
    game = pygame.display.set_mode((540, 600))
    pygame.display.set_caption("Sudoku")
    board = GameGrid(9, 9, 540, 540)
    running = True
    key = None
    strikes = 0
    start = time.time()
    while running:

        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear_selected()
                    key = None
                if event.key == pygame.K_RETURN:
                    if board.selected_pos != None:
                        row, column = board.selected_pos
                        if board.cubes[row][column].tmp != 0 and board.cubes[row][column].value == 0:
                            if board.set_permanent_value(board.cubes[row][column].tmp):
                                print("Brawo!")
                            else:
                                print("Sprobuj jeszcze raz(+1 blad)")
                                strikes = strikes +1
                            key = None
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                board.select_cube(pos)
                key = None
            if board.selected and key != None:
                board.set_temp_value(key)

        if strikes > 9:
            lose_screen(game,board)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        board = GameGrid(9, 9, 540, 540)
                        running = True
                        key = None
                        strikes = 0
                        start = time.time()
        else:
            redraw_board(game, board, strikes, play_time)
            pygame.display.update()

main()
pygame.quit()