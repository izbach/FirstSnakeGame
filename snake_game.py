import pygame
import random
import time

pygame.init()

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Snake!!")

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

clock = pygame.time.Clock()
applImg = pygame.image.load('/home/isaac/Documents/Python_Projects/Snake_Game/apple.jpg')
def apples(prevApple, snake_ids, score):
    if prevApple == []:
        xVal = random.randrange(0, display_width/20 - 1) * 20
        yVal = random.randrange(0, display_height/20 - 1) * 20
        prevApple.append(xVal)
        prevApple.append(yVal)
        gameDisplay.blit(applImg, (xVal,yVal))
    elif prevApple[0] == snake_ids[0][0] and prevApple[1] == snake_ids[0][1]:
        xVal = random.randrange(0, display_width/20 - 1) * 20
        yVal = random.randrange(0, display_height/20 - 1) * 20
        prevApple.clear()
        prevApple.append(xVal)
        prevApple.append(yVal)
        gameDisplay.blit(applImg, (xVal,yVal))
        snake_ids.append([snake_ids[-1][0], snake_ids[-1][1]])
        score += 1

    else:    
        gameDisplay.blit(applImg, (prevApple[0], prevApple[1]))

    return score

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

    game_loop()


def crash():
    message_display('You Died!')

def score_count(score):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Score: "+str(score), True, black)
    gameDisplay.blit(text, (0,0))


def snake_movement(snake_direction, snake_ids, count):
    size = 20
    lead_position_x = snake_ids[0][0]
    lead_position_y = snake_ids[0][1]
    if snake_direction == 'right' and count == 3:
        snake_ids[0][0] += size
    elif snake_direction == 'left' and count == 3:
        snake_ids[0][0] -= size
    elif snake_direction == 'up' and count == 3:
        snake_ids[0][1] -= size
    elif snake_direction == 'down' and count == 3:
        snake_ids[0][1] += size

    
    if snake_ids[0][0] < 0 or snake_ids[0][0] + size > display_width:
        crash()
    elif snake_ids[0][1] < 0 or snake_ids[0][1] + size > display_height:
        crash()
    
    pygame.draw.rect(gameDisplay, black, [snake_ids[0][0], snake_ids[0][1], size, size])
    if count == 3:
        for snake in snake_ids[1:]:
            if snake == snake_ids[0]:
                crash()
            else:
                prev_position_x = snake[0]
                prev_position_y = snake[1]
                
                snake[0] = lead_position_x
                snake[1] = lead_position_y
                pygame.draw.rect(gameDisplay, black, [snake[0], snake[1], size, size])
                lead_position_x = prev_position_x
                lead_position_y = prev_position_y
    else:
        for snake in snake_ids[1:]:
            pygame.draw.rect(gameDisplay, black, [snake[0], snake[1], size, size])

                
    


def game_loop():

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


        gameDisplay.fill(white)
        # start movement
        # spawn the snake
        snake_movement_count += 1
        
        snake_movement(snake_direction, snake_ids, snake_movement_count)
        score = apples(prevApple, snake_ids, score)
        score_count(score)
        if snake_movement_count == 3:
            snake_movement_count = 0
        pygame.display.update()
        clock.tick(30)


game_loop()
pygame.quit()
quit()