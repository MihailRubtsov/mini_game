# Конфигурация игры

# Размеры 
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 960
TILE_SIZE = 24 # Каждый блок - 48x48 пикселей

#  Физика 
GRAVITY = 0.5
JUMP_FORCE = -8
PLAYER_SPEED = 4
FALL_TERMINAL_VELOCITY = 10 # Максимальная скорость падения

#  Логика игры
KEY_TO_WIN = 3
FOG_RADIUS = 100 # Радиус видимости вокруг игрока

# Цвета 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 150, 0)
RED = (200, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 200)
GREY = (50, 50, 50)
LIGHT_GREY = (150, 150, 150)

ASSET_PATHS = {
    'player': 'player.png',
    'wall': 'wall.png',
    'platform': 'plat.png', 
    'spike': 'sss.png',
    'key': 'keeey.png',
    'door_closed': 'door.png',
    'door_open': 'door.png', 
    'background': 'wall.png', 
}