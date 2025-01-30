# -*- mode: python ; coding: utf-8 -*-

import sys
import platform

os = platform.system()

if os == "Windows":
    current_system_binaries = [
        (f"{sys.prefix}/Library/bin/*.dll", "./Library/bin/")
    ]
elif os == "Linux":
    current_system_binaries = [
        (f"{sys.prefix}/lib/*.so*", "./lib/")
    ]
else:
    current_system_binaries = []


a = Analysis(
    ['vibra/launch.py'],
    pathex=[],
    binaries=current_system_binaries,
    datas=[
        ("vibra/interface/data/", "vibra/interface/data/")
    ],
    hiddenimports=[
        "vtk"
    ],
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
    [],
    exclude_binaries=True,
    name='vibra.exe',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['vibra.ico'],
)


coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Vibra',
)
