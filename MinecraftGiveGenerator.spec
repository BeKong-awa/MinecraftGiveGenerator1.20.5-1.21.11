# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['give.py'],
    pathex=[
    r'D:\工具\..by Be_Kong\高版本数据组件生成器(鸽\nbt',
    r'D:\工具\..by Be_Kong\高版本数据组件生成器(鸽\nbt\py_files'
],
    binaries=[],
    datas=[],
    hiddenimports=[
        'banner_generator',
        'component_mapper',
        'equippable_generator',
        'fireworks_generator',
        'food_generator',
        'potion_effects',
        'skull_generator',
        'tool_generator',
        'written_book_generator',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MinecraftGiveGenerator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='command_block.ico'
)