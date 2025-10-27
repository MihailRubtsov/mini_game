import pygame
import sys
import random

# Импорт конфигурации, данных уровня и классов спрайтов
from config import *
from level_data import TILE_MAP,  LEVEL_4
# ОБЯЗАТЕЛЬНО: Импортируем load_and_scale, чтобы использовать ее для фона
from sprites import Player, Key, Spike, Tile, Door, load_and_scale 

# --- Инициализация Pygame ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Квест-платформер 'Поиск Ключей'")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 40)

# --- ЗАГРУЗКА ФОНА ---
# Загружаем фон, используя функцию из sprites.py. Если air.png не найден, будет черный плейсхолдер.

BACKGROUND_IMAGE = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
BACKGROUND_IMAGE.fill(GREY) # Резервный фон
    

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


HELP_TEXT = [
    "--- ПРАВИЛА ИГРЫ (Нажмите H или ESC для выхода) ---",
    "",
    "1) Чтобы двигаться, используй стрелочки (Влево/Вправо).",
    "2) Для прыжка используй стрелочку Вверх.",
    "3) Доски ('P') - это ступеньки, с помощью них можно спускаться (стрелочка Вниз).",
    "4) Лава (шипы) убивает. Будь осторожен!",
    "5) Собери все ключи, чтобы открыть дверь и перейти на следующий уровень."
]

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

            # --- ИЗМЕНЕНИЕ: УДАЛЯЕМ АРГУМЕНТЫ ЦВЕТА ИЗ Tile() ---
            if char == 'W':
                tile = Tile(x, y, 'Wall') # Теперь цвет берется из текстуры в sprites.py
                all_sprites.add(tile)
                solid_tiles.add(tile)
            
            elif char == 'P':
                tile = Tile(x, y, 'Platform') # Теперь цвет берется из текстуры в sprites.py
                all_sprites.add(tile)
                solid_tiles.add(tile)
                
            # Шипы, Дверь и Точка спауна не меняются
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
    keys_group.empty() # Обязательно очищаем группу после .kill()
    
    try:
        if len(available_spawn_points) >= KEY_TO_WIN:
            spawn_coords = random.sample(available_spawn_points, KEY_TO_WIN)
        else:
             spawn_coords = available_spawn_points
             
        for x, y in spawn_coords:
            key = Key(x, y)
            all_sprites.add(key)
            keys_group.add(key)
            
    except ValueError as e:
        print(f"Ошибка при размещении ключей: {e}. Проверьте, достаточно ли свободных мест на карте.")


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
    
    # Обновление двери
    for door in door_group:
        door.update_visual(player.keys_collected)


def draw_fog_of_war():
    """Создание эффекта ограниченной видимости вокруг игрока."""
    # 1. Черный слой "тумана" с альфа-каналом
    fog_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    # Заполняем черным с небольшой прозрачностью (230 из 255)
    fog_surface.fill((0, 0, 0, 230)) 
    
    # 2. Рисуем "окно света" (круг) полностью прозрачным цветом
    center_x = player.rect.centerx
    center_y = player.rect.centery
    
    # Рисуем круг, используя режим BLEND_RGBA_ZERO для "стирания" пикселей
    # Если pygame.SRCALPHA используется, это не обязательно, но для надежности
    pygame.draw.circle(
        fog_surface, 
        (0, 0, 0, 0), # Полностью прозрачный цвет
        (center_x, center_y), 
        FOG_RADIUS
    )
    
    # 3. Наложение тумана на основной экран
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
    draw_text("", screen, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    draw_text("Нажмите любую клавишу для начала...", screen, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

def congratulations_screen():
    """Финальный экран (Открытка)."""
    screen.fill(GREY) # Яркий праздничный фон
    
    # Центральное поздравление
    draw_text("ПОЗДРАВЛЯЮ!", screen, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200), YELLOW)
    
    # Ваше личное сообщение
    final_message = "З Днем Народження, найгарніша блондинко Відня! Ти шалено яскрава і красива! Я дуже радий, що познайомився з тобою цього року і хочу, щоб ти й надалі освітлювала цей світ своєю красою)"
    # draw_text(final_message, screen, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), WHITE)
    draw_text("З Днем Народження, найгарніша блондинко Відня!", screen, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150), WHITE)
    draw_text("Ти шалено яскрава і красива!", screen, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100), WHITE)
    draw_text("Я дуже радий, що познайомився з тобою цього року.", screen, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2-50), WHITE)
    draw_text("Хочу, щоб ти й надалі освітлювала цей світ своєю красою)", screen, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), WHITE)
    draw_text("Твой: Миша)", screen, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50), WHITE)


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

    # --- ИЗМЕНЕНИЕ: Рендеринг фона первым ---
    screen.blit(BACKGROUND_IMAGE, (0, 0))

    if GAME_STATE == "START":
        start_screen()

    elif GAME_STATE == "PLAYING":
        keys = pygame.key.get_pressed()
        player.handle_input(keys)

        # 1. Обновление
        all_sprites.update()
        player.update_physics(solid_tiles) 
        
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
            door.on_collide(player, sys.modules[__name__]) 
        
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
