import pygame
import random
import os
pygame.mixer.init()
pygame.init()
screen_width = 900
screen_height = 600
gamewindow = pygame.display.set_mode((screen_width, screen_height))
bgimg = pygame.image.load("./files/bgimg.png")
bgimg = pygame.transform.scale(
    bgimg, (screen_width, screen_height)).convert_alpha()
pygame.display.set_caption("SnakesWithAjay")
pygame.display.update()


def game_loop():
    # colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 100, 0)
    # game variables
    score = 0
    exit_game = False
    game_over = False
    clock = pygame.time.Clock()
    velocity_x = 0
    velocity_y = 0

    initial_velocity = 5
    snake_x = 50
    snake_y = 55
    snake_size = 10
    fps = 30
    if (not os.path.exists("./files/high_score.txt")):
        with open("./files/high_score.txt", "w") as f:
            f.write("0")
    with open("./files/high_score.txt", "r") as f:
        high_score = f.read()

    food_x = random.randint(20, screen_width/2)
    food_y = random.randint(20, screen_height/2)
    font = pygame.font.SysFont(None, 40)

    def text_screen(text, color, x, y):
        screen_text = font.render(text, True, color)
        gamewindow.blit(screen_text, [x, y])

    def plot_snake(gamewindow, color, snake_list, snake_size):
        for snake_x, snake_y in snake_list:
            pygame.draw.rect(gamewindow, black, [
                             snake_x, snake_y, snake_size, snake_size])

    snake_length = 1
    snake_list = []

    while not exit_game:
        if game_over:
            with open("./files/high_score.txt", "w") as f:
                f.write(str(high_score))
            gamewindow.fill(white)
            text_screen("Game Over, enter to continue", green, 250, 250)
            text_screen("Your Score: " + str(score), green, 320, 280)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_loop()
        else:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        velocity_y = initial_velocity
                        velocity_x = 0

                    if event.key == pygame.K_UP:
                        velocity_y = -initial_velocity
                        velocity_x = 0
                    if event.key == pygame.K_LEFT:
                        velocity_y = 0
                        velocity_x = -initial_velocity
                    if event.key == pygame.K_RIGHT:
                        velocity_y = 0
                        velocity_x = initial_velocity
                if event.type == pygame.QUIT:
                    exit_game = True

            snake_x += velocity_x
            snake_y += velocity_y

            if abs(snake_x - food_x) < 6 and abs(snake_y - food_y) < 6:
                score += 10
                fps += 5
                pygame.mixer.music.load("./files/beep.mp3")
                pygame.mixer.music.play()
                food_x = random.randint(20, screen_width/2)
                food_y = random.randint(20, screen_height/2)
                snake_length += 5
                if score > int(high_score):
                    high_score = score

            gamewindow.fill(white)
            gamewindow.blit(bgimg, (0, 0))
            text_screen("Score: " + str(score) +
                        "  High Score: " + str(high_score), green, 5, 5)
            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)
            if len(snake_list) > snake_length:
                del snake_list[0]

            if head in snake_list[:-1]:
                game_over = True
                pygame.mixer.music.load("./files/bomb.mp3")
                pygame.mixer.music.play()

            if snake_x < 0:
                snake_x = screen_width
            if snake_x > screen_width:
                snake_x = 0
            if snake_y < 0:
                snake_y = screen_height
            if snake_y > screen_height:
                snake_y = 0
            # This below 4 lines of code is to do gameover on touch snake with walls
            # if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
            #     game_over = True
            #     pygame.mixer.music.load("bomb.mp3")
            #     pygame.mixer.music.play()

            pygame.draw.rect(gamewindow, red, [
                             food_x, food_y, snake_size, snake_size])
            plot_snake(gamewindow, black, snake_list, snake_size)
        pygame.display.update()
        clock.tick(fps)
    pygame.quit()
    quit()


game_loop()
