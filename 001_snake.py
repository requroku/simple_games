''' Simple Snake Game '''

import random
import curses


# prints Game Over screen
def game_over():
	text = ['██╗░░░██╗░█████╗░██╗░░░██╗  ██╗░░░░░░█████╗░░██████╗██████╗ ',
			'╚██╗░██╔╝██╔══██╗██║░░░██║  ██║░░░░░██╔══██╗██╔════╝██╔═══╝ ',
			'░╚████╔╝░██║░░██║██║░░░██║  ██║░░░░░██║░░██║╚█████╗░█████╗░ ',
			'░░╚██╔╝░░██║░░██║██║░░░██║  ██║░░░░░██║░░██║░╚═══██╗██╔══╝░ ',
			'░░░██║░░░╚█████╔╝╚██████╔╝  ███████╗╚█████╔╝██████╔╝██████╗ ',
			'░░░╚═╝░░░░╚════╝░░╚═════╝░  ╚══════╝░╚════╝░╚═════╝░╚═════╝ ',
			' '*60,
			' '*19 + 'Press Enter to exit...' + ' '*19,
			' '*60,
			' '*60]

	# max box height
	by = len(text)
	# max box width
	bx = len(text[0])

	w.clear()
	w.refresh()
	pad = curses.newpad(by, bx)
	# These loops fill the pad with letters
	for y in range(0, by-1):
	    for x in range(0, bx-1):
	        pad.addch(y, x, text[y][x])

	# Displays a section of the pad in the middle of the screen.
	# (0,0) 		: coordinate of upper-left corner of pad area to display.
	# (sh//4,sw//4) : coordinate of upper-left corner of window area to be filled
	#         		  with pad content.
	# (20, 110) 	: coordinate of lower-right corner of window area to be
	#          		: filled with pad content.
	pad.refresh(0,0, sh//4,sw//4, 20,110)


def game_start():
	# snake initial position
	snk_x = sw // 4
	snk_y = sh // 2

	# snake body parts
	snake = [
		[snk_y, snk_x],
		[snk_y, snk_x-1],
		[snk_y, snk_x-2]
	]

	# starting position of the food
	food = [sh // 2, sw // 2]

	# add food to the screen
	w.addch(food[0], food[1], curses.ACS_PI)

	# initial snake direction to go
	key = curses.KEY_RIGHT

	# infinite loop for every snake move
	while True:
		# get the next pressed key
		next_key = w.getch()

		# do not allow snake to go inside itself
		if (key == curses.KEY_DOWN) and (next_key == curses.KEY_UP) \
		or (key == curses.KEY_UP) and (next_key == curses.KEY_DOWN) \
		or (key == curses.KEY_LEFT) and (next_key == curses.KEY_RIGHT) \
		or (key == curses.KEY_RIGHT) and (next_key == curses.KEY_LEFT) \
		or next_key == -1:
			pass
		else:
			key = next_key


		# check if we lost the game
		# if the y position either at the top or at the height of the screen
		# or the x position is either to the left or at the width of the screen
		# or the snake is in itself
		if snake[0][0] in [0, sh-1] or snake[0][1] in [0, sw-1] \
		or snake[0] in snake[1:]:
			game_over()
			curses.noecho()
			w.getstr()
			curses.endwin()
			quit()

		# determine the new head of the snake
		new_head = [snake[0][0], snake[0][1]]

		if key == curses.KEY_DOWN:
			new_head[0] += 1
		if key == curses.KEY_UP:
			new_head[0] -= 1
		if key == curses.KEY_LEFT:
			new_head[1] -= 1
		if key == curses.KEY_RIGHT:
			new_head[1] += 1

		# insert the new head of our snake
		snake.insert(0, new_head)

		if snake[0] == food:
			food = None
			while food is None:
				# new food location
				nf = [
					random.randint(1, sh-1),
					random.randint(1, sw-1),
				]
				# redo if food spawn in snake
				food = nf if nf not in snake else None
			# add to the screen
			w.addch(food[0], food[1], curses.ACS_PI)
		else:
			tail = snake.pop()
			w.addch(tail[0], tail[1], ' ')
		
		w.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)


# initialize the screen
s = curses.initscr()
# set cursor to 0, so it doesnt shown on the screen
curses.curs_set(0)
# get the height and width of the screen
sh, sw = s.getmaxyx()
# new window
w = curses.newwin(sh, sw, 0, 0)
#accept keypad input
w.keypad(1)
# refresh the screen every 100 ms
w.timeout(1)


if __name__ == "__main__":
	game_start()
