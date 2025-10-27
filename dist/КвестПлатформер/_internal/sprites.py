import pygame
from config import *
from level_data import LEVEL_4
import os
import sys # Необходим для корректной работы




def load_and_scale(path, size_w, size_h=None):
    """Загружает изображение с правильным путём в PyInstaller."""
    if size_h is None:
        size_h = size_w

    # --- КЛЮЧЕВОЙ МОМЕНТ: Определяем правильный путь ---
    if getattr(sys, 'frozen', False):
        # Если запущено из PyInstaller (onefile или onedir)
        base_path = sys._MEIPASS
    else:
        # Если запущено как скрипт (python main.py)
        base_path = os.path.abspath(".")

    full_path = os.path.join(base_path, path)
    # -------------------------------------------

    try:
        image = pygame.image.load(full_path).convert_alpha()
        return pygame.transform.scale(image, (size_w, size_h))
    except pygame.error as e:
        print(f"Ошибка загрузки текстуры {full_path}: {e}. Используется плейсхолдер.")
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
    def __init__(self, x, y, tile_type, color=GREEN):
        super().__init__()
        self.type = tile_type
        
        # Загрузка временной поверхности (вместо load_and_scale)
        # self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        # self.image.fill(color)
        self.image = load_and_scale(ASSET_PATHS['wall'], TILE_SIZE, TILE_SIZE)
        
        # Для односторонних платформ делаем их тоньше и другого цвета
        if self.type == 'Platform':
            # self.image = pygame.Surface((TILE_SIZE, TILE_SIZE // 4))
            # self.image.fill(LIGHT_GREY)
            self.image = load_and_scale(ASSET_PATHS['platform'], TILE_SIZE, TILE_SIZE // 4)
            # Размещение в нижней части тайла, как односторонняя платформа
            self.rect = self.image.get_rect(topleft=(x, y + TILE_SIZE - TILE_SIZE // 4))
        else:
            self.rect = self.image.get_rect(topleft=(x, y))

# --- Класс Игрока ---
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = TILE_SIZE // 2
        self.height = TILE_SIZE
        
        # Визуальное представление (временное)
        self.image = load_and_scale(ASSET_PATHS['player'], self.width, self.height)
        self.rect = self.image.get_rect(topleft=(x, y))
        # self.image = pygame.Surface((self.width, self.height))
        # self.image.fill(BLUE)
        # self.rect = self.image.get_rect(topleft=(x, y))

        # Физика
        self.x_vel = 0
        self.y_vel = 0
        self.on_ground = False
        self.down_pressed = False # Флаг для спуска сквозь платформу (предотвращение многократного срабатывания)
        self.can_drop = False # Флаг, что игрок может провалиться через платформу

        # Состояние игры
        self.keys_collected = 0

    def handle_input(self, keys):
        # Горизонтальное движение
        self.x_vel = 0
        if keys[pygame.K_LEFT]:
            self.x_vel = -PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.x_vel = PLAYER_SPEED
        
        # Прыжок
        if keys[pygame.K_UP] and self.on_ground:
            self.y_vel = JUMP_FORCE
            self.on_ground = False

        # Спуск сквозь одностороннюю платформу
        if keys[pygame.K_DOWN]:
            # Разрешаем провалиться только один раз при первом нажатии и стоянии на земле
            if not self.down_pressed and self.on_ground:
                 self.can_drop = True 
            self.down_pressed = True
        else:
            self.down_pressed = False
            self.can_drop = False # Сбрасываем только когда кнопка отпущена

    def apply_gravity(self):
        # Применение гравитации и ограничение скорости падения
        self.y_vel += GRAVITY
        if self.y_vel > FALL_TERMINAL_VELOCITY:
            self.y_vel = FALL_TERMINAL_VELOCITY

    def update_physics(self, tile_list):
        self.apply_gravity()

        # 1. Горизонтальное движение и коллизия
        self.rect.x += self.x_vel
        self.collide_x(tile_list)

        # 2. Вертикальное движение и коллизия
        self.rect.y += self.y_vel
        self.on_ground = False # Сброс перед проверкой
        self.collide_y(tile_list)

    def collide_x(self, tiles):
        for tile in tiles:
            if tile.type in ['Wall']:
                if self.rect.colliderect(tile.rect):
                    if self.x_vel > 0: # Движение вправо
                        self.rect.right = tile.rect.left
                    elif self.x_vel < 0: # Движение влево
                        self.rect.left = tile.rect.right

    def collide_y(self, tiles):
        for tile in tiles:
            if tile.type in ['Wall']:
                if self.rect.colliderect(tile.rect):
                    if self.y_vel > 0: # Падение (удар об пол)
                        self.rect.bottom = tile.rect.top
                        self.y_vel = 0
                        self.on_ground = True
                    elif self.y_vel < 0: # Прыжок (удар об потолок)
                        self.rect.top = tile.rect.bottom
                        self.y_vel = 0
            
            # Логика односторонних платформ (P)
            elif tile.type == 'Platform':
                if self.rect.colliderect(tile.rect):
                    # Коллизия только при падении или стоянии
                    if self.y_vel >= 0: 
                        
                        # Если не нажата клавиша "Вниз" (т.е. хотим остановиться)
                        if not self.can_drop:
                            
                            # Проверяем, что игрок приземлился сверху.
                            # Если игрок падает (y_vel > 0) и сталкивается с верхней частью платформы, мы его останавливаем.
                            if self.rect.bottom > tile.rect.top:
                                self.rect.bottom = tile.rect.top
                                self.y_vel = 0
                                self.on_ground = True
                        
                        # ВНИМАНИЕ: Если can_drop == True, коллизия игнорируется, и игрок падает. 
                        # can_drop сбрасывается в handle_input, когда отпускают кнопку.
                        # ВАЖНО: Мы убрали сброс can_drop = False отсюда.


# --- Класс Ключа ---
class Key(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # self.image = pygame.Surface((TILE_SIZE // 2, TILE_SIZE // 2))
        # self.image.fill(YELLOW) # Желтый цвет для ключа
        # self.rect = self.image.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))
        size = TILE_SIZE // 2
        self.image = load_and_scale(ASSET_PATHS['key'], size)
        self.rect = self.image.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))

    def on_collide(self, player):
        player.keys_collected += 1
        self.kill() # Удалить ключ из всех групп

# --- Класс Шипов ---
class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # self.image = pygame.Surface((TILE_SIZE, TILE_SIZE // 3))
        # self.image.fill(RED) # Красный цвет для шипов
        # # Размещение на нижней границе тайла
        # self.rect = self.image.get_rect(topleft=(x, y + TILE_SIZE - TILE_SIZE // 3))
        height = TILE_SIZE // 3
        self.image = load_and_scale(ASSET_PATHS['spike'], TILE_SIZE, height)
        self.rect = self.image.get_rect(topleft=(x, y + TILE_SIZE - height))

    def on_collide(self, game_state_manager):
        # Вызов функции сброса уровня
        game_state_manager.reset_level() 

# --- Класс Двери (Выход) ---
# class Door(pygame.sprite.Sprite):
#     def __init__(self, x, y):
#         super().__init__()
#         self.image = pygame.Surface((TILE_SIZE, TILE_SIZE * 2)) # Дверь выше игрока
#         self.image.fill(BLUE) # Изначально синяя (закрытая)
#         self.rect = self.image.get_rect(topleft=(x, y - TILE_SIZE)) # Размещаем над уровнем пола

#     def update_visual(self, keys_collected):
#         # Визуальное изменение двери, если все ключи собраны
#         if keys_collected >= KEY_TO_WIN:
#             self.image.fill(GREEN) # Зеленый цвет (открытая)

#     def on_collide(self, player, game_state_manager):
#         if player.keys_collected >= KEY_TO_WIN:
#             game_state_manager.GAME_STATE = "CONGRATULATIONS" # Переключение на финальный экран


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
