import pygame
pygame.font.init()
import time
from random import randrange

class Grid:

    def __init__(self,rows,columns,width,height,color_list):
        self.color_list = color_list
        self.rows = rows
        self.columns = columns
        self.width = width
        self.height = height
        self.random_order = [0,1]
        self.cards = [[Card(color_list[0],i, j, width, height, rows) for j in range(columns)] for i in range(rows)]
        self.flipped_pos_before = None
        self.selected_pos = None
        self.flipped_one = None
        self.flipped_two = None
        self.colors_left = True

    def assign_color(self):
        for i in range(self.rows):
            for j in range(self.columns):
                self.cards[i][j].color = self.color_list[i][j]

    def draw(self,game):

        self.assign_color()

        gap = self.width / self.rows #space for each card
        #writing cards
        for i in range(self.rows):
            for j in range(self.columns):
                self.cards[i][j].draw(game)
        # writing lines of the grid
        for i in range(self.rows+1):
            pygame.draw.line(game, (0, 0, 0), (0, gap * i), (self.width, gap * i), 2)
            pygame.draw.line(game, (0, 0, 0), (gap * i, 0), (gap * i, self.height), 2)

    def flip_card(self):

        if self.flipped_pos_before == self.selected_pos:
            pass
        elif self.selected_pos != None:
            row,column = self.selected_pos
            if self.flipped_one != None and self.flipped_two == None:
                self.cards[row][column].flip()
                self.flipped_two = self.cards[row][column].color
            elif self.flipped_one == None:
                self.flipped_one = self.cards[row][column].color
                self.cards[row][column].flip()
                self.flipped_pos_before = self.selected_pos

    def compare_flipped(self):
        if self.flipped_one == self.flipped_two and self.flipped_one != None and self.flipped_two != None:
            for i in range(self.rows):
                for j in range(self.columns):
                    if self.cards[i][j].flipped:
                        self.cards[i][j].set_cant_flip_state(True)
            self.remove_select()
            self.flipped_one = None
            self.flipped_two = None
            return True
        elif self.flipped_one != None and self.flipped_two != None:
            self.unflip()
            self.remove_select()
            self.flipped_one = None
            self.flipped_two = None

            return False
        return False

    def unflip(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.cards[i][j].flipped == True:
                    self.cards[i][j].flip()

    def remove_select(self):
        for i in range(self.rows):
            for j in range(self.columns):
                self.cards[i][j].set_selected(False)
                self.selected_pos = None

    def click_select(self,pos):
        gap = self.width / self.rows
        if pos[0]<self.width and pos[1]<self.height:
            for i in range(self.rows):
                for j in range(self.columns):
                    self.cards[i][j].set_selected(False)
            column = int(pos[0]/gap)
            row = int(pos[1] / gap)
            self.cards[row][column].set_selected(True)
            self.selected_pos = row,column

    def check_if_done(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if not self.cards[i][j].flipped:
                    return False
        return True

class Card:

    def __init__(self,color,row,column,width,height,row_amount):
        self.width = width
        self.height = height
        self.color = color
        self.row = row
        self.column = column
        self.flipped = False
        self.cant_flip = False
        self.selected = False
        self.row_amount = row_amount

    def flip(self):
        if not self.cant_flip:
            self.flipped = not self.flipped

    def draw(self,game):
        gap = self.width / self.row_amount
        x_coordinate = gap * self.column
        y_coordinate = gap * self.row
        if self.flipped:
            pygame.draw.rect(game, self.color, (x_coordinate, y_coordinate, gap, gap), 0)
        else:
            pygame.draw.rect(game, 'Grey', (x_coordinate, y_coordinate, gap, gap), 0)

        if self.selected:
            pygame.draw.rect(game, 'Red', (x_coordinate, y_coordinate, gap, gap), 5)

    def set_selected(self,bool):
        self.selected = bool

    def set_cant_flip_state(self,bool):
        self.cant_flip = bool

def redraw_board(game,board,time,points):
    game.fill((255, 255, 255))
    board.draw(game)
    font = pygame.font.SysFont('Comic Sans MS', 30)
    #printing time
    text = font.render("Time: " + format_playtime(time),True,'Black')
    game.blit(text, (board.width-text.get_width(), board.height+10))
    #printing points
    text = font.render("Points:"+str(points),True,'Black')
    game.blit(text, (20, board.height+10))

def win_screen(game,board,points):
    game.fill((255, 255, 255))
    font = pygame.font.SysFont('Comic Sans MS', 60)
    text = font.render("YOU WON", True, 'Red')
    game.blit(text, ((board.width - text.get_width()) / 2, (board.height - text.get_height()) / 4))
    tmp = text.get_height()
    text = font.render("Your points: " + str(points), True, 'Black')
    game.blit(text, ((board.width - text.get_width()) / 2, (board.height - text.get_height()) / 4 + tmp))
    tmp = tmp+ text.get_height()
    text = font.render("Press R", True, 'Red')
    game.blit(text, ((board.width - text.get_width()) / 2, (board.height - text.get_height()) / 4 + tmp))
    tmp = tmp + text.get_height()
    text = font.render("to restart", True, 'Red')
    game.blit(text, ((board.width - text.get_width()) / 2, (board.height - text.get_height()) / 4 + tmp))
    pygame.display.update()

def format_playtime(time):
    hours = int(time / 3600)
    minutes = int((time - hours * 3600)/60)
    seconds = time - hours * 3600 - minutes * 60
    text = str(hours)+ ":" + str(minutes) + ":" + str(seconds)
    return text

def main():


    n = 4
    game = pygame.display.set_mode((540, 600))
    colors = [['yellow', 'red', 'blue','beige'], ['blue', 'black', 'white','purple'],['yellow', 'red', 'white','cyan'],['beige','purple','cyan','black']]
    #colors = [['yellow','cyan'],['cyan','yellow']]
    board = Grid(n, n, 540, 540, colors)
    pygame.display.set_caption("Card Game")

    print("Welcome to card game each move removes 1 point and each correct match gives you 5 points")
    print("Keep in mind that trying to flip same card multiple times removes points")

    running = True
    points = 10
    start = time.time()
    while running:

        playtime = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    board.flip_card()
                    redraw_board(game, board, playtime,points)
                    pygame.display.update()
                    if board.compare_flipped():
                        points = points + 5
                    else:
                        points = points - 1
                        time.sleep(0.2)

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                board.click_select(pos)

        if board.check_if_done():
            win_screen(game, board, points)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        board = Grid(n, n, 540, 540,colors)
                        points = 0
                        start = time.time()

        else:
            redraw_board(game,board,playtime,points)
            pygame.display.update()

main()
pygame.quit()