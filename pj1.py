import pygame
import numpy as np
import os

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600

BLACK = (0,0,0)
WHITE = (255,255,255)


class Image:
    def __init__(self,pic):
        self.pic = pic
        if pic == "O":
            self.img = loadImage("O")
        elif pic == "X":
            self.img = loadImage("X")
        self.move = []


class Choice:
    def __init__(self):
        self.move = ['','','','','','','','','']
    def update(self, pl, en, screen, rect):
        for mv_p in pl.move:
            if mv_p not in self.move:
                self.move[mv_p] = pl.pic
        for mv_e in en.move:
            if mv_e not in self.move:
                self.move[mv_e] = en.pic
        for i in range(9):
            if self.move[i] == 'O':
                screen.blit(loadImage('O'),rect[i])
            if self.move[i] == 'X':
                screen.blit(loadImage('X'),rect[i])


def loadImage(img):
    current_path = os.path.dirname(__file__)
    assets_path = os.path.join(current_path, 'assets')

    img_board = pygame.image.load(os.path.join(assets_path, "ttt_board.png"))
    img_O = pygame.image.load(os.path.join(assets_path, "ttt_O.png"))
    img_X = pygame.image.load(os.path.join(assets_path, "ttt_X.png"))
    
    if img == 'board':
        return img_board
    elif img == 'O':
        return img_O
    elif img == 'X':
        return img_X

def isWinner(bo, le):

    return ((bo[6] == le and bo[7] == le and bo[8] == le) or # across the top
    (bo[3] == le and bo[4] == le and bo[5] == le) or # across the middle
    (bo[0] == le and bo[1] == le and bo[2] == le) or # across the bottom
    (bo[6] == le and bo[3] == le and bo[0] == le) or # down the left side
    (bo[7] == le and bo[4] == le and bo[1] == le) or # down the middle
    (bo[8] == le and bo[5] == le and bo[2] == le) or # down the right side
    (bo[6] == le and bo[4] == le and bo[2] == le) or # diagonal
    (bo[8] == le and bo[4] == le and bo[0] == le))

def getFirstTurn():
    a = np.random.randint(0,2)
    if a == 1:
        return 1
    else:
        return 0

def boardCopy(bo):
    copy = []
    for i in bo:
        copy.append(i)
    return copy

def enemyMove(bo, le):
    if le == 'O':
        pl = 'X'
    if le == 'X':
        pl = 'O'

    corner = [0,2,6,8]
    
    for i in range(9):
        if bo[i] == '':
            bo[i] = le
            
            if isWinner(bo,le):
                print('enemyWin')
                return i
            else:
                bo[i] = ''

    for i in range(9):
        if bo[i] == '':
            bo[i] = pl
            if isWinner(bo,pl):
                print('playerWin')
                return i
            else:
                bo[i] = ''
        
    for i in corner:
        if bo[i] == '':
            print('corner')
            return i
    

    if bo[4] == '':
        print('center')
        return 4
    
    for i in range(9):
            if bo[i] == '':
                print('random')
                return i
    
    return

class minimax():
    def __init__(self,board,le):
        self.bo = board
        if le == 'O':
            self.le = 'O'
            self.pl = 'X'
        if le == 'X':
            self.le = 'X'
            self.pl = 'O'
    
    def update(self,board):
        self.bo = board
    def evaluate(self):

        if isWinner(self.bo, self.le):
            return 1
        if isWinner(self.bo, self.pl):
            return -1
        
        for i in range(9):
            if self.bo[i] == '':
                return 2
        return 0

    def max(self):
        x = None
        
        max_eval = -2
        Eval = self.evaluate()
        if Eval != 2:
            return (Eval, 0)
        
        for i in range(9):
            if self.bo[i] == '':
                self.bo[i] = self.le
                min_eval = self.min()[0]
                if max_eval < min_eval:
                    max_eval = min_eval
                    x = i
                self.bo[i] = ''
        
        return (max_eval,x)


    def min(self):
        
        x = None

        min_eval = 2
        Eval = self.evaluate()
        if Eval != 2:
            return (Eval, 0)

        for i in range(9):
            if self.bo[i] == '':
                self.bo[i] = self.pl
                max_eval = self.max()[0]
                if min_eval > max_eval:
                    min_eval = max_eval
                    x = i
                self.bo[i] = ''
        
        return (min_eval,x)
    

        
def fullCheck(bo):
    for i in range(9):
        if bo[i] == '':
            return False
    
    return True

