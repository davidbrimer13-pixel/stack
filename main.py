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


def count_rows(rows):
    """Count settled rows without relying on len()."""
    count = 0
    for row in rows:
        count += 1
    return count


def draw_game(rows, moving_x, moving_width):
    """Draw the newest four settled rows and the row currently moving."""
    basic.clear_screen()

    row_count = count_rows(rows)
    first_visible = row_count - 4
    if first_visible < 0:
        first_visible = 0

    row_index = 0
    for mask in rows:
        if row_index >= first_visible:
            y = 4 - (row_index - first_visible)
            for x in range(WIDTH):
                if mask & (1 << x):
                    led.plot(x, y)
        row_index += 1

    visible_count = row_count - first_visible
    moving_y = 4 - visible_count
    for x in range(moving_x, moving_x + moving_width):
        led.plot(x, moving_y)


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
                    return count_rows(rows)
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
                return count_rows(rows)

        button_was_pressed = pressed

        max_x = WIDTH - block_width
        moving_x += direction
        if moving_x >= max_x:
            moving_x = max_x
            direction = -1
        elif moving_x <= 0:
            moving_x = 0
            direction = 1

        row_count = count_rows(rows)
        delay = START_DELAY - row_count * 25
        if delay < MIN_DELAY:
            delay = MIN_DELAY
        basic.pause(delay)


while True:
    score = play_game()
    game_over(score)
