import pgzrun
import random

TITLE = "Arkanoid clone"
WIDTH = 800
HEIGHT = 500

# сложность игры
easy = Actor("easy.jpg", (200, 250))
normal = Actor("normal.jpg",(400, 250))
hard = Actor("hard.jpg", (600, 250))

paddle = Actor("paddleblue.png")
paddle.x = 120
paddle.y = 420

ball = Actor("ballblue.png")
ball.x = 30
ball.y = 300

ball_x_speed = -1.5
ball_y_speed = -1.5

bars_list = []

score = 0
game_over = False
menu = True

def draw():
    # Режим меню
    if menu:
        screen.blit("background.png", (0,0))
        screen.draw.text('Выберите сложность', center = (400, 150), color = "white", fontsize = 36)
        easy.draw()
        normal.draw()
        hard.draw()
    # Режим игры
    elif not game_over:
        screen.blit("background.png", (0,0))
        paddle.draw()
        ball.draw()
        for bar in bars_list:
            bar.draw()
        screen.draw.text(f"Score: {score} ",  (20, 30))
    else:
        screen.blit("background.png", (0,0))
        screen.draw.text(f"GAME OVER, Your score: {score} ",  (350, 150), color = "white", fontsize = 36)
        screen.draw.text("Нажниме Space, чтобы начать игру заново",  (200, 300), color = "red", fontsize = 25)

def update(dt):
    global ball_x_speed, ball_y_speed, game_over, score, menu
    if keyboard.left:
        paddle.x = paddle.x - 5
    if keyboard.right:
        paddle.x = paddle.x + 5

    update_ball()
    for bar in bars_list:
        if ball.colliderect(bar):
            scoreCount(bar.color)
            bars_list.remove(bar)
            ball_y_speed *= -1


    if paddle.colliderect(ball):
        ball_y_speed *= -1
        # randomly move ball left or right on hit
        rand = random.randint(0,1)
        if rand:
            ball_x_speed *= -1

    #рестарт
    if game_over and keyboard.space:
        start()
        menu = True 
        score = 0
        ball.pos = (30, 300)
        paddle.pos = (120, 420)
        game_over = False

def on_mouse_down(button, pos):
    global menu, ball_x_speed, ball_y_speed
    if menu and easy.collidepoint(pos):
        ball_x_speed = -1
        ball_y_speed = -1
        menu = False
    elif menu and normal.collidepoint(pos):
        ball_x_speed = -3
        ball_y_speed = -3
        menu = False
    elif menu and hard.collidepoint(pos):
        ball_x_speed = -5
        ball_y_speed = -5
        menu = False

def place_bars(x,y,image, color):
    bar_x = x
    bar_y = y
    for i in range(8):
        bar = Actor(image)
        bar.x = bar_x
        bar.y = bar_y
        bar.color = color
        bar_x += 70
        bars_list.append(bar)

def scoreCount(bar):
    global score
    if bar == "red" or bar == "blue":
        score += 1
    elif bar == "green":
        score += 2


def update_ball():
    global ball_x_speed, ball_y_speed, game_over
    ball.x -= ball_x_speed
    ball.y -= ball_y_speed
    if (ball.x >= WIDTH) or (ball.x <=0):
        ball_x_speed *= -1
    if (ball.y >= HEIGHT) or (ball.y <=0):
        ball_y_speed *= -1
    if ball.y > paddle.y+30:
        game_over = True
        ball_y_speed = 0
        ball_x_speed = 0

def start():
    global bars_list
    bars_list = []
    coloured_box_list = {"blue" : "element_blue_rectangle_glossy.png", "green" : "element_green_rectangle_glossy.png","red" : "element_red_rectangle_glossy.png"}
    x = 120
    y = 100
    for coloured_box in coloured_box_list:
        place_bars(x, y, coloured_box_list[coloured_box], coloured_box)
        y += 50

start()
pgzrun.go()