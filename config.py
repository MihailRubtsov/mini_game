# Конфигурация игры

# --- Размеры и сетка ---
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 960
TILE_SIZE = 24 # Каждый блок - 48x48 пикселей

# --- Физика ---
GRAVITY = 0.5
JUMP_FORCE = -9
PLAYER_SPEED = 4
FALL_TERMINAL_VELOCITY = 10 # Максимальная скорость падения

# --- Логика игры ---
KEY_TO_WIN = 3
FOG_RADIUS = 2000 # Радиус видимости вокруг игрока

# --- Цвета (для временных плейсхолдеров) ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 150, 0)
RED = (200, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 200)
GREY = (50, 50, 50)
LIGHT_GREY = (150, 150, 150)

ASSET_PATHS = {
    'player': 'assets/graphics/air.png', # Используем air.png как плейсхолдер игрока
    'wall': 'assets/graphics/wall.png',
    'platform': 'assets/graphics/air.png', # Используем air.png
    'spike': 'assets/graphics/sss.png',
    'key': 'assets/graphics/keeey.png',
    'door_closed': 'assets/graphics/door.png',
    'door_open': 'assets/graphics/air.png', # Нужно будет создать open_door.png
    'background': 'assets/graphics/wall.png', # Используем wall как временный фон
}