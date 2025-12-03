# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['c:\\Users\\Gabriel\\OneDrive\\Computadora\\Documents\\Programas\\Librería CEAU\\Programa.py'],
    pathex=[],
    binaries=[],
    datas=[('c:\\Users\\Gabriel\\OneDrive\\Computadora\\Documents\\Programas\\Librería CEAU\\librería.ico', '.')],
    hiddenimports=['mysql.connector', 'mysql.connector.locales.eng.client_error', 'babel.numbers', 'tkinter'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Sistema gestión de librería',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['c:\\Users\\Gabriel\\OneDrive\\Computadora\\Documents\\Programas\\Librería CEAU\\librería.ico'],
)
