import random

from defs import *


# Game Lopp
running = True
try:  # usama LEVELS, POWER-UPS
	while running:
		clock.tick(fps if state == 'playing' else 10)  # Limit fps
		if not skip_ticks == 0:
			skip_ticks -= 1
			continue
		if state == 'lcom':
			try:
				bricks = levels.levels[levels.level]
			except IndexError:
				state = set_state('won')
				skip_ticks = 30
			if state == 'lcom':
				ball['rect'] = pygame.Rect(pad['rect'].centerx, pad['rect'].y - ball['ball'].get_height() - 2, ball['ball'].get_width(), ball['ball'].get_height())
				ball['in_motion'] = False
				state = set_state('playing')
		elif state == 'won':
			state = set_state('menu')
			lives, skip_ticks, pad, ball, bricks = init_game()
		for event in pygame.event.get():
			if event.type == pygame.MOUSEMOTION:  # Mouse Motion Events
				mousex = event.pos[0]
				mousey = event.pos[1]
				if state == 'playing':
					# Move pad
					x = mousex
					if x + pad['rect'].w / 2 > screen.get_width():
						x = screen.get_width() - pad['rect'].w / 2
					if x < pad['rect'].w / 2:
						x = pad['rect'].w / 2
					pad['rect'].centerx = x

					# Move ball with pad if not in motion
					if not ball['in_motion']:
						ball['rect'].x = pad['rect'].centerx
			elif event.type == pygame.MOUSEBUTTONUP:  # Mouse Button Events
				if event.button == 3:  # Pause game on right click
					if state == 'paused':
						state = set_state('playing')
					elif state == 'playing':
						state = set_state('paused')
				elif event.button == 1:
					if state == 'playing' and not ball['in_motion']:  # Start ball on left click
						ball['in_motion'] = True
						ball['dy'] = -4
						ball['dx'] = 0 if random.randint(1, 2) == 1 else -2  # Fix
					elif state == 'paused':
						state = set_state('playing')
					elif state == 'menu':  # Button clicks
						if menu_start_rect.collidepoint(mousex, mousey):
							state = set_state('playing')
						if menu_exit_rect.collidepoint(mousex, mousey):
							running = False
					elif state == 'over':
						if over_again_rect.collidepoint(mousex, mousey):
							init_game()
							state = set_state('playing')
						if over_menu_rect.collidepoint(mousex, mousey): state = set_state('menu')
			elif event.type == pygame.KEYDOWN:  # Keyboard Events
				if bool(event.mod & pygame.KMOD_ALT) and event.key == pygame.K_F4:
					running = False
				if event.key == pygame.K_1:  # Cheat
					bricks[0] = [bricks[0][0]]
			elif event.type == pygame.QUIT:
				running = False

		# State dependant rendering
		screen.fill(0x000000)  # Clear screen
		if state in ['paused', 'over', 'playing', 'won']:
			screen.blit(pad['pad'], pad['rect'])
			screen.blit(ball['ball'], ball['rect'])
			for brick, sprite in zip(bricks[0], bricks[1]):
				screen.blit(sprite, brick)
			for i in range(lives):
				screen.blit(heart, (10 + i * (heart.get_width() + 10), 10))
		if state == 'paused':
			darken_screen()
			screen.blit(paused_text, paused_rect)
		elif state == 'over':
			darken_screen()
			screen.blit(gameover_text, gameover_rect)
			screen.blit(over_again_text_hl if over_again_rect.collidepoint(mousex, mousey) else over_again_text, over_again_rect)
			screen.blit(over_menu_text_hl if over_menu_rect.collidepoint(mousex, mousey) else over_menu_text, over_menu_rect)
		elif state == 'menu':
			screen.blit(menu_head_text, menu_head_rect)
			screen.blit(menu_start_text_hl if menu_start_rect.collidepoint(mousex, mousey) else menu_start_text, menu_start_rect)
			screen.blit(menu_exit_text_hl if menu_exit_rect.collidepoint(mousex, mousey) else menu_exit_text, menu_exit_rect)
		elif state == 'won':
			darken_screen()
			screen.blit(won_head_text, won_head_rect)

		# Update ball
		if ball['in_motion'] and state == 'playing':
			dx = ball['dx']
			dy = ball['dy']
			fx = ball['fx']
			fdx = ball['fdx']
			rect = ball['rect']

			# Fine movement
			fx += fdx
			if fx >= 1:
				rect = rect.move(1, 0)
				fx -= 1
			elif fx <= 1:
				rect = rect.move(-1, 0)
				fx += 1

			# Boundaries
			if (rect.right >= screen.get_width() - 5 and dx > 0) or (rect.x <= 0 and dx < 0):
				dx = -dx
				fdx = -fdx
			if rect.y < 0 and dy < 0:
				dy = -dy
			if rect.y + rect.h > screen.get_height() + 300:
				lives -= 1
				if lives < 0:
					state = set_state('over')
				ball = set_ball()
				rect = ball['rect']

			# Collision
			collision = rect.collidelist(bricks[0])
			if not collision == -1:
				brick = bricks[0][collision]
				below_top = rect.centery > brick.top
				above_bottom = rect.centery < brick.bottom
				if below_top and dy < 0:
					dy = -dy
				elif below_top and dy > 0:
					dx = -dx
					fdx = -fdx
				elif above_bottom and dy < 0:
					dx = -dx
					fdx = -fdx
				elif above_bottom and dy > 0:
					dy = -dy
				bricks[0].pop(collision)

			if len(bricks[0]) == 0:
				state = set_state('lcom')

			# Bounce
			collision = rect.colliderect(pad['rect'])
			if collision and dy > 0:
				diff = (rect.centerx - pad['rect'].centerx) / 10
				fdx = diff % 1 if diff >= 0 else (-diff % 1) * -1
				dx = int(diff)
				dy = -dy

			ball['rect'] = rect.move(dx, dy)
			ball['dx'] = dx
			ball['dy'] = dy
			ball['fx'] = fx
			ball['fdx'] = fdx

		pygame.display.flip()  # Display next frame
finally:
	pygame.quit()
