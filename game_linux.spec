# -*- mode: python ; coding: utf-8 -*-
#
# Файл спецификации для PyInstaller
# Используется для создания самодостаточного исполняемого файла для Linux.

import sys

# Добавляем все файлы ассетов и модули, которые PyInstaller должен включить.
added_files = [
    ('air.png', '.'),
    ('door.png', '.'),
    ('keeey.png', '.'),
    ('plat.png', '.'),
    ('player.png', '.'),
    ('sss.png', '.'),
    ('wall.png', '.'),
    # Также добавляем файлы Python
    ('config.py', '.'),
    ('level_data.py', '.'),
    ('sprites.py', '.'),
]

# Анализ проекта
a = Analysis(
    ['main.py'], # Главный исполняемый файл
    pathex=['.'], # Путь поиска исходников
    binaries=[],
    datas=added_files,
    hiddenimports=['pygame'], # Убедимся, что pygame импортирован правильно
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    name='КвестПлатформер',
    # Для Linux обычно используется 'unix', но PyInstaller сам определит OS
    target_arch=None, 
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# --- Настройки для Linux (One-File Executable) ---
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='КвестПлатформер',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True, # Оставляем консоль для отладки, если нужно. Можно поменять на False.
    # Этот флаг - ключ к созданию одного файла
    # 'onefile=True' в команде сборки делает то же самое
)

# Для Linux мы собираем в один исполняемый файл (OneFile)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='КвестПлатформер',
)
