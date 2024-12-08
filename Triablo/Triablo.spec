# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['Triablo.py'],
    pathex=[],
    binaries=[('*.dll', '.')],
    datas=[('C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Othersprite', 'Othersprite/'), ('C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/collider_coordinates.txt', '.')],
    hiddenimports=[],
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
    name='Triablo',
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
)
