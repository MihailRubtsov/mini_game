import pygame
from config import *
from level_data import LEVEL_4 # Необходим для корректной работы

# --- ВСПОМОГАТЕЛЬНАЯ ФУНКЦИЯ ДЛЯ ЗАГРУЗКИ ТЕКСТУР ---
def load_and_scale(path, size_w, size_h=None):
    """Загружает изображение и масштабирует его до нужного размера."""
    if size_h is None:
        size_h = size_w
        
    try:
        # Загрузка с прозрачностью и масштабирование
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, (size_w, size_h))
    except pygame.error as e:
        print(f"Ошибка загрузки текстуры {path}: {e}. Используется плейсхолдер.")
        
        # Создание цветного плейсхолдера, если файл не найден
        surf = pygame.Surface((size_w, size_h))
        if 'player' in path: surf.fill(BLUE)
        elif 'spike' in path: surf.fill(RED)
        elif 'key' in path: surf.fill(YELLOW)
        elif 'wall' in path: surf.fill(GREEN)
        elif 'door' in path: surf.fill(LIGHT_GREY)
        else: surf.fill(BLACK)
        return surf


# --- Базовый класс для всех статических тайлов ---
class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_type): # Удален color=GREEN
        super().__init__()
        self.type = tile_type
        
        # --- ЗАМЕНА НА ТЕКСТУРЫ ---
        if self.type == 'Platform':
            # Платформа тоньше, поэтому загружаем с размером 24x6 (TILE_SIZE // 4)
            self.image = load_and_scale(ASSET_PATHS['platform'], TILE_SIZE, TILE_SIZE // 4)
            self.rect = self.image.get_rect(topleft=(x, y + TILE_SIZE - TILE_SIZE // 4))
        
        else: # Wall
            self.image = load_and_scale(ASSET_PATHS['wall'], TILE_SIZE)
            self.rect = self.image.get_rect(topleft=(x, y))

# --- Класс Игрока ---
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = TILE_SIZE // 2
        self.height = TILE_SIZE
        
        # --- ЗАМЕНА НА ТЕКСТУРУ ---
        self.image = load_and_scale(ASSET_PATHS['player'], self.width, self.height)
        self.rect = self.image.get_rect(topleft=(x, y))
        # ... (остальной код Player без изменений) ...

    def handle_input(self, keys):
        # ... (логика handle_input без изменений) ...

    def apply_gravity(self):
        # ... (логика apply_gravity без изменений) ...

    def update_physics(self, tile_list):
        # ... (логика update_physics без изменений) ...

    def collide_x(self, tiles):
        # ... (логика collide_x без изменений) ...

    def collide_y(self, tiles):
        # ... (логика collide_y без изменений) ...


# --- Класс Ключа ---
class Key(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # --- ЗАМЕНА НА ТЕКСТУРУ ---
        size = TILE_SIZE // 2
        self.image = load_and_scale(ASSET_PATHS['key'], size)
        self.rect = self.image.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))

    def on_collide(self, player):
        player.keys_collected += 1
        self.kill() 

# --- Класс Шипов ---
class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # --- ЗАМЕНА НА ТЕКСТУРУ ---
        height = TILE_SIZE // 3
        self.image = load_and_scale(ASSET_PATHS['spike'], TILE_SIZE, height)
        self.rect = self.image.get_rect(topleft=(x, y + TILE_SIZE - height))

    def on_collide(self, game_state_manager):
        game_state_manager.reset_level() 

# --- Класс Двери (Выход) ---
class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Дверь должна быть высотой 2 тайла
        door_height = TILE_SIZE * 2
        
        # --- ЗАГРУЗКА ДВУХ ТЕКСТУР ---
        self.image_closed = load_and_scale(ASSET_PATHS['door_closed'], TILE_SIZE, door_height)
        self.image_open = load_and_scale(ASSET_PATHS['door_open'], TILE_SIZE, door_height)
        
        self.image = self.image_closed # Изначально закрытая
        self.rect = self.image.get_rect(topleft=(x, y - TILE_SIZE)) # Размещаем над уровнем пола

    def update_visual(self, keys_collected):
        if keys_collected >= KEY_TO_WIN:
            self.image = self.image_open # Зеленый цвет (открытая)
        else:
            self.image = self.image_closed

    def on_collide(self, player, game_state_manager):
        if player.keys_collected >= KEY_TO_WIN:
            game_state_manager.GAME_STATE = "CONGRATULATIONS"