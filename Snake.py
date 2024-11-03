import pygame
import time
import random
import math

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
light_green = (144, 238, 144)
orange = (255, 165, 0)
red = (255, 0, 0)
grey = (169, 169, 169)
yellow = (255, 255, 0)
beige = (245, 245, 220)
pink = (255, 182, 193)

display_width = 800
display_height = 600
block_size = 20
clock = pygame.time.Clock()

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snake Game')

font_style = pygame.font.SysFont("bahnschrift", 20)
score_font = pygame.font.SysFont("comicsansms", 20)

def Your_score(score):
    value = score_font.render("Your Score: " + str(score), True, black)
    gameDisplay.blit(value, [10, 10])

def our_snake(block_size, snake_List):
    for x in snake_List:
        pygame.draw.rect(gameDisplay, black, [x[0], x[1], block_size, block_size])
    # Add eyes
    if len(snake_List) > 0:
        head = snake_List[-1]
        eye_radius = 2
        eye_offset_x = block_size // 4
        eye_offset_y = block_size // 4
        pygame.draw.circle(gameDisplay, yellow, (int(head[0] + block_size // 2 - eye_offset_x), int(head[1] + block_size // 2 - eye_offset_y)), eye_radius)
        pygame.draw.circle(gameDisplay, yellow, (int(head[0] + block_size // 2 + eye_offset_x), int(head[1] + block_size // 2 - eye_offset_y)), eye_radius)

def draw_food_as_cat(x, y, block_size):
    # Cat
    body_width = block_size
    body_height = block_size * 1.5
    head_radius = block_size // 2
    body_rect = pygame.Rect(int(x), int(y), int(body_width), int(body_height))
    head_center = (int(x + body_width // 2), int(y))
    pygame.draw.ellipse(gameDisplay, beige, body_rect)
    pygame.draw.circle(gameDisplay, beige, head_center, head_radius)
    ear_height = head_radius
    left_ear = [
        (head_center[0] - head_radius // 2, head_center[1]),
        (head_center[0] - head_radius, head_center[1] - ear_height),
        (head_center[0], head_center[1] - ear_height // 2)
    ]
    right_ear = [
        (head_center[0] + head_radius // 2, head_center[1]),
        (head_center[0] + head_radius, head_center[1] - ear_height),
        (head_center[0], head_center[1] - ear_height // 2)
    ]
    pygame.draw.polygon(gameDisplay, beige, left_ear)
    pygame.draw.polygon(gameDisplay, beige, right_ear)
    eye_radius = 2
    eye_offset_x = head_radius // 2
    eye_offset_y = head_radius // 4
    pygame.draw.circle(gameDisplay, black, (head_center[0] - eye_offset_x, head_center[1] + eye_offset_y), eye_radius)
    pygame.draw.circle(gameDisplay, black, (head_center[0] + eye_offset_x, head_center[1] + eye_offset_y), eye_radius)
    nose_point = (head_center[0], head_center[1] + head_radius // 2)
    pygame.draw.polygon(gameDisplay, pink, [
        (nose_point[0], nose_point[1]),
        (nose_point[0] - 2, nose_point[1] + 2),
        (nose_point[0] + 2, nose_point[1] + 2)
    ])
    mouth_rect = pygame.Rect(nose_point[0] - 5, nose_point[1], 10, 5)
    pygame.draw.arc(gameDisplay, black, mouth_rect, math.pi / 8, math.pi - math.pi / 8, 1)
    whisker_length = head_radius
    pygame.draw.line(gameDisplay, black,
                     (head_center[0] - eye_offset_x - 2, head_center[1] + eye_offset_y),
                     (head_center[0] - eye_offset_x - whisker_length, head_center[1] + eye_offset_y - 2), 1)
    pygame.draw.line(gameDisplay, black,
                     (head_center[0] + eye_offset_x + 2, head_center[1] + eye_offset_y),
                     (head_center[0] + eye_offset_x + whisker_length, head_center[1] + eye_offset_y - 2), 1)
    leg_width = block_size // 8
    leg_height = block_size // 3
    leg_positions = [
        (int(x + body_width * 0.2), int(y + body_height - leg_height)),
        (int(x + body_width * 0.4), int(y + body_height - leg_height)),
        (int(x + body_width * 0.6), int(y + body_height - leg_height)),
        (int(x + body_width * 0.8), int(y + body_height - leg_height))
    ]
    for pos in leg_positions:
        leg_rect = pygame.Rect(pos[0], pos[1], leg_width, leg_height)
        pygame.draw.rect(gameDisplay, beige, leg_rect)
    tail_start = (int(x + body_width), int(y + body_height // 2))
    tail_points = [
        tail_start,
        (tail_start[0] + block_size // 2, tail_start[1] - block_size // 4),
        (tail_start[0] + block_size, tail_start[1] + block_size // 2)
    ]
    pygame.draw.lines(gameDisplay, beige, False, tail_points, 2)

# Display messages
def message(msg, color, position):
    mesg = font_style.render(msg, True, color)
    text_rect = mesg.get_rect(center=position)
    gameDisplay.blit(mesg, text_rect)

def gameLoop():
    game_over = False
    game_close = False

    # Difficulty level
    gameDisplay.fill(white)
    message("Select Difficulty Level:", black, (display_width / 2, display_height / 5))
    button_b = pygame.Rect(display_width / 2 - 75, display_height / 2.5 - 80, 150, 50)
    button_i = pygame.Rect(display_width / 2 - 75, display_height / 2.5, 150, 50)
    button_a = pygame.Rect(display_width / 2 - 75, display_height / 2.5 + 80, 150, 50)

    pygame.draw.rect(gameDisplay, light_green, button_b)
    message("Beginner", black, (button_b.centerx, button_b.centery))
    pygame.draw.rect(gameDisplay, orange, button_i)
    message("Intermediate", black, (button_i.centerx, button_i.centery))
    pygame.draw.rect(gameDisplay, red, button_a)
    message("Advanced", black, (button_a.centerx, button_a.centery))
    pygame.display.update()

    difficulty_selected = False
    while not difficulty_selected:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_b.collidepoint(event.pos):
                    snake_speed = 5
                    difficulty_selected = True
                elif button_i.collidepoint(event.pos):
                    snake_speed = 10
                    difficulty_selected = True
                elif button_a.collidepoint(event.pos):
                    snake_speed = 15
                    difficulty_selected = True

    x1 = display_width / 2
    y1 = display_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    # Food
    foodx = round(random.randrange(0, display_width - block_size) / block_size) * block_size
    foody = round(random.randrange(0, display_height - block_size) / block_size) * block_size

    frame_count = 0

    while not game_over:

        while game_close == True:
            gameDisplay.fill(white)
            message("You Lost! Press Q-Quit or P-Play Again", red, (display_width / 2, display_height / 3))
            Your_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_p:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -block_size
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = block_size
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -block_size
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = block_size
                    x1_change = 0
        if x1 >= display_width or x1 < 0 or y1 >= display_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        gameDisplay.fill(grey)
        frame_count += 1
        amplitude = 3
        cat_jump_offset = math.sin(frame_count * 0.2) * amplitude
        draw_food_as_cat(foodx, foody + cat_jump_offset, block_size)

        # Snake
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(block_size, snake_List)
        Your_score(Length_of_snake - 1)

        pygame.display.update()
        snake_rect = pygame.Rect(x1, y1, block_size, block_size)
        cat_rect = pygame.Rect(foodx, foody, block_size, int(block_size * 1.5))

        if snake_rect.colliderect(cat_rect):
            foodx = round(random.randrange(0, display_width - block_size) / block_size) * block_size
            foody = round(random.randrange(0, display_height - block_size) / block_size) * block_size
            Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
