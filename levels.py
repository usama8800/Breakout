level = 1
levels = [None]


def set_levels(screen_width, brick_width, brick_height, brick_sprites, pygame):
	global levels
	levels = [None]
	# @formatter:of
	# for j in range(3):
	# 	rects = []
	# 	sprites = []
	# 	rows = 1
	# 	cols = 1
	# 	start = (screen_width - cols * brick_width) / 2
	# 	for i in range(rows):
	# 		for j in range(cols):
	# 			x = start + j * brick_width
	# 			y = 50 + i * brick_height
	# 			rects.append(pygame.Rect(x, y, brick_width, brick_height))
	# 			sprites.append(brick_sprites[0])
	# 	levels.append([rects, sprites])
	# @formatter:on

	rects = []
	sprites = []
	rows = 5
	cols = 22
	start = (screen_width - cols * brick_width) / 2
	for i in range(rows):
		for j in range(cols):
			x = start + j * brick_width
			y = 50 + i * brick_height
			rects.append(pygame.Rect(x, y, brick_width, brick_height))
			sprites.append(brick_sprites[0])
	levels.append([rects, sprites])
