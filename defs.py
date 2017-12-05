import pygame
import levels


def set_state(s):
	global state, skip_ticks
	pygame.mouse.set_visible(True)
	state = s
	if s in ["playing", "lcom"]:
		pygame.mouse.set_visible(False)
	if s in ["lcom", 'won']:
		skip_ticks = 3
		levels.level += 1
	return state


def set_ball():
	global ball, pad, ball_sprites
	ball = {'ball': ball_sprites[2], 'in_motion': False, 'dx': 0, 'dy': 0, 'fdx': 0, 'fx': 0}
	ball['rect'] = pygame.Rect(pad['rect'].centerx, pad['rect'].y - ball['ball'].get_height() - 2, ball['ball'].get_width(), ball['ball'].get_height())
	return ball


def init_game():
	global lives, skip_ticks, pad, ball, bricks
	lives = 3
	levels.level = 1
	skip_ticks = 0
	levels.set_levels(screen.get_width(), brick_width, brick_height, brick_sprites, pygame)

	pad = {'pad': pad_sprites[2][1]}
	pad['rect'] = pygame.Rect(screen.get_width() / 2 - pad['pad'].get_width(), screen.get_height() - 50, pad['pad'].get_width(), pad['pad'].get_height())

	ball = set_ball()
	bricks = levels.levels[levels.level]

	return lives, skip_ticks, pad, ball, bricks


lives = skip_tricks = pad = ball = bricks = state = 0
screen = pygame.display.set_mode((800, 450))
clock = pygame.time.Clock()
fps = 60
state = set_state("playing")
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 30, 30)
mousex = 0
mousey = 0

# Set Menu Texts
pygame.font.init()
font_hel40 = pygame.font.SysFont('Helvetica', 40)
font_hel24 = pygame.font.SysFont('Helvetica', 24)

paused_text = "Paused"
paused_size = font_hel40.size(paused_text)
paused_text = font_hel40.render(paused_text, True, white).convert_alpha()
paused_rect = pygame.Rect((screen.get_width() / 2 - paused_size[0] / 2, 90), paused_size)

menu_head_string = "Main Menu"
menu_head_size = font_hel40.size(menu_head_string)
menu_head_text = font_hel40.render(menu_head_string, True, white).convert_alpha()
menu_head_rect = pygame.Rect((screen.get_width() / 2 - menu_head_size[0] / 2, 90), menu_head_size)

menu_start_string = "Start Game"
menu_start_size = font_hel24.size(menu_start_string)
menu_start_text = font_hel24.render(menu_start_string, True, white).convert_alpha()
menu_start_text_hl = font_hel24.render(menu_start_string, True, red).convert_alpha()
menu_start_rect = menu_head_rect.move(0, menu_head_rect.h + 10)
menu_start_rect.size = menu_start_size
menu_start_rect.centerx = menu_head_rect.centerx

menu_exit_string = "Quit"
menu_exit_size = font_hel24.size(menu_exit_string)
menu_exit_text = font_hel24.render(menu_exit_string, True, white).convert_alpha()
menu_exit_text_hl = font_hel24.render(menu_exit_string, True, red).convert_alpha()
menu_exit_rect = menu_start_rect.move(0, menu_start_rect.h + 10)
menu_exit_rect.size = menu_exit_size
menu_exit_rect.centerx = menu_head_rect.centerx

gameover_string = "Game Over"
gameover_size = font_hel40.size(gameover_string)
gameover_text = font_hel40.render(gameover_string, True, white).convert_alpha()
gameover_rect = pygame.Rect((screen.get_width() / 2 - gameover_size[0] / 2, 90), gameover_size)

over_again_string = "Try again"
over_again_size = font_hel24.size(over_again_string)
over_again_text = font_hel24.render(over_again_string, True, white).convert_alpha()
over_again_text_hl = font_hel24.render(over_again_string, True, red).convert_alpha()
over_again_rect = gameover_rect.move(0, gameover_rect.h + 10)
over_again_rect.size = over_again_size
over_again_rect.centerx = gameover_rect.centerx

over_menu_string = "Main Menu"
over_menu_size = font_hel24.size(over_menu_string)
over_menu_text = font_hel24.render(over_menu_string, True, white).convert_alpha()
over_menu_text_hl = font_hel24.render(over_menu_string, True, red).convert_alpha()
over_menu_rect = over_again_rect.move(0, over_again_rect.h + 10)
over_menu_rect.size = over_menu_size
over_menu_rect.centerx = gameover_rect.centerx

won_head_string = "You Won"
won_head_size = font_hel40.size(won_head_string)
won_head_text = font_hel40.render(won_head_string, True, white).convert_alpha()
won_head_rect = pygame.Rect((screen.get_width() / 2 - won_head_size[0] / 2, 90), won_head_size)

# Set images
heart = pygame.transform.scale(pygame.image.load('heart.png').convert_alpha(), (16, 16))

sprite_sheet = pygame.image.load('breakout.png').convert_alpha()
sprite_block = 8
brick_width = sprite_block * 4
brick_height = sprite_block * 2

# Set brick sprites
brick_sprites = []
for i in range(21):
	x = (brick_width * i) % 192
	y = (brick_width * i) // 192 * brick_height
	brick_sprites.append(sprite_sheet.subsurface(x, y, brick_width, brick_height))

# Set ball sprites
ball_sprites = []
for i in range(7):
	x = (3 * brick_width + sprite_block * i) if i < 4 else (3 * brick_width + sprite_block * (i - 4))
	y = brick_height * 3 + (sprite_block if i > 3 else 0)
	ball_sprites.append(sprite_sheet.subsurface(x, y, sprite_block, sprite_block))

# Set pad sprites, pad_sprite[size][color]
pad_sprites = [[0] * 4 for i in range(4)]
temp = 0
for size in range(4):
	width = sprite_block * 4 * (size + 1)
	for color in range(4):
		x = temp % 192
		y = brick_height * (4 + 2 * color) + (temp // 192) * brick_height
		pad_sprites[size][color] = sprite_sheet.subsurface(x, y, width, brick_height)
	temp += width

init_game()

dark_screen = pygame.Surface((screen.get_width(), screen.get_height()))
dark_screen.set_alpha(150)
dark_screen.fill((0, 0, 0))


def darken_screen():
	screen.blit(dark_screen, (0, 0))
