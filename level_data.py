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
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "W   W                  P P P P P P P P W", # 1 (Door, D)
    "W   WWWWWWWWWW WWWWWW WWWWWWWWWWWWWWWW W",
    "W     P P P      W W                   W",
    "W WWWWWW WWWWWWWW WWWWWWWWWWWWWWWWWWWWWW",
    "W                W W S S S S S S S S S W",
    "W WWWWWW WWWWWWWW WWWWWWWWWWWWWWWWWWWWWW",
    "W     P P P P P  W W                   W",
    "W WWWWWW WWWWWWWW WWWWWWWWWWWWWWWWWWWWWW",
    "W                W W P P P P P P P P P W",
    "W WWWWWWWWWWWWWWWW WWWWWWWWWWWWWWWWWWWWW",
    "W   S S S S S S S  W                   W",
    "W WWWWWW WWWWWWWW WWWWWWWWWWWWWWWWWWWWWW",
    "W     P P P P P  W W S S S S S S S S S W",
    "W WWWWWW WWWWWWWW WWWWWWWWWWWWWWWWWWWWWW",
    "W W              W W                   W",
    "W WWWWWWWWWWWWWWWW WWWWWWWWWWWWWWWWWWWWW",
    "W   P P P P P P P P P P P P P P P P P PW", # Длинная платформа
    "W WWWWWW WWWWWW WWWWWW WWWWWW WWWWWW WWW",
    "W                                      W",
    "W WWWWWW WWWWWW WWWWWW WWWWWW WWWWWW WWW",
    "W   S S S S S S S S S S S S S S S S S SW", # Шипы (Опасно!)
    "W WWWWWW WWWWWW WWWWWW WWWWWW WWWWWW WWW",
    "W                                      W",
    "W WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "W   P P P P P P P P P P P P P P P P P PW",
    "W WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "W                                      W",
    "W   S S S S S S S S S S S S S S S S S SW", # Шипы
    "W WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "W                                      W",
    "W   P P P P P P P P P P P P P P P P P PW",
    "W WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "W                                      W",
    "W   S S S S S S S S S S S S S S S S S SW", # Шипы
    "W WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "W                                      W",
    "W W P P P P P P P P P P P P P P P P P PW",
    "W B                                   DW", # 38 (Spawn, B)
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"
]



LEVEL_2 = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "W            P     P     P     P     DW",
    "W WWWWWW WWWWWW WWWWWW WWWWWW WWWWWWWW W",
    "W                                        W",
    "W   P     P     P     P     P     P     W",
    "W WWWWWW WWWWWW WWWWWW WWWWWW WWWWWWWW W",
    "W                                        W",
    "W  S S S     P     S S S     P     S S  W",
    "W WWWWWW WWWWWW WWWWWW WWWWWW WWWWWWWW W",
    "W                                        W",
    "W     P     P     P     P     P        W",
    "W WWWWWW WWWWWW WWWWWW WWWWWW WWWWWWWW W",
    "W                                        W",
    "W  P   P   S S S   P   P   S S S   P   W",
    "W WWWWWW WWWWWW WWWWWW WWWWWW WWWWWWWW W",
    "W                                        W",
    "W     P     P     P     P     P        W",
    "W WWWWWW WWWWWW WWWWWW WWWWWW WWWWWWWW W",
    "W                                        W",
    "W   S S S S S   P   S S S S S S S S    W",
    "W WWWWWW WWWWWW WWWWWW WWWWWW WWWWWWWW W",
    "W                                        W",
    "W      P     P     P     P     P       W",
    "W WWWWWW WWWWWW WWWWWW WWWWWW WWWWWWWW W",
    "W                                        W",
    "W  S S S S S S     P     S S S S S S   W",
    "W WWWWWW WWWWWW WWWWWW WWWWWW WWWWWWWW W",
    "W                                        W",
    "W     P     P     B     P     P        W",
    "W WWWWWW WWWWWW WWWWWW WWWWWW WWWWWWWW W",
    "W                                        W",
    "W  S S S   P   S S S   P   S S S   S S W",
    "W WWWWWW WWWWWW WWWWWW WWWWWW WWWWWWWW W",
    "W                                        W",
    "W    P     P     P     P     P         W",
    "W WWWWWW WWWWWW WWWWWW WWWWWW WWWWWWWW W",
    "W                                        W",
    "W   S S S S S S S S S S S S S S S S S  W",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"
]

LEVEL_3 = [
"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
"W    PPPP  SPPPPPP     PPSDP     PPPP  W",
"W   PPPPPPPP     PPPPPP     PPP  PPPP  W",
"WWWWWW  WWWWWWWW  WWWWWWWWWWWW    WWWWWW",
"W PPPPS  SPPPPP    SPPPPP     PPPPPP   W",
"W   PPPPPPP     PSPPPP     PPPPPPPP   PW",
"WPPPPPPPP    PSSPPPP  SPPPPP  PPPPS    W",
"WWWWWW    WWWWWWWWWWWWWWWWWWWWWW  WW  WW",
"W  PPPPPSP  PPPPPPPP     PPPPPSPP   PPPW",
"W    PPPPP    PPPPPPPP    PPPP   PPPPP W",
"W PPSPPP    PPPPPPPP     SSPPPPS   WPPPW",
"WWWWWWWWWWWWWWWWWWWWWWWW  WWWWWWWW WWWWW",
"W  SPPP     PPPPPP     PPPPPP  PPPPP   W",
"WPPPPPPP   SSP  PSPPP   PPPPPPS    PPPPW",
"WPPPPPP   PPP    PPSPPP     PPPPPPS    W",
"WW  WWWW  WWWWWW    WWWWWWWWWWWWWWWWWWWW",
"W    SPP   PSPPPP  W  PPPPPPP W   PSPPPW",
"W PPP    PPPPPPPS  PSP   PPPPPPPP  PPP W",
"W   PPPPPW  PPPPPPPP   PPPP     SPPPPP W",
"WWWWWWWW WWWWWWW  WWWWWWWWWW  WWWWWWWWWW",
"W PPPP   PPP  WPPPSPBP     PPP  SPPPPP W",
"W SPPPPPP     SPPPS   PPSPPP    PPPPPPPW",
"WPPPPPPP    PSPP   PPPPSP     PPPSPP   W",
"WWWWWWWWWWWWWWWWWW    WWWW  WWWWWWWWWWWW",
"W   PSPP    PPPPPPPP    PPPPPPP   PPPP W",
"W   PSPP     PPPPPPPP  PPPPPPP    PPP  W",
"WPPSW   SPPPPPP    PPPPPPS     PPPPPPP W",
"WWWWWWWWWWWW  WWWWWWWWWW  WWWWWWWWWWWWWW",
"W  PPPPSPSP   PPPPPPPP    PSPPPP     PPW",
"W   PPPS  PPSPSPS   PPPPPPP  PPP   PPPPW",
"W PPPPPP   PPPPPP   PPPPPP  PPSPSPPP   W",
"WW  WWWWWWWWWWWWWWWWWW  WWWWWWWW  WWWWWW",
"W   PPPPPW    PPPPP    PPP  PPPPPPPP   W",
"W    PPPPPPPP     PPPP  PPP    SPSP  SPW",
"W  SPP     PPPPPP     PPPPP    PPSPPPPPW",
"WWWWWW  WWWWWWWWWWWWWWWW  WWWWWWWWWWWWWW",
"WPPP  PPPPPP     PPPPSPPP    PPPP     PW",
"W   SPPSPPP     PPPPPP     PPPSSPPP  PPW",
"W   PPPPPP    PPSPP  PPPPP    PPP     PW",
"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"
]