def main():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    msg = 'Press any space to start'
    font_title = pygame.font.SysFont('arial', 40, True, False)
    font_msg = pygame.font.SysFont('arial', 24, True, False)
    text_title = font_title.render('Tic-Tac-Toe!',True,BLACK)
    text_msg = font_msg.render(msg,True,BLACK)

    img_board = loadImage('board')
    img_O = loadImage('O')
    img_X = loadImage('X')
    board_x = WINDOW_WIDTH/2 - img_board.get_rect().w/2
    board_y = WINDOW_HEIGHT-img_board.get_rect().height - 50
    
    img_O_rect = pygame.Rect(WINDOW_WIDTH/3 - img_O.get_rect().centerx, WINDOW_HEIGHT-img_board.get_rect().height - 130,img_O.get_rect().width,img_O.get_rect().height)
    img_X_rect = pygame.Rect(WINDOW_WIDTH * 2/3 - img_X.get_rect().centerx, WINDOW_HEIGHT-img_board.get_rect().height - 130,img_X.get_rect().width,img_X.get_rect().height)

    # for visually checking the size of clickable space
    clickspace = pygame.Surface((90,90))
    clickspace.fill(WHITE)

    clickSpace = []
    clickSpace.append([board_x + 50,WINDOW_HEIGHT/2 + 150])
    clickSpace.append([WINDOW_WIDTH/2 +5 - clickspace.get_rect().centerx,WINDOW_HEIGHT/2 + 150])
    clickSpace.append([board_x + 270,WINDOW_HEIGHT/2 +150])
    clickSpace.append([board_x + 50,WINDOW_HEIGHT/2 + 40])
    clickSpace.append([WINDOW_WIDTH/2 +5 - clickspace.get_rect().centerx,WINDOW_HEIGHT/2 + 40])
    clickSpace.append([board_x + 270,WINDOW_HEIGHT/2 +40])
    clickSpace.append([board_x + 50,WINDOW_HEIGHT/2 - 70])
    clickSpace.append([WINDOW_WIDTH/2 +5 - clickspace.get_rect().centerx,WINDOW_HEIGHT/2 - 70])
    clickSpace.append([board_x + 270,WINDOW_HEIGHT/2 -70])

    # define Rect of clickable space
    cS_rect = []
    for i in range(9):
        cS_rect.append(pygame.Rect(clickSpace[i][0],clickSpace[i][1], clickspace.get_width(),clickspace.get_height()))
    
    # define empty surface of clickable space
    space = []
    for i in range(9):
        space.append(clickspace)
    

    done = False

    isStart = False
    isChosen = False
    isOver = False
    
    
    turn = getFirstTurn()
    all_choice = Choice()
    
    while not done:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not isStart:
                    isStart = True
                elif not isChosen:
                    if img_O_rect.collidepoint(event.pos):
                        print('chose O')
                        isChosen = True
                        player = Image('O')
                        enemy = Image('X')
                        mm = minimax(boardCopy(all_choice.move),enemy.pic)
                        
                        
                    elif img_X_rect.collidepoint(event.pos):
                        print('chose X')
                        isChosen = True
                        player = Image('X')
                        enemy = Image('O')
                        mm = minimax(boardCopy(all_choice.move),enemy.pic)

                if isChosen and not isOver:
                    for i in range(len(cS_rect)):
                        if cS_rect[i].collidepoint(event.pos):
                            if all_choice.move[i] == '':
                                player.move.append(i)
                                all_choice.update(player,enemy,screen,cS_rect)
                                mm.bo = boardCopy(all_choice.move)
                                turn = 0
        

                            
                            


        text_msg = font_msg.render(msg,True,BLACK)
        screen.fill(WHITE) # fill screen at first
        screen.blit(img_board,(board_x, board_y))
        screen.blit(text_msg, [WINDOW_WIDTH/2 - text_msg.get_rect().centerx,100])

        #----------Game Start----------------
        if not isStart:
            screen.blit(text_title, [WINDOW_WIDTH/2 - text_title.get_rect().centerx,20])
            screen.blit(text_msg, [WINDOW_WIDTH/2 - text_msg.get_rect().centerx,100])
        elif not isChosen:
            msg = "Choose 'O' or 'X'"
            screen.blit(img_O,(WINDOW_WIDTH/3 - img_O.get_rect().centerx, WINDOW_HEIGHT-img_board.get_rect().height - 130))
            screen.blit(img_X,(WINDOW_WIDTH * 2/3 - img_X.get_rect().centerx, WINDOW_HEIGHT-img_board.get_rect().height - 130))
        
        if isChosen:
            msg = 'Play!'
            all_choice.update(player,enemy,screen,cS_rect)
            
            
            if isWinner(all_choice.move,player.pic):
                msg = 'Win!'
                isOver = True
            elif isWinner(all_choice.move,enemy.pic):
                msg = 'Lose..'
                isOver = True
            elif fullCheck(all_choice.move):
                msg = 'Draw'
                isOver = True
            elif turn == 0:
                
                
                #enemy.move.append(enemyMove(boardCopy(all_choice.move),enemy.pic))
                #enemy.move.append(max(boardCopy(all_choice.move),enemy.pic)[1])
                enemy.move.append(mm.max()[1])
                
                all_choice.update(player,enemy,screen,cS_rect)
                
                mm.bo = boardCopy(all_choice.move)
                
                turn = 1

        
        pygame.display.flip()
        clock.tick(60)       


    return




if __name__ == '__main__':
    pygame.init()
    main()
    
    pygame.quit()