

from kivy_deps import sdl2, glew
import os
import sys

# Имя приложения
APP_NAME = 'Timer'

# Папка с ресурсами
ASSETS_DIR = 'assets'

# Основной скрипт
main_script = 'main.py'

# Функция для формирования путей
def get_resources():
    return [
        (os.path.join(ASSETS_DIR, '*'), ASSETS_DIR),  # Все файлы из assets
        ('timer.kv', '.'),                           # KV-файл в корне
    ]

# Анализ зависимостей
a = Analysis(
    [main_script],
    pathex=[os.path.abspath('.')],  # Путь к вашему проекту
    binaries=[],
    datas=get_resources(),          # Добавляем ресурсы
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
)

# Архив Python-библиотек
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# Настройки исполняемого файла
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=APP_NAME,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # Отключите UPX, если возникают проблемы
    console=False,  # Скрыть консоль
    icon=os.path.join(ASSETS_DIR, 'icon.ico'),  # Иконка из assets
)

# Сборка всех данных
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],  # Зависимости Kivy
    strip=False,
    upx=False,
    upx_exclude=[],
    name=APP_NAME,
)