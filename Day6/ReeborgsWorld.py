# hurdle

def turn_right():
    turn_left()
    turn_left()
    turn_left()

def jump():
    go = 0
    turn_left()
    move()
    if right_is_clear() == True:
        turn_right()
        move()
        turn_right()
        move()
        turn_left()
    else:
        while right_is_clear() != True:
            go = go + 1
            move()
            if right_is_clear() == True:
                turn_right()
                move()
                turn_right()
                while go >= 0:
                    move()
                    go = go - 1
                turn_left()
                break
while at_goal() != True:
    if front_is_clear() == True:
        move()
    elif wall_in_front() == True:
        jump()