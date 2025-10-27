# Данные уровня и интерпретация карты

# Определение символов для карты
TILE_MAP = {
    'W': 'Wall',       # Твердый блок 
    'P': 'Platform',   # Односторонняя платформа 
    'S': 'Spike',      # Шипы
    ' ': 'Air',        # Пустое пространство
    'B': 'Spawn',      # Начальная точка игрока 
    'D': 'Door'        # Дверь для выхода
}

# Пример карты (20x15 тайлов)
# W - Wall, P - Platform, S - Spike, B - Base, D - Door
# LEVEL_1 = [
#     "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
#     "W   W                  P P P P P P P P W", # 1 (Door, D)
#     "W   WWWWWWWWWW WWWWWW WWWWWWWWWWWWWWWW W",
#     "W     P P P      W W                   W",
#     "W WWWWWW WWWWWWWW WWWWWWWWWWWWWWWWWWWWWW",
#     "W                W W S S S S S S S S S W",
#     "W WWWWWW WWWWWWWW WWWWWWWWWWWWWWWWWWWWWW",
#     "W     P P P P P  W W                   W",
#     "W WWWWWW WWWWWWWW WWWWWWWWWWWWWWWWWWWWWW",
#     "W                W W P P P P P P P P P W",
#     "W WWWWWWWWWWWWWWWW WWWWWWWWWWWWWWWWWWWWW",
#     "W   S S S S S S S  W                   W",
#     "W WWWWWW WWWWWWWW WWWWWWWWWWWWWWWWWWWWWW",
#     "W     P P P P P  W W S S S S S S S S S W",
#     "W WWWWWW WWWWWWWW WWWWWWWWWWWWWWWWWWWWWW",
#     "W W              W W                   W",
#     "W WWWWWWWWWWWWWWWW WWWWWWWWWWWWWWWWWWWWW",
#     "W   P P P P P P P P P P P P P P P P P PW", # Длинная платформа
#     "W WWWWWW WWWWWW WWWWWW WWWWWW WWWWWW WWW",
#     "W                                      W",
#     "W WWWWWW WWWWWW WWWWWW WWWWWW WWWWWW WWW",
#     "W   S S S S S S S S S S S S S S S S S SW", # Шипы (Опасно!)
#     "W WWWWWW WWWWWW WWWWWW WWWWWW WWWWWW WWW",
#     "W                                      W",
#     "W WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
#     "W   P P P P P P P P P P P P P P P P P PW",
#     "W WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
#     "W                                      W",
#     "W   S S S S S S S S S S S S S S S S S SW", # Шипы
#     "W WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
#     "W                                      W",
#     "W   P P P P P P P P P P P P P P P P P PW",
#     "W WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
#     "W                                      W",
#     "W   S S S S S S S S S S S S S S S S S SW", # Шипы
#     "W WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
#     "W                                      W",
#     "W W P P P P P P P P P P P P P P P P P PW",
#     "W B                                   DW", # 38 (Spawn, B)
#     "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"
# ]



# LEVEL_2 = [
#     "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
#     "W            P     P     P     P     DW",
#     "W WWWWWW WWWWWW WWWWWW WWWWWW WWWWWWWW W",
#     "W                                        W",
#     "W   P     P     P     P     P     P     W",
#     "W WWWWWW WWWWWW WWWWWW WWWWWW WWWWWWWW W",
#     "W                                        W",
#     "W  S S S     P     S S S     P     S S  W",
#     "W WWWWWW WWWWWW WWWWWW WWWWWW WWWWWWWW W",
#     "W                                        W",
#     "W     P     P     P     P     P        W",
#     "W WWWWWW WWWWWW WWWWWW WWWWWW WWWWWWWW W",
#     "W                                        W",
#     "W  P   P   S S S   P   P   S S S   P   W",
#     "W WWWWWW WWWWWW WWWWWW WWWWWW WWWWWWWW W",
#     "W                                        W",
#     "W     P     P     P     P     P        W",
#     "W WWWWWW WWWWWW WWWWWW WWWWWW WWWWWWWW W",
#     "W                                        W",
#     "W   S S S S S   P   S S S S S S S S    W",
#     "W WWWWWW WWWWWW WWWWWW WWWWWW WWWWWWWW W",
#     "W                                        W",
#     "W      P     P     P     P     P       W",
#     "W WWWWWW WWWWWW WWWWWW WWWWWW WWWWWWWW W",
#     "W                                        W",
#     "W  S S S S S S     P     S S S S S S   W",
#     "W WWWWWW WWWWWW WWWWWW WWWWWW WWWWWWWW W",
#     "W                                        W",
#     "W     P     P     B     P     P        W",
#     "W WWWWWW WWWWWW WWWWWW WWWWWW WWWWWWWW W",
#     "W                                        W",
#     "W  S S S   P   S S S   P   S S S   S S W",
#     "W WWWWWW WWWWWW WWWWWW WWWWWW WWWWWWWW W",
#     "W                                        W",
#     "W    P     P     P     P     P         W",
#     "W WWWWWW WWWWWW WWWWWW WWWWWW WWWWWWWW W",
#     "W                                        W",
#     "W   S S S S S S S S S S S S S S S S S  W",
#     "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"
# ]

