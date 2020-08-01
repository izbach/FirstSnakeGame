import pygame
import random
import time
from random import choice

pygame.init()

display_width = 800
display_height = 600
grid_unit_size = 20
PAUSE = False

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Snake!!")

black = (0,0,0)
white = (255,255,255)
red = (247, 147, 131)
green = (131, 242, 142)
bright_green = (0,255,0)
bright_red = (255,0,0)

clock = pygame.time.Clock()

def find_x_and_y(snake_ids):
    rangeX = int(display_width/grid_unit_size -1)
    rangeY = int(display_height/grid_unit_size -1)
    non_usable_xs = []
    non_usable_ys = []
    for snake in snake_ids:
        non_usable_xs.append(snake[0]/grid_unit_size)
        non_usable_ys.append(snake[1]/grid_unit_size)
    xVal = choice([i for i in range(0, rangeX) if i not in non_usable_xs]) * grid_unit_size
    yVal = choice([i for i in range(0, rangeY) if i not in non_usable_ys]) * grid_unit_size

    return xVal, yVal
def draw_apple(xVal, yVal):
    pygame.draw.rect(gameDisplay, bright_red, [xVal, yVal, grid_unit_size, grid_unit_size])
def apples(prevApple, snake_ids, score):
    if prevApple == []:
        xVal, yVal = find_x_and_y(snake_ids)
        prevApple.append(xVal)
        prevApple.append(yVal)
        draw_apple(xVal, yVal)

    elif prevApple[0] == snake_ids[0][0] and prevApple[1] == snake_ids[0][1]:

        xVal, yVal = find_x_and_y(snake_ids)
        prevApple.clear()
        prevApple.append(xVal)
        prevApple.append(yVal)
        draw_apple(xVal, yVal)
        snake_ids.append([snake_ids[-1][0], snake_ids[-1][1]])
        score += 1

    else:    
        draw_apple(prevApple[0], prevApple[1])


    return score


def quitgame():
    pygame.quit()
    quit()

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2), (display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(2)

    game_intro()


def crash():
    
    message_display('You Died!')
    

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    buttonText = pygame.font.Font('freesansbold.ttf', 75)
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    textSurf, textRect = text_objects(msg, buttonText)
    textRect.center = ((x+(w/2)), (y+(h/2)))

    gameDisplay.blit(textSurf, textRect)

def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        largeText = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects("Snake!!", largeText)
        TextRect.center = ((display_width/2), 200)
        gameDisplay.blit(TextSurf, TextRect)
        
        button("Start", 0, 400, 400, 200, green, bright_green, game_loop)
        button("Close", 400, 400, 400, 200, red, bright_red, quitgame)

        pygame.display.update()
        clock.tick(15)

def unpause():
    global PAUSE

    PAUSE = False



def paused():
    global PAUSE

    while PAUSE:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        largeText = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects("Snake!!", largeText)
        TextRect.center = ((display_width/2), 200)
        gameDisplay.blit(TextSurf, TextRect)
        
        button("Continue", 0, 400, 400, 200, green, bright_green, unpause)
        button("Close", 400, 400, 400, 200, red, bright_red, quitgame)

        pygame.display.update()
        clock.tick(15)
        

def score_count(score):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Score: "+str(score), True, black)
    gameDisplay.blit(text, (0,0))


def snake_movement(snake_direction, snake_ids, count, deathFunc=crash):

    lead_position_x = snake_ids[0][0]
    lead_position_y = snake_ids[0][1]
    if snake_direction == 'right' and count == 3:
        snake_ids[0][0] += grid_unit_size
    elif snake_direction == 'left' and count == 3:
        snake_ids[0][0] -= grid_unit_size
    elif snake_direction == 'up' and count == 3:
        snake_ids[0][1] -= grid_unit_size
    elif snake_direction == 'down' and count == 3:
        snake_ids[0][1] += grid_unit_size

    
    if snake_ids[0][0] < 0 or snake_ids[0][0] + grid_unit_size > display_width:
        return deathFunc()
    elif snake_ids[0][1] < 0 or snake_ids[0][1] + grid_unit_size > display_height:
        return deathFunc()

    pygame.draw.rect(gameDisplay, black, [snake_ids[0][0], snake_ids[0][1], grid_unit_size, grid_unit_size])
    if count == 3:
        for snake in snake_ids[1:]:
            if snake == snake_ids[0]:
                return deathFunc()
            else:
                prev_position_x = snake[0]
                prev_position_y = snake[1]
                
                snake[0] = lead_position_x
                snake[1] = lead_position_y
                pygame.draw.rect(gameDisplay, black, [snake[0], snake[1], grid_unit_size, grid_unit_size])
                lead_position_x = prev_position_x
                lead_position_y = prev_position_y
    else:
        for snake in snake_ids[1:]:
            pygame.draw.rect(gameDisplay, black, [snake[0], snake[1], grid_unit_size, grid_unit_size])






def game_loop():

    global PAUSE

    snake_ids = [[400,300], [380, 300], [360, 300], [340, 300]]
    snake_direction = "right"
    snake_movement_count = 0
    game_over = False
    prevApple = []
    score = 0


    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    snake_direction = 'right'
                if event.key == pygame.K_LEFT:
                    snake_direction = 'left'
                if event.key == pygame.K_UP:
                    snake_direction = 'up'
                if event.key == pygame.K_DOWN:
                    snake_direction = 'down'
                if event.key == pygame.K_p:
                    PAUSE = True
                    paused()


        gameDisplay.fill(white)
        snake_movement_count += 1
        
        snake_movement(snake_direction, snake_ids, snake_movement_count, crash)
        score = apples(prevApple, snake_ids, score)
        score_count(score)
        if snake_movement_count == 3:
            snake_movement_count = 0
        pygame.display.update()
        clock.tick(30)

game_intro()
game_loop()
pygame.quit()
quit()