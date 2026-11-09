"""Stack: a simple block-stacking game for the BBC micro:bit LED display.

Press A to drop the moving row. Press B after game over to play again.
"""

import basic
import input
import led


WIDTH = 5
START_WIDTH = 3
START_DELAY = 400
MIN_DELAY = 90


def draw_game(rows, moving_x, moving_width):
    """Draw the newest four settled rows and the row currently moving."""
    basic.clear_screen()

    visible_rows = rows[-4:]
    for row_index in range(len(visible_rows)):
        y = 4 - row_index
        mask = visible_rows[len(visible_rows) - 1 - row_index]
        for x in range(WIDTH):
            if mask & (1 << x):
                led.plot(x, y)

    moving_y = 4 - len(visible_rows)
    for x in range(moving_x, moving_x + moving_width):
        led.plot(x, moving_y)


def wait_for_drop():
    """Wait for a fresh A-button press, so holding A won't drop twice."""
    while input.button_is_pressed(Button.A):
        basic.pause(20)
    while not input.button_is_pressed(Button.A):
        basic.pause(20)
    while input.button_is_pressed(Button.A):
        basic.pause(20)


def game_over(score):
    basic.show_icon(IconNames.NO)
    basic.pause(500)
    basic.show_string("SCORE")
    basic.show_number(score)
    basic.show_string("B")
    while not input.button_is_pressed(Button.B):
        basic.pause(20)
    while input.button_is_pressed(Button.B):
        basic.pause(20)


def play_game():
    rows = []  # Each settled row is stored as a five-bit mask.
    block_width = START_WIDTH
    moving_x = 0
    direction = 1
    button_was_pressed = False

    while True:
        draw_game(rows, moving_x, block_width)
        pressed = input.button_is_pressed(Button.A)

        if pressed and not button_was_pressed:
            # Keep only the part of the moving row that overlaps the tower.
            if rows:
                overlap = ((1 << block_width) - 1) << moving_x
                overlap &= rows[-1]
                if overlap == 0:
                    return len(rows)
                block_width = 0
                for x in range(WIDTH):
                    if overlap & (1 << x):
                        block_width += 1
                moving_x = 0
                while not (overlap & (1 << moving_x)):
                    moving_x += 1
                rows.append(overlap)
            else:
                rows.append(((1 << block_width) - 1) << moving_x)

            if block_width == 1:
                return len(rows)

        button_was_pressed = pressed

        max_x = WIDTH - block_width
        moving_x += direction
        if moving_x >= max_x:
            moving_x = max_x
            direction = -1
        elif moving_x <= 0:
            moving_x = 0
            direction = 1

        delay = max(MIN_DELAY, START_DELAY - len(rows) * 25)
        basic.pause(delay)


def wait_for_button_release(button):
    while input.button_is_pressed(button):
        basic.pause(20)


while True:
    score = play_game()
    game_over(score)
