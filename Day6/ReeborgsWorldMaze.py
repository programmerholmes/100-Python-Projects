def turn_right():
    turn_left()
    turn_left()
    turn_left()


while at_goal() != True:
    if front_is_clear() == True and right_is_clear() == True:
        if is_facing_north() == True:
            turn_right()
            move()

while at_goal() != True:
    if front_is_clear() == True and right_is_clear() == True:
        if is_facing_north() == True:
            turn_right()
            move()
            break
    if front_is_clear() == True:
        move()
    elif front_is_clear() != True and wall_on_right() == True:
        turn_left()
    elif front_is_clear() != True:
        turn_right()
    else:
        move()
    if front_is_clear() != True and right_is_clear() == True:
        turn_right()
        move()
        if wall_on_right() != True:
            turn_right()
        else:
            if front_is_clear() != True and wall_on_right() == True:
                turn_left()
                move()
    if front_is_clear() == True and right_is_clear() == True:
        move()

            break
    if front_is_clear() == True:
        move()
    elif front_is_clear() != True and wall_on_right() == True:
        turn_left()
    elif front_is_clear() != True:
        turn_right()
    else:
        move()
    if front_is_clear() != True and right_is_clear() == True:
        turn_right()
        move()
        if wall_on_right() != True:
            turn_right()
        else:
            if front_is_clear() != True and wall_on_right() == True:
                turn_left()
                move()
    if front_is_clear() == True and right_is_clear() == True:
        move()
