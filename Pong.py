# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
ball_pos = [0, 0]
ball_vel = [1, 1]
paddle1_pos = HEIGHT / 2
paddle2_pos = HEIGHT / 2
paddle1_vel = 3
paddle2_vel = 3
score1 = 0
score2 = 0

# helper function that spawns a ball by updating the 
# ball's position vector and velocity vector
# if right is True, the ball's velocity is upper right, else upper left
def ball_init(right):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    if right:
        ball_vel = [random.randrange(2, 5), -random.randrange(2, 5)]
    else:
        ball_vel = [-random.randrange(2, 5), -random.randrange(2, 5)]        

# define event handlers

def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are floats
    global score1, score2  # these are ints
    ball_init(True)

def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    
    paddle1Range = range(paddle1_pos - HALF_PAD_HEIGHT, paddle1_pos + HALF_PAD_HEIGHT)
    paddle2Range = range(paddle2_pos - HALF_PAD_HEIGHT, paddle2_pos + HALF_PAD_HEIGHT)
 
    # update paddle's vertical position, keep paddle on the screen
        
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    # draw paddles
    c.draw_line ((HALF_PAD_WIDTH, paddle1_pos - 
                  HALF_PAD_HEIGHT), (HALF_PAD_WIDTH, paddle1_pos +
                                     HALF_PAD_HEIGHT), PAD_WIDTH,
                 'white')
    c.draw_line ((WIDTH - HALF_PAD_WIDTH, paddle2_pos -
                  HALF_PAD_HEIGHT), (WIDTH - HALF_PAD_WIDTH,
                                     paddle2_pos + HALF_PAD_HEIGHT), 
                 PAD_WIDTH, 'white')
    
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # Reflects off ceiling and floor
    if ball_pos[1] + BALL_RADIUS == HEIGHT:
        ball_vel[1] -= ball_vel[1] * 2
    elif ball_pos[1] - BALL_RADIUS == 0:
        ball_vel[1] -= ball_vel[1] * 2
    
    # Resets/reflects off gutter
    if ball_pos[1] in paddle1Range:
        if ball_pos[0] - BALL_RADIUS <= PAD_WIDTH:
            ball_vel[0] *= -1.1
    elif ball_pos[1] in paddle2Range:
        if ball_pos[0] + BALL_RADIUS >= WIDTH - PAD_WIDTH:
            ball_vel[0] *=-1.1
    elif ball_pos[0] - BALL_RADIUS <= PAD_WIDTH:
        score2 += 1
        ball_init(True)
    elif ball_pos[0] + BALL_RADIUS >= WIDTH - PAD_WIDTH:
        score1 += 1
        ball_init(False)
            
    # draw ball and scores
    c.draw_circle((ball_pos), BALL_RADIUS, 1, 'WHITE', 'WHITE')
    c.draw_text(str(score1), (150, 100), 60, 'white')
    c.draw_text(str(score2), (450, 100), 60, 'white')
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['up']:
        timerUp.start()
    elif key == simplegui.KEY_MAP['down']:
        timerDown.start()
    elif key == simplegui.KEY_MAP['w']:
        timerW.start()
    elif key == simplegui.KEY_MAP['s']:
        timerS.start()
    
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP ['up']:
        timerUp.stop()
    elif key == simplegui.KEY_MAP ['down']:
        timerDown.stop()
    elif key == simplegui.KEY_MAP ['w']:
        timerW.stop()
    elif key == simplegui.KEY_MAP ['s']:
        timerS.stop()
    
def up():
    global paddle2_pos
    if paddle2_pos - HALF_PAD_HEIGHT >= 0:
        paddle2_pos -= paddle2_vel
    
def down():
    global paddle2_pos
    if paddle2_pos + HALF_PAD_HEIGHT <= HEIGHT:
        paddle2_pos += paddle2_vel

def w():
    global paddle1_pos
    if paddle1_pos - HALF_PAD_HEIGHT >= 0:
        paddle1_pos -= paddle1_vel

def s():
    global paddle1_pos
    if paddle1_pos + HALF_PAD_HEIGHT <= HEIGHT:
        paddle1_pos += paddle1_vel
        
def restart():
    global score1, score2
    score1 = 0
    score2 = 0
    ball_init(True)

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
timerUp = simplegui.create_timer (10, up)
timerDown = simplegui.create_timer (10, down)
timerW = simplegui.create_timer (10, w)
timerS = simplegui.create_timer (10, s)
frame.add_button('restart', restart, 100)

new_game()

# start frame
frame.start()
