import pygame
import sys
import random

# Импорт конфигурации, данных уровня и классов спрайтов
from config import *
from level_data import LEVEL_1, TILE_MAP, LEVEL_2, LEVEL_3, LEVEL_4
from sprites import Player, Key, Spike, Tile, Door

# --- Инициализация Pygame ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Квест-платформер 'Поиск Ключей'")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 40)

# --- Группы спрайтов ---
all_sprites = pygame.sprite.Group()
solid_tiles = pygame.sprite.Group() # Только Wall и Platform
keys_group = pygame.sprite.Group()
spike_group = pygame.sprite.Group()
door_group = pygame.sprite.Group()

# --- Переменные игры ---
GAME_STATE = "START" # START, PLAYING, CONGRATULATIONS
player = None
spawn_point = (0, 0)
available_spawn_points = [] # Список пустых координат для спауна ключей

# --- Функции игрового процесса ---

def load_level(level):
    """Парсинг карты, создание тайлов, шипов, двери и игрока."""
    global player, spawn_point, available_spawn_points
    
    # Очистка групп для перезагрузки или начала
    all_sprites.empty()
    solid_tiles.empty()
    keys_group.empty()
    spike_group.empty()
    door_group.empty()
    available_spawn_points = []
    
    # Проход по карте (тайл за тайлом)
    for row_index, row in enumerate(level):
        for col_index, char in enumerate(row):
            x = col_index * TILE_SIZE
            y = row_index * TILE_SIZE
            
            tile_type_name = TILE_MAP.get(char, 'Air')

            if char == 'W':
                tile = Tile(x, y, 'Wall', GREEN)
                all_sprites.add(tile)
                solid_tiles.add(tile)
            
            elif char == 'P':
                tile = Tile(x, y, 'Platform', LIGHT_GREY)
                all_sprites.add(tile)
                solid_tiles.add(tile)
                
            elif char == 'S':
                spike = Spike(x, y)
                all_sprites.add(spike)
                spike_group.add(spike)
                
            elif char == 'D':
                door = Door(x, y)
                all_sprites.add(door)
                door_group.add(door)

            elif char == 'B':
                spawn_point = (x, y)
                # Игрок создается после цикла, чтобы убедиться, что spawn_point определен

            # Если это пустое место, добавляем его в список для спауна ключей
            if tile_type_name in ['Air', 'Spawn']:
                available_spawn_points.append((x, y))

    # Создание игрока на точке спауна
    player = Player(spawn_point[0] + TILE_SIZE // 4, spawn_point[1])
    all_sprites.add(player)


def random_key_spawn():
    """Случайное размещение ключей в пустых, доступных местах."""
    
    # Удаляем все старые ключи, если они есть
    for key in keys_group:
        key.kill()

    # Берем случайные точки для спауна
    spawn_coords = random.sample(available_spawn_points, KEY_TO_WIN)
    
    for x, y in spawn_coords:
        key = Key(x, y)
        all_sprites.add(key)
        keys_group.add(key)
    #  проверка на работу двери
    # for i in range(3):
    #     key = Key(72+i* 24, 900)
    #     all_sprites.add(key)
    #     keys_group.add(key)


def reset_level():
    """Сброс состояния игрока и ключей после попадания на шипы."""
    global player
    
    # Возврат игрока на точку B
    player.rect.topleft = (spawn_point[0] + TILE_SIZE // 4, spawn_point[1])
    player.x_vel = 0
    player.y_vel = 0
    player.keys_collected = 0
    
    # Случайный спаун ключей заново
    random_key_spawn()


def draw_fog_of_war():
    """Создание эффекта ограниченной видимости вокруг игрока."""
    # 1. Черный слой "тумана"
    fog_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fog_surface.fill(BLACK)
    
    # 2. Установка режима смешивания для "вырезания" круга
    # Этот режим позволяет "стереть" часть поверхности, делая ее прозрачной
    fog_surface.set_colorkey(WHITE) 
    
    # 3. Рисуем "окно света" (круг) белым цветом
    # Круг центрируется на игроке (относительно экрана)
    center_x = player.rect.centerx
    center_y = player.rect.centery
    
    pygame.draw.circle(fog_surface, WHITE, (center_x, center_y), FOG_RADIUS)
    
    # 4. Наложение тумана на основной экран
    screen.blit(fog_surface, (0, 0))


# --- Основные экраны ---

def draw_text(text, surface, pos, color=WHITE):
    """Вспомогательная функция для вывода текста."""
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect(center=pos)
    surface.blit(text_surface, rect)


def start_screen():
    """Начальный экран."""
    draw_text("Найди все ключи и открой дверь)", screen, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    draw_text("Соберите 3 желтых ключа, чтобы открыть дверь!", screen, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    draw_text("Нажмите любую клавишу для начала...", screen, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

def congratulations_screen():
    """Финальный экран (Открытка)."""
    screen.fill(RED) # Яркий праздничный фон
    
    # Центральное поздравление
    draw_text("ПОЗДРАВЛЯЮ!", screen, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100), YELLOW)
    
    # Ваше личное сообщение (можно заменить на загрузку картинки-открытки)
    final_message = "Ты нашла все ключи и открыла моё сердце! С Днем Рождения!"
    draw_text(final_message, screen, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), WHITE)
    draw_text("", screen, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50), WHITE)


# --- Главный цикл игры ---
load_level(LEVEL_4)
random_key_spawn()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Переход со стартового экрана
        if GAME_STATE == "START" and event.type == pygame.KEYDOWN:
            GAME_STATE = "PLAYING"

    screen.fill(GREY) # Фон

    if GAME_STATE == "START":
        start_screen()

    elif GAME_STATE == "PLAYING":
        keys = pygame.key.get_pressed()
        player.handle_input(keys)

        # 1. Обновление
        all_sprites.update()
        player.update_physics(solid_tiles) # Обновление физики игрока относительно тайлов
        
        # Обновление двери
        for door in door_group:
            door.update_visual(player.keys_collected)

        # 2. Проверка коллизий
        
        # Player <-> Key
        keys_collected_list = pygame.sprite.spritecollide(player, keys_group, False)
        for key in keys_collected_list:
            key.on_collide(player)

        # Player <-> Spike
        spike_hits = pygame.sprite.spritecollide(player, spike_group, False)
        if spike_hits:
            reset_level()
        
        # Player <-> Door
        door_hits = pygame.sprite.spritecollide(player, door_group, False)
        for door in door_hits:
            door.on_collide(player, sys.modules[__name__]) # Передача ссылки на главный модуль для смены GAME_STATE
        
        # 3. Рендеринг
        all_sprites.draw(screen)
        
        # Наложение тумана войны
        draw_fog_of_war()

        # Нарисовать UI (счетчик ключей)
        key_text = font.render(f"Ключей: {player.keys_collected} / {KEY_TO_WIN}", True, WHITE)
        screen.blit(key_text, (10, 10))

    elif GAME_STATE == "CONGRATULATIONS":
        congratulations_screen()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