# LEVEL_3 = [
# "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
# "W          S             SD            W",
# "W                            PP  PPPP  W",
# "WWWWWW  WWWWWWWW  WWWWWWWWWWWW    WWWWWW",
# "W     S  S         S          PPPP     W",
# "W   PPPPPPP     PSPPPP     PPPPPPPP   PW",
# "W     PPP     SS      S       PPPPS    W",
# "WWWWWW    WWWWWWWWWWWWWWWWWWWWWW  WW  WW",
# "W     PPSP                    S P   PPPW",
# "W    PPPPP    PPPPPPPP    PPPP   PPPPP W",
# "W   S       PPPPPPPP     SSPPPPS   WPPPW",
# "WWWWWWWWWWWWWWWWWWWWWWWW  WWWWWWWW WWWWW",
# "W  S        PPPPPP     PPPPPP  PPPPP   W",
# "W          SSP  PSPPP   PPPPPPS    PPPPW",
# "WPPPPPP   PPP    PPSPPP     PPPPPPS    W",
# "WW  WWWW  WWWWWW    WWWWWWWWWWWWWWWWWWWW",
# "W    S     PSPPPP PW  PPPPPPP W   PSPPPW",
# "W PPP    PPPPPPPS  PSP   PPPPPPPP  PPP W",
# "W       PW  PPPPPPPP   PPPP     SPPPPP W",
# "WWWWWWWW WWWWWWW  WWWWWWWWWW  WWWWWWWWWW",
# "W PPPP   PPP  WPPPS B       PP  SPPPPP W",
# "W SPPPPPP     SPPPS   PPSPPP    PPPPPPPW",
# "W           PSPP   PPPPSP        S     W",
# "WWWWWWWWWWWWWWWWWW    WWWW  WWWWWWWWWWWW",
# "W   PSPP    PPPPPPPP    PPPPPPP   PPPP W",
# "W   PSPP     PPPPPPPP  PPPPPPP    PPP  W",
# "WPPSW   SPPPPPP    PPPPPPS     PPPPPPP W",
# "WWWWWWWWWWWW  WWWWWWWWWW  WWWWWWWWWWWWWW",
# "W  PPPPSPSP   PPPPPPPP    PSPPPP       W",
# "W   PPPS  PPSPSPS   PPPPPPP  PPP   PP  W",
# "W PPPPPP   PPPPPP   PPPPPP  PPSPSPPP   W",
# "WW  WWWWWWWWWWWWWWWWWW  WWWWWWWW  WWWWWW",
# "W  P     W              P      PPP     W",
# "W    PPPPPPPP     PPPP  PPP    SPSP  SPW",
# "W  SPP     PPPPPP     PPPPP    PPSPPPPPW",
# "WWWWWW  WWWWWWWWWWWWWWWW  WWWWWWWWWWWWWW",
# "W     PP         PPPPSPPP             PW",
# "W   SPPSPPP     PPPPPP     PPPSSPPP  PPW",
# "W   PPPPPP    PPSPP  PPPPP    PPP     PW",
# "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"
# ]


LEVEL_4 = [
"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
"W          S             SD            W",
"W                            PP  PPPP  W",
"WWWWWW PWWWWWWWW WWWWWWWWWWWWW    WWWWWW",
"W     S            S          PPPP     W",
"W   PPPP P     PSPPPP     PPP        P W",
"W       P     SS      S         PPS    W",
"WWWWWW    WWWWWWWWWWWWWWWWWWWWWW  WW  WW",
"W     PPSP                    S P   PP W",
"W    PPPPP    PPPPPPPP    PPPP   PPPPP W",
"W   S                    SS    S   W   W",
"WWWWWWWWWWWWWWWWWWWWWWWW  WWWWWWWW  WWWW",
"W  S                    PP        P    W",
"W          SSP  PSPPP   PPPPPPS    PPPPW",
"WPPPPPP          PPS              S    W",
"WW  WWWW PWWWWWW    WWWWWWWWWWWWWWWWWWWW",
"W    S      S   P PW          W    S   W",
"W PPP     PPPPP     SP   PPPP   P  PPP W",
"W       PW      PP              S      W",
"WWWWWWWW WWWWWWW  WWWWWWWWWW  WWWWWWWWWW",
"W             W P   B       PP  S      W",
"W SPPPPPP     SP P    PPSPPP    PPPPPPPW",
"W            S     PPP S               W",
"WWWWWWWWWWWWWWWWWWP   WWWW   WWWWWWWWWWW",
"W    S                     P           W",
"W    SPP     PPPPPPPP    PP PP    PPP  W",
"W  SW   S   P           PS             W",
"WWWWWWWWWWWW  WWWWWWWWWW  WWWWWWWWWWWWWW",
"W      S S                 S           W",
"W   PPPS  PPSPSPS   PP  PPP  PPP   PP  W",
"W PP                  PP      S SP     W",
"WW  WWWWWWWWWWWWWWWWWW  WWWWWWWW  WWWWWW",
"W  P     W            P          P     W",
"W    PPPP PPP     PPP    PP     P P  SPW",
"W  S                    P              W",
"WWWWWW  WWWWWWWWWWWWWWWW  WWWWWWWWWWWWWW",
"W     PP             S  P              W",
"W   SPPSPPP     PPPPPP     PPPSSPPP    W",
"W               S                     PW",
"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"
]

