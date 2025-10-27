# Данные уровня и интерпретация карты

# Определение символов для карты
TILE_MAP = {
    'W': 'Wall',       # Твердый блок (земля, стена)
    'P': 'Platform',   # Односторонняя платформа (можно спуститься)
    'S': 'Spike',      # Шипы (смерть/урон)
    ' ': 'Air',        # Пустое пространство
    'B': 'Spawn',      # Начальная точка игрока (Base)
    'D': 'Door'        # Дверь для выхода
}

# Пример карты (20x15 тайлов)
# W - Wall, P - Platform, S - Spike, B - Base, D - Door
LEVEL_1 = [
    "WWWWWWWWWWWWWWWWWWWW",
    "W                  W",
    "W                  W",
    "W         P P P    W",
    "W WWWWWWWWWWWWWWW  W",
    "W                  W",
    "W  S S S           W",
    "W WWWWWWWWWWWWP W  W",
    "W             P W  W",
    "W  P P P      P W  W",
    "W WWWWWWWWWWW   W  W",
    "W S S S S S S   W  W",
    "W WWWWWWWWWWWW  W  D",
    "W B                W",
    "WWWWWWWWWWWWWWWWWWWW",
    ]
